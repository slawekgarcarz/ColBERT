import csv
from tqdm import tqdm
from argparse import ArgumentParser


# Function to count words in a text
def count(text):
    return len(text.split())

def main(args):
    # Read the input TSV and create a new one with the desired output
    with open(args.collection_path, 'r', encoding='utf-8') as input_file, open(f"./data/{args.output_name}.tsv", 'w', encoding='utf-8',
                                                                      newline='') as output_file:
        # Using the csv module to handle TSV files
        tsv_reader = csv.reader(input_file, delimiter='\t')
        tsv_writer = csv.writer(output_file, delimiter='\t')

        # Write header to the output TSV
        tsv_writer.writerow(['id', 'number of words'])

        # Iterate through each row in the input TSV
        for row in tqdm(tsv_reader):
            # Assuming the 'id' is in the first column and 'text' is in the second
            doc_id = row[0]
            text = row[1]

            # Write the 'id' and the word count to the output TSV
            tsv_writer.writerow([doc_id, count(text)])

    print(f"Processing complete. The word counts are saved in '{args.output_name}.tsv'.")


if __name__ == "__main__":
    parser = ArgumentParser(description="Count words")

    # Input Arguments.
    parser.add_argument('--collection_path', dest='collection_path', required=True, type=str)
    parser.add_argument('--output_name', dest='output_name', required=True, type=str)

    args = parser.parse_args()

    main(args)

