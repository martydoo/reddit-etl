import logging

from config.defaults import DEFAULTS
from core.db import db_factory
from core.etl import etl_factory
from core.transform import transformation_factory

logger = logging.getLogger(__name__)


def run_etl(
    source=DEFAULTS["source"],
    sub=DEFAULTS["sub"],
    sort_by=DEFAULTS["sort"],
    transformation=DEFAULTS["filter"],
    db=None,
):
    """
    Initiate ETL process.

    Args:
        source (str): Site to extract data from. Defaults to `reddit`.
        sub (str): SubReddit to pull from. Defaults to `all`.
        sort_by (str): Sort method for posts. Defaults to `hot`.
        transformation (str): Defines which filter to apply to extracted data.
            Defaults to `zero` transformation.
        db (DatabaseConnection): Database connection object.
    """
    logger.info("Starting ETL.")

    logger.info("Retrieving ETL object from factory.")
    client, pipeline = etl_factory(source)

    logger.info("Initializing database.")
    if db is None:
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
