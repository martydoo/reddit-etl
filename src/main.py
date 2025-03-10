import logging

from src.config.defaults import DEFAULTS
from src.core.db import db_factory
from src.core.etl import etl_factory
from src.core.transform import transformation_factory

logger = logging.getLogger(__name__)


def run_etl(
    source=DEFAULTS["source"],
    sub=DEFAULTS["sub"],
    sort_by=DEFAULTS["sort_by"],
    transformation=DEFAULTS["transformation"],
    db_file=DEFAULTS["db_file"],
):
    """
    Initiate ETL process.

    Args:
        source (str): Site to extract data from. Defaults to `reddit`.
        sub (str): SubReddit to pull from. Defaults to `all`.
        sort_by (str): Sort method for posts. Defaults to `hot`.
        transformation (str): Defines which filter to apply to extracted data.
            Defaults to `zero` transformation.
        db_file (str): Database file location.
    """
    logger.info("Starting ETL.")

    logger.info("Retrieving ETL object from factory.")
    client, pipeline = etl_factory(source)

    logger.info("Initializing database.")
    db = db_factory(db_file=db_file)

    logger.info("Running pipeline.")
    pipeline.run(
        db.managed_cursor(),
        client,
        transformation_factory(transformation),
        sub,
        sort_by,
    )

    logger.info("Pipeline completed.")
