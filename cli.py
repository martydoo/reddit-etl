import argparse
import logging

from src.config.defaults import DEFAULTS
from src.main import run_etl

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        choices=["reddit"],
        default=DEFAULTS["source"],
        type=str,
        help="Site to extract data from. Currently only supports `reddit`.",
    )
    parser.add_argument(
        "--sub",
        default=DEFAULTS["sub"],
        type=str,
        help="SubReddit to pull from. Defaults to `all`.",
    )
    parser.add_argument(
        "--sort",
        choices=["hot", "new", "top"],
        default=DEFAULTS["sort_by"],
        type=str,
        help="Sort method for posts. Defaults to `hot`.",
    )
    parser.add_argument(
        "--filter",
        choices=["zero", "random", "discussion", "popular"],
        default=DEFAULTS["transformation"],
        type=str,
        help="Filter to apply to extracted data. Defaults to `zero`.",
    )

    args = parser.parse_args()
    logging.basicConfig(
        filename="etl.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )

    run_etl(args.source, args.sub, args.sort, args.filter)
