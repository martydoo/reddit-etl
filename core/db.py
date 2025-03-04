import sqlite3
from contextlib import contextmanager


class DatabaseConnection:
    """Class to connect to a database."""

    def __init__(self, db_type="sqlite3", db_file="reddit.db"):
        """
        Initializes database connection object.

        Args:
            db_type (str): Database to use. Defaults to SQLite3.
            db_file (str): File to contain database. Defaults to 'reddit.db'.
        """
        self._db_type = db_type
        self._db_file = db_file

    @contextmanager
    def managed_cursor(self):
        """
        Create a managed database cursor object.

        Yields:
            sqlite3.Cursor: SQLite3 cursor to execute on database.
        """
        if self._db_type == "sqlite3":
            _con = sqlite3.connect(self._db_file)
            cur = _con.cursor()
            try:
                yield cur
            finally:
                _con.commit()
                cur.close()
                _con.close()


def db_factory(db_type=None, db_file=None):
    """
    Create a database connection object.

    Args:
        db_type (str): Database to use. Defaults to SQLite3.
        db_file (str): File to contain database. Defaults to 'reddit.db'.

    Returns:
        DatabaseConnection: Database connection object.
    """
    kwargs = {}
    if db_type is not None:
        kwargs["db_type"] = db_type
    if db_file is not None:
        kwargs["db_file"] = db_file

    return DatabaseConnection(**kwargs)
