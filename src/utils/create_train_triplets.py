import csv
import random
from argparse import ArgumentParser

# This file is used for adding negative examples to the training data. Training data is in the form of pair (query_id, doc_id).

def main(args):
    # Read relevant (query_id, doc_id) pairs from the first TSV file
    relevant_pairs = []
    query_relevant_docs = {}  # Dictionary to hold list of relevant doc_ids for each query_id
    with open(args.relevant_pairs, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            query_id, relevant_doc_id = row
            relevant_pairs.append((query_id, relevant_doc_id))

            # Populate query_relevant_docs dictionary
            if query_id not in query_relevant_docs:
                query_relevant_docs[query_id] = []
            query_relevant_docs[query_id].append(relevant_doc_id)

    # Read all document ids from the second TSV file
    map = {}
    all_doc_ids = []
    with open(args.map, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            map[row[1]] = row[0]
            all_doc_ids.append(row[1])

    # Prepare training triplets
    training_triplets = []
    for query_id, relevant_doc_id in relevant_pairs:
        # Select a random negative example that is not a relevant document for the query
        negative_doc_id = random.choice(all_doc_ids)
        while negative_doc_id in query_relevant_docs[query_id]:
            negative_doc_id = random.choice(all_doc_ids)

        training_triplets.append((query_id, relevant_doc_id, negative_doc_id))

    training_triplets_mapped = []
    for qid, pid_pos, pid_neg in training_triplets:
        training_triplets_mapped.append((qid, map[pid_pos], map[pid_neg]))

    # Write training triplets to a new TSV file
    with open(args.output_path, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for triplet in training_triplets_mapped:
            writer.writerow(triplet)

    print("Training triplets have been written to training_triplets.tsv.")
    print(f"Test: {map['D576811']}")

if __name__ == "__main__":
    parser = ArgumentParser(description="Create train triplets")

    # Input Arguments.
    parser.add_argument('--map', dest='map',
                        default="/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/map.tsv",
                        type=str)

    parser.add_argument('--relevant_pairs', dest='relevant_pairs',
                        default="/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/train_triplets.tsv",
                        type=str)
    parser.add_argument('--output_path', dest='output_path',
                        default="/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/dupa.tsv",
                        type=str, help='Output path')

    args = parser.parse_args()

    main(args)
