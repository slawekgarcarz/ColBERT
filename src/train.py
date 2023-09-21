import sys

sys.path.append( '/gpfs/home3/sgarcarz/PycharmProjects/ColBERT' )

from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Trainer
from argparse import ArgumentParser

def main(args):

    with Run().context(RunConfig(nranks=4, experiment=args.experiment)):
        config = ColBERTConfig(
            bsize=args.bsize,
            root=f"./experiments/{args.experiment}",
            doc_maxlen=args.doc_maxlen,
            maxsteps=args.maxsteps,
            lr=3e-06, warmup=None, dim=128, nway=args.nway, accumsteps=1, use_ib_negatives=False
        )
        trainer = Trainer(
            triples=args.triplets_path,
            queries=args.queries_path,
            collection=args.collection_path,
            config=config,
        )

        checkpoint_path = trainer.train(checkpoint='/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/colbertv2.0')

        print(f"Saved checkpoint to {checkpoint_path}...")


if __name__ == "__main__":
    parser = ArgumentParser(description="Trainer ColBERT.")

    # Input Arguments.
    parser.add_argument('--queries_path', dest='queries_path', default='/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/train_queries.tsv', type=str)
    parser.add_argument('--collection_path', dest='collection_path', default='/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/collection.tsv', type=str)
    parser.add_argument('--triplets_path', dest='triplets_path', default='/gpfs/home3/sgarcarz/PycharmProjects/ColBERT/docs/downloads/msmarco_docs/train_triplets.jsonl', type=str)
    parser.add_argument('--bsize', dest='bsize', default=32, type=int)
    parser.add_argument('--experiment', dest='experiment', default='msmarco_docs_finetuning_256', type=str) # msmarco_passage or msmarco_docs
    parser.add_argument('--doc_maxlen', dest='doc_maxlen', default=256, type=int)
    parser.add_argument('--maxsteps', dest='maxsteps', default=100000, type=int)
    parser.add_argument('--nway', dest='nway', default=2, type=int)

    args = parser.parse_args()

    main(args)
