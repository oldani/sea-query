from sea_query import Condition, Expr, Query

from tests.utils import assert_query


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
        mysql_expected="UPDATE `table` SET `column1` = 1",
    )


def test_update_returning_column():
    query = (
        Query.update().table("table").value("column1", 1).returning_column("column1")
    )
    assert_query(
        query,
        'UPDATE "table" SET "column1" = 1 RETURNING "column1"',
        mysql_expected="UPDATE `table` SET `column1` = 1",
    )
