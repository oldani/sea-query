from typing import Union

from sea_query import (
    DBEngine,
    DeleteStatement,
    InsertStatement,
    SelectStatement,
    UpdateStatement,
)


def assert_query(
    query: Union[SelectStatement, UpdateStatement, DeleteStatement, InsertStatement],
    expected: str,
    mysql_expected: str = None,
):
    assert query.build_sql(DBEngine.Postgres) == expected
    assert query.build_sql(DBEngine.Sqlite) == expected
    assert query.build_sql(DBEngine.Mysql) == mysql_expected or expected.replace(
        '"', "`"
    )
