import argparse
import logging

from reddit import etl_factory
from transform import transformation_factory
from db import db_factory

logger = logging.getLogger(__name__)

def main(source='reddit', sub='all', transformation='none'):
    """
    Initiate ETL process.

    Args:
        source (str): Site to extract data from. Defaults to Reddit.
        sub (str): SubReddit to pull from.
        transformation (str): Defines which filter to apply to extracted data.
    """
    logging.basicConfig(filename='etl.log', level=logging.INFO)
    logger.info("Starting ETL.")
    logger.info("Retrieving ETL object from factory.")


if __name__ == '__main__':
    main(args.source, args.sub, args.filter)
