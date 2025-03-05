import os
from pathlib import Path

# Get reddit-etl folder (defaults.py > config > src > reddit-etl)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Use environment path if running with Docker, normal path otherwise
DB_PATH = Path(os.getenv("ETL_DB_PATH", PROJECT_ROOT / "data" / "reddit.db"))

DEFAULTS = {
    "source": "reddit",
    "sub": "all",
    "sort": "hot",
    "filter": "zero",
    "db_file": str(DB_PATH),
}
