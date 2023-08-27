from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Trainer
from argparse import ArgumentParser

def main(args):

    with Run().context(RunConfig(nranks=4, experiment=args.experiment)):
        config = ColBERTConfig(
            bsize=args.bsize,
            root=f"./experiments/{args.experiment}",
        )
        trainer = Trainer(
            triples=args.triples_path,
            queries=args.queries_path,
            collection=args.collection_path,
            config=config,
        )

        checkpoint_path = trainer.train()

        print(f"Saved checkpoint to {checkpoint_path}...")


if __name__ == "__main__":
    parser = ArgumentParser(description="Trainer ColBERT.")

    # Input Arguments.
    parser.add_argument('--queries_path', dest='queries_path', default='./docs/downloads/msmarco_docs/queries.tsv', type=str)
    parser.add_argument('--collection_path', dest='collection_path', default='./docs/downloads/msmarco_docs/collection.tsv', type=str)
    parser.add_argument('--triples_path', dest='triples_path', default='./docs/downloads/msmarco_docs/triples.tsv', type=str)
    parser.add_argument('--bsize', dest='bsize', default=32, type=int)
    parser.add_argument('--experiment', dest='experiment', default='msmarco_passage', type=str) # msmarco_passage or msmarco_docs

    args = parser.parse_args()

    main(args)
