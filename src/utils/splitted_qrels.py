from tqdm import tqdm
import sys
import pandas as pd
from collections import defaultdict

splitted_map_file = '/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/map_splitted.tsv'
original_map_file = '/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/map_original.tsv'
qrels_file = '/gpfs/work5/0/gusr0664/data/msmarco_docs/qrels.tsv'
new_qrels_file = '/gpfs/work5/0/gusr0664/data/msmarco_docs/splitted_qrels.tsv'

def load_original_map(map_file):
    map = dict()
    with open(map_file, 'r') as f:
        for line in f:
            l = line.split('\t')
            map[l[1].strip()] = l[0]

    print('Original map loaded')

    return map


def load_splitted_map(map_file):
    map = defaultdict(list)
    with open(map_file, 'r') as f:
        for line in f:
            l = line.split('\t')
            map[l[1].strip()].append(l[0])

    print('Splitted map loaded')

    return map

if __name__ == '__main__':
    splitted_map = load_splitted_map(splitted_map_file)
    original_map = load_original_map(original_map_file)

    new_map = dict()
    for k, v in tqdm(splitted_map.items()):
        new_k = original_map[k]
        new_map[new_k] = v

    res = []

    with open(qrels_file, 'r') as f:
        for line in f:
            l = line.split('\t')
            if l[2].strip() in new_map:
                for doc in new_map[l[2].strip()]:
                    res.append([l[0].strip(), l[1].strip(), int(doc), l[3].strip()])

    with open(new_qrels_file, 'w') as f:
        for r in res:
            f.write('\t'.join(r) + '\n')
