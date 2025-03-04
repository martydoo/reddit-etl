import argparse
import logging

from core.db import db_factory
from core.etl import etl_factory
from core.transform import transformation_factory

logger = logging.getLogger(__name__)


def main(source, sub, sort_by, transformation):
    """
    Initiate ETL process.

    Args:
        source (str): Site to extract data from. Defaults to `reddit`.
        sub (str): SubReddit to pull from. Defaults to `all`.
        sort_by (str): Sort method for posts. Defaults to `hot`.
        transformation (str): Defines which filter to apply to extracted data.
            Defaults to `zero` transformation.
    """
    logger.info("Starting ETL.")

    logger.info("Retrieving ETL object from factory.")
    client, pipeline = etl_factory(source)

    logger.info("Initializing database.")
    db = db_factory()

    logger.info("Running pipeline.")
    pipeline.run(
        db.managed_cursor(),
        client,
        transformation_factory(transformation),
        sub,
        sort_by,
    )

    logger.info("Pipeline completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        choices=["reddit"],
        default="reddit",
        type=str,
        help="Site to extract data from. Currently only supports `reddit`.",
    )
    parser.add_argument(
        "--sub",
        default="all",
        type=str,
        help="SubReddit to pull from. Defaults to `all`.",
    )
    parser.add_argument(
        "--sort",
        choices=["hot", "new", "top"],
        default="hot",
        type=str,
        help="Sort method for posts. Defaults to `hot`.",
    )
    parser.add_argument(
        "--filter",
        choices=["zero", "random", "discussion", "popular"],
        default="zero",
        type=str,
        help="Filter to apply to extracted data. Defaults to `zero`.",
    )

    args = parser.parse_args()
    logging.basicConfig(
        filename="etl.log", 
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO)

    main(args.source, args.sub, args.sort, args.filter)
