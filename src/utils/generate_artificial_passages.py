import random
from tqdm import tqdm

def main():
    # Read documents numbers from mapping file
    print("Reading documents numbers from mapping file...")
    docs = []
    with open('/Users/slawek/PycharmProjects/ColBERT/docs/downloads/msmarco_passage/collection.tsv', 'r') as f:
        for line in f:
            doc_id = line.strip().split('\t')[0]
            docs.append(doc_id)


    # Read relevant docs from qrels file
    print("Reading relevant docs from qrels file...")
    relevant_docs = []
    with open('/Users/slawek/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/qrels.tsv', 'r') as f:
        for line in f:
            _, _, pid, _ = line.strip().split('\t')
            relevant_docs.append(pid)

    non_relevant_docs = list(set(docs) - set(relevant_docs))

    # # Choose random non relevant docs for each relevant doc
    # sampled_non_relevant_docs = random.sample(non_relevant_docs, len(relevant_docs))

    # Read collection and append non-relevant docs to the beggining of relevant docs in the collection
    print("Reading collection and appending non-relevant docs to the beggining of relevant docs in the collection...")
    collection = {}
    with open('/Users/slawek/PycharmProjects/ColBERT/docs/downloads/msmarco_passage/collection.tsv', 'r') as f:
        for i, line in tqdm(enumerate(f)):
            doc_id, text = line.strip().split('\t')
            collection[doc_id] = text

    # Write new collection to file
    print("Writing new collection to file...")
    prefix_collection = {}
    postfix_collection = {}
    random_collection = {}
    for i in tqdm(collection.keys()):
        if i not in relevant_docs:
            prefix_collection[i] = collection[i]
            postfix_collection[i] = collection[i]
            random_collection[i] = collection[i]
        else:
            doc_id = i
            random_doc_id = random.sample(non_relevant_docs, 1)[0]
            relevant_doc = collection[doc_id].split(' ')
            non_relevant_doc = collection[random_doc_id].split(' ')

            while len(non_relevant_doc) < 450:
                non_relevant_doc = non_relevant_doc + collection[random.sample(non_relevant_docs, 1)[0]].split(' ')

            n = len(relevant_doc)

            prefix = non_relevant_doc.copy()
            postfix = non_relevant_doc.copy()
            random_place = non_relevant_doc.copy()

            prefix[-n:] = relevant_doc
            postfix[:n] = relevant_doc
            x = random.randint(0, len(non_relevant_doc) - n)
            random_place[x:x + n] = relevant_doc

            prefix_collection[doc_id] = ' '.join(prefix)
            postfix_collection[doc_id] = ' '.join(postfix)
            random_collection[doc_id] = ' '.join(random_place)

    with open('/Users/slawek/PycharmProjects/ColBERT/docs/downloads/msmarco_passage/prefix_collection.tsv', 'w') as f:
        for doc_id in prefix_collection:
            f.write(f"{doc_id}\t{prefix_collection[doc_id]}\n")

    with open('/Users/slawek/PycharmProjects/ColBERT/docs/downloads/msmarco_passage/postfix_collection.tsv', 'w') as f:
        for doc_id in postfix_collection:
            f.write(f"{doc_id}\t{postfix_collection[doc_id]}\n")

    with open('/Users/slawek/PycharmProjects/ColBERT/docs/downloads/msmarco_passage/random_collection.tsv', 'w') as f:
        for doc_id in random_collection:
            f.write(f"{doc_id}\t{random_collection[doc_id]}\n")


if __name__ == "__main__":
    main()