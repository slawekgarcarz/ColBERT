import sys

sys.path.append( '/gpfs/home3/sgarcarz/PycharmProjects/ColBERT' )

from argparse import ArgumentParser

from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Indexer


def main(args):

    index_name = f'{args.dataset}.{args.nbits}bits'

    with Run().context(RunConfig(nranks=4, experiment=args.experiment)):

        config = ColBERTConfig(
            nbits=args.nbits,
            doc_maxlen=args.doc_maxlen
        )
        indexer = Indexer(checkpoint=args.checkpoint_path, config=config)
        indexer.index(name=index_name, collection=args.collection_path)


if __name__ == "__main__":
    parser = ArgumentParser(description="Indexing parser")

    # Input Arguments.
    parser.add_argument('--collection_path', dest='collection_path', default='./docs/downloads/msmarco_docs/collection.tsv', type=str)
    parser.add_argument('--checkpoint_path', dest='checkpoint_path', default='./docs/downloads/colbertv2.0', type=str)
    parser.add_argument('--dataset', dest='dataset', default='msmarco_docs', type=str) # msmarco_passage or msmarco_docs
    parser.add_argument('--experiment', dest='experiment', default='msmarco_docs', type=str) # msmarco_passage or msmarco_docs
    parser.add_argument('--nbits', dest='nbits', default=2, type=int)
    parser.add_argument('--doc_maxlen', dest='doc_maxlen', default=256, type=int)

    args = parser.parse_args()

    main(args)
