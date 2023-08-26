import os
import tqdm
from argparse import ArgumentParser
from collections import defaultdict
from colbert.utils.utils import print_message, file_tqdm


def get_bin(length, min_length, max_length, bin_width):
    if length == max_length:
        return 9  # Ensure the maximum length goes in the last bin
    return min(int((length - min_length) / bin_width), 9)


def main(args):
    # 1. Load pid2length
    pid2length = {}
    with open(args.doc_lengths_tsv, 'r') as f:
        for line in f:
            doc_id, num_words = line.strip().split('\t')
            pid2length[int(doc_id)] = int(num_words)

    min_length = min(pid2length.values())
    max_length = max(pid2length.values())
    bin_width = (max_length - min_length) / 10

    qid2positives = defaultdict(list)
    qid2ranking = defaultdict(list)

    qid2mrr = defaultdict(lambda: defaultdict(float))
    qid2recall = {depth: defaultdict(lambda: defaultdict(float)) for depth in [10, 100]}

    with open(args.qrels) as f:
        print_message(f"#> Loading QRELs from {args.qrels} ..")
        for line in file_tqdm(f):
            qid, _, pid, label = map(int, line.strip().split())
            assert label == 1

            qid2positives[qid].append(pid)

    with open(args.ranking) as f:
        print_message(f"#> Loading ranked lists from {args.ranking} ..")
        for line in file_tqdm(f):
            qid, pid, rank, *score = line.strip().split('\t')
            qid, pid, rank = int(qid), int(pid), int(rank)

            if len(score) > 0:
                assert len(score) == 1
                score = float(score[0])
            else:
                score = None

            qid2ranking[qid].append((rank, pid, score))

    for qid in tqdm.tqdm(qid2positives):
        ranking = qid2ranking[qid]
        positives = qid2positives[qid]

        for rank, (_, pid, _) in enumerate(ranking):
            rank = rank + 1  # 1-indexed

            if pid in positives:
                bin_id = get_bin(pid2length[pid], min_length, max_length, bin_width)
                if rank <= 10:
                    qid2mrr[bin_id][qid] = 1.0 / rank
                break

        for rank, (_, pid, _) in enumerate(ranking):
            rank = rank + 1  # 1-indexed

            if pid in positives:
                bin_id = get_bin(pid2length[pid], min_length, max_length, bin_width)
                for depth in qid2recall:
                    if rank <= depth:
                        qid2recall[depth][bin_id][qid] = qid2recall[depth][bin_id].get(qid, 0) + 1.0 / len(positives)

    # Save the results per bin
    with open(args.output, 'w') as out_file:
        for bin_id in range(10):
            mrr_values = qid2mrr[bin_id]
            mrr_10_sum = sum(mrr_values.values())

            bin_start = min_length + bin_id * bin_width
            bin_end = bin_start + bin_width

            out_file.write(f"Bin {bin_id+1} (Length {bin_start}-{bin_end}):\n")
            out_file.write(f"MRR@10 = {mrr_10_sum / len(mrr_values) if len(mrr_values) > 0 else 0}\n")

            for depth in [10, 100]:
                recall_values = qid2recall[depth][bin_id]
                recall_sum = sum(recall_values.values())
                out_file.write(f"Recall@{depth} = {recall_sum / len(recall_values) if len(recall_values) > 0 else 0}\n")

            out_file.write("-" * 40 + "\n")


if __name__ == "__main__":
    parser = ArgumentParser(description="msmarco_passages.")

    # Input Arguments.
    parser.add_argument('--qrels', dest='qrels', type=str, default="/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_passage/qrels.dev.tsv")
    parser.add_argument('--ranking', dest='ranking', type=str, default="/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/experiments/msmarco_passage/retrieval/2023-08/14/03.59.59/msmarco.nbits=2.dev.ranking.tsv")
    parser.add_argument('--doc_lengths_tsv', dest='doc_lengths_tsv', type=str, default="/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/msmarco_passage_doc_lengths.tsv")
    parser.add_argument('--annotate', dest='annotate', default=False, action='store_true')

    args = parser.parse_args()

    if args.annotate:
        args.output = f'{args.ranking}.annotated'
        assert not os.path.exists(args.output), args.output
    else:
        args.output = 'evaluation_by_length_bins.txt'

    main(args)
