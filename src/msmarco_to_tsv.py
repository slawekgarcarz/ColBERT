import ir_datasets
from tqdm import tqdm

if __name__ == '__main__':
    dataset = ir_datasets.load("msmarco-document/dev")

    # Define the path to the output TSV file
    collection_file_path = "./docs/downloads/msmarco_docs/collection.tsv"
    queries_file_path = "./docs/downloads/msmarco_docs/queries.tsv"
    qrels_file_path = "./docs/downloads/msmarco_docs/qrels.tsv"
    mapping_file_path = "./docs/downloads/msmarco_docs/map.tsv"

    res = []
    mapping_table = str.maketrans({'\n': ' ', '\t': ' '})

    print("Creating collections file...")
    # Open the file for writing
    with open(collection_file_path, "w", encoding="utf-8") as outfile:

        # Iterate through the documents
        for idx, doc in tqdm(enumerate(dataset.docs_iter())):
            # Remove newlines from title and body and merge with a space in between
            title_clean = doc.title.translate(mapping_table)
            body_clean = doc.body.translate(mapping_table)
            title_body = title_clean + " " + body_clean

            res.append((idx, doc.doc_id))
            # Write the doc_id and merged title_body to the TSV file
            outfile.write(f"{idx}\t{title_body}\n")

    with open(mapping_file_path, "w", encoding="utf-8") as outfile:
        for idx, doc_id in tqdm(res):
            outfile.write(f"{idx}\t{doc_id}\n")

    print(f"Collection has been written to {collection_file_path}")

    print("Creating queries file...")
    # Open the file for writing
    with open(queries_file_path, "w", encoding="utf-8") as outfile:

        # Iterate through the documents
        for idx, query in tqdm(enumerate(dataset.queries_iter())):
            # Remove newlines from the query
            clean_query = query.text.translate(mapping_table)

            # Write the query_id and query to the TSV file
            outfile.write(f"{query.query_id}\t{clean_query}\n")

    print(f"Queries has been written to {queries_file_path}")

    print("Creating qrels file...")
    # Open the file for writing

    map = {}

    with open(mapping_file_path, 'r', encoding="utf-8") as infile:
        for line in infile:
            idx, doc_id = line.strip().split('\t')
            map[doc_id] = idx

    with open(qrels_file_path, "w", encoding="utf-8") as outfile:

        # Iterate through the documents
        for idx, qrel in tqdm(enumerate(dataset.qrels_iter())):

            # Write the query_id and query to the TSV file
            outfile.write(f"{qrel.query_id}\t{qrel.iteration}\t{map[qrel.doc_id]}\t{qrel.relevance}\n")

    print(f"Qrels has been written to {qrels_file_path}")
