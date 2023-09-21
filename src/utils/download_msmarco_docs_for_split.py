import ir_datasets
from tqdm import tqdm

if __name__ == '__main__':
    dataset = ir_datasets.load("msmarco-document/dev")

    # Define the path to the output TSV file
    collection_file_path = "/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/collection_original.tsv"
    mapping_file_path = "/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/map_original.tsv"

    res = []
    mapping_table = str.maketrans({'\n': ' ', '\t': ' '})

    print("Creating collections file...")
    # Open the file for writing
    with open(collection_file_path, "w", encoding="utf-8") as outfile:

        # Iterate through the documents
        for idx, doc in tqdm(enumerate(dataset.docs_iter())):
            # Remove newlines from title and body and merge with a space in between
            doc_id = doc.doc_id
            url = doc.url
            title_clean = doc.title.translate(mapping_table)
            body_clean = doc.body.translate(mapping_table)

            res.append((idx, doc.doc_id))
            # Write the doc_id and merged title_body to the TSV file
            outfile.write(f"{doc_id}\t{url}\t{title_clean}\t{body_clean}\n")

    with open(mapping_file_path, "w", encoding="utf-8") as outfile:
        for idx, doc_id in tqdm(res):
            outfile.write(f"{idx}\t{doc_id}\n")

    print(f"Collection has been written to {collection_file_path}")