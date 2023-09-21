import csv
import json
import random
from argparse import ArgumentParser

# This file is used remapping doc ids in the training triplets to the doc ids in the map.tsv file

def main(args):

    queries_count = dict()
    with open(args.train_triplets, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            query_id, _, _ = row
            if query_id not in queries_count.keys():
                queries_count[query_id] = 1
            else:
                queries_count[query_id] += 1

    # Read train triplets with original doc ids
    train_triplets = []
    seen_query_ids = dict()
    with open(args.train_triplets, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            query_id, pid_pos, pid_neg = row
            # Skip the first occurrence of each query_id
            if query_id not in seen_query_ids.keys():
                seen_query_ids[query_id] = 1
                continue

            if query_id in seen_query_ids.keys() and seen_query_ids[query_id] > 3:
                continue

            if queries_count[query_id] < 4:
                continue

            seen_query_ids[query_id] += 1
            train_triplets.append((int(query_id), pid_pos, pid_neg))

    # Read the map
    map = {}
    with open(args.map, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            id, doc_id = row
            map[doc_id] = int(id)

    training_triplets_mapped = []
    for qid, pid_pos, pid_neg in train_triplets:
        training_triplets_mapped.append((qid, map[pid_pos], map[pid_neg]))

    # # Write training triplets to a new TSV file
    # with open(args.output_path, 'w') as f:
    #     writer = csv.writer(f, delimiter='\t')
    #     for triplet in training_triplets_mapped:
    #         writer.writerow(triplet)

    # Write training triplets to a new JSONL file
    with open(args.output_path, 'w') as f:
        for triplet in training_triplets_mapped:
            f.write(json.dumps(triplet) + '\n')

    print("Training triplets have been written to train_triplets.jsonl")

if __name__ == "__main__":
    parser = ArgumentParser(description="Docs mapping")

    # Input Arguments.
    parser.add_argument('--map', dest='map',
                        default="/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/map.tsv",
                        type=str)

    parser.add_argument('--train_triplets', dest='train_triplets',
                        default="/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/train_triplets.tsv",
                        type=str)
    parser.add_argument('--output_path', dest='output_path',
                        default="/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/train_triplets.jsonl",
                        type=str, help='Output path')
    # parser.add_argument('--output_path', dest='output_path',
    #                     default="/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/train_triplets.tsv",
    #                     type=str, help='Output path')

    args = parser.parse_args()

    main(args)
