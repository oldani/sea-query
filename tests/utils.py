from typing import Any, Optional

from sea_query import (
    DBEngine,
)


def assert_query(
    query: Any,
    expected: str,
    mysql_expected: Optional[str] = None,
):
    assert (
        query.build_sql(DBEngine.Postgres) == expected
    ), f"{query.build_sql(DBEngine.Postgres)} != {expected}"
    assert (
        query.build_sql(DBEngine.Sqlite) == expected
    ), f"{query.build_sql(DBEngine.Sqlite)} != {expected}"
    assert (
        query.build_sql(DBEngine.Mysql)
        == (mysql_expected or expected.replace('"', "`"))
    ), f"{query.build_sql(DBEngine.Mysql)} != {mysql_expected or expected.replace('\"', '`')}"
