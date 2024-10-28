import re
from typing import Any, Optional

from sea_query import DBEngine


def assert_query(
    query: Any,
    expected: str,
    mysql_expected: Optional[str] = None,
) -> None:
    for engine in [DBEngine.Postgres, DBEngine.Sqlite, DBEngine.Mysql]:
        if engine == DBEngine.Mysql:
            expected = mysql_expected or expected.replace('"', "`")

        assert (
            query.to_string(engine) == expected
        ), f"{query.to_string(engine)} != {expected}"


def format_mysql(expected: str) -> str:
    return re.sub(r"\$\d+", "?", expected.replace('"', "`"))


def format_sqlite(expected: str) -> str:
    return re.sub(r"\$\d+", "?", expected)
