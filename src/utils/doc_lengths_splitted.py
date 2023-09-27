import pandas as pd


# Read tsv file
map_original = pd.read_csv('/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/map_original.tsv', sep='\t', header=None, names=['id', 'doc_id'])
map_splitted = pd.read_csv('/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/map_splitted.tsv', sep='\t', header=None, names=['id', 'doc_id'])
doc_lengths_original = pd.read_csv('/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/src/data/msmarco_docs_doc_lengths.tsv', sep='\t', header=None, names=['id', 'length'])

map_with_lengths = map_original.merge(doc_lengths_original, how='left', on='id')

del map_with_lengths['id']

doc_lengths_splitted = map_splitted.merge(map_with_lengths, how='left', on='doc_id')

del doc_lengths_splitted['doc_id']

# Check if there are na values
doc_lengths_splitted.isna().sum()

# Change na to 513
doc_lengths_splitted['length'] = doc_lengths_splitted['length'].fillna(513)

# Change type of length column to int
doc_lengths_splitted['length'] = doc_lengths_splitted['length'].astype(int)


# Save tsv file without header
doc_lengths_splitted.to_csv('/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/src/data/msmarco_docs_doc_lengths_splitted.tsv', sep='\t', header=False, index=False)
