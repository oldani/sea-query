from sea_query import Condition, DBEngine, Expr, Query, UpdateStatement


def assert_query(
    query: UpdateStatement,
    expected: str,
    mysql_expected: str = None,
):
    assert query.build_sql(DBEngine.Postgres) == expected
    assert query.build_sql(DBEngine.Sqlite) == expected
    assert query.build_sql(DBEngine.Mysql) == mysql_expected or expected.replace(
        '"', "`"
    )


def test_update_table():
    query = Query.update().table("table").value("column1", 1).value("column2", "value")
    assert_query(
        query,
        'UPDATE "table" SET "column1" = 1, "column2" = \'value\'',
    )


def test_update_values():
    query = Query.update().table("table").values([("column1", 1), ("column2", "value")])
    assert_query(
        query,
        'UPDATE "table" SET "column1" = 1, "column2" = \'value\'',
    )


def test_update_with_and_where():
    query = (
        Query.update()
        .table("table")
        .value("column1", 1)
        .and_where(Expr.column("column2").eq("value"))
    )
    assert_query(
        query,
        'UPDATE "table" SET "column1" = 1 WHERE "column2" = \'value\'',
    )


def test_update_with_cond_where():
    query = (
        Query.update()
        .table("table")
        .value("column1", 1)
        .cond_where(
            Condition.any()
            .add(Expr.column("column2").eq("value"))
            .add(Expr.column("column3").eq(3))
        )
    )
    assert_query(
        query,
        'UPDATE "table" SET "column1" = 1 WHERE "column2" = \'value\' OR "column3" = 3',
    )


def test_update_with_limit():
    query = Query.update().table("table").value("column1", 1).limit(1)
    assert_query(
        query,
        'UPDATE "table" SET "column1" = 1 LIMIT 1',
    )


def test_update_returning_all():
    query = Query.update().table("table").value("column1", 1).returning_all()
    assert_query(
        query,
        'UPDATE "table" SET "column1" = 1 RETURNING *',
    )


def test_update_returning_column():
    query = (
        Query.update().table("table").value("column1", 1).returning_column("column1")
    )
    assert_query(
        query,
        'UPDATE "table" SET "column1" = 1 RETURNING "column1"',
    )
