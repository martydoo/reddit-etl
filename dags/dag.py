from airflow.decorators import dag, task
from datetime import datetime, timedelta
from ..main import run_etl
from ..core.db import db_factory
from ..config.defaults import DEFAULTS

default_args = {
    "start_date": datetime(2025, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


@dag(
    "reddit-etl",
    description="ETL pipeline for Reddit posts. Automatically backs up database.",
    schedule_interval=timedelta(days=1),
    catchup=False,
    default_args=default_args,
    params=DEFAULTS,
)
def reddit_etl():
    @task
    def execute_etl(**context):
        db = db_factory(db_file=DEFAULTS["db_file"])
        run_etl(db=db, **context["params"])

    @task.bash
    def generate_csv():
        return f"""
            chmod +x {DEFAULTS["db_file"].replace("reddit.db", "")} && \
            DB_PATH={DEFAULTS["db_file"]} && \
            {DEFAULTS["db_file"].replace("reddit.db", "generate_csv.sh")}
        """

    execute_etl() >> generate_csv()  # type: ignore


reddit_etl_dag = reddit_etl()
