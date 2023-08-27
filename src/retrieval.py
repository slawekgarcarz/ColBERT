from colbert.data import Queries
from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Searcher
from argparse import ArgumentParser

def main(args):

    with Run().context(RunConfig(nranks=4, experiment=args.experiment)):
        config = ColBERTConfig(
            root=f"./experiments/{args.experiment}",
        )
        searcher = Searcher(index=args.index_name, config=config)
        queries = Queries(args.queries_path)
        ranking = searcher.search_all(queries, k=args.k)
        ranking.save(f"{args.experiment}_{args.k}_ranking_small.tsv")


if __name__ == "__main__":
    parser = ArgumentParser(description="Retrieval parser")

    # Input Arguments.
    parser.add_argument('--queries_path', dest='queries_path', default='./docs/downloads/msmarco_passage/queries_small.tsv', type=str)
    parser.add_argument('--index_name', dest='index_name', default='msmarco_passage.dev.2bits', type=str)
    parser.add_argument('--k', dest='k', default=1000, type=int)
    parser.add_argument('--experiment', dest='experiment', default='msmarco_passage', type=str) # msmarco_passage or msmarco_docs

    args = parser.parse_args()

    main(args)
