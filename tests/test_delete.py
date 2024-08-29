from sea_query import Condition, Expr, Query

from tests.utils import assert_query


def test_delete_from_table():
    query = Query.delete().from_table("table")
    assert_query(
        query,
        'DELETE FROM "table"',
    )


def test_delete_with_and_where():
    query = Query.delete().from_table("table").and_where(Expr.column("column1").eq(1))
    assert_query(
        query,
        'DELETE FROM "table" WHERE "column1" = 1',
    )


def test_delete_with_cond_where():
    query = (
        Query.delete()
        .from_table("table")
        .cond_where(
            Condition.any()
            .add(Expr.column("column1").eq(1))
            .add(Expr.column("column2").eq("value"))
        )
    )
    assert_query(
        query,
        'DELETE FROM "table" WHERE "column1" = 1 OR "column2" = \'value\'',
    )


def test_delete_with_limit():
    query = Query.delete().from_table("table").limit(1)
    assert_query(
        query,
        'DELETE FROM "table" LIMIT 1',
    )


def test_delete_returning_all():
    query = Query.delete().from_table("table").returning_all()
    assert_query(
        query,
        'DELETE FROM "table" RETURNING *',
    )


def test_delete_returning_column():
    query = Query.delete().from_table("table").returning_column("column")
    assert_query(
        query,
        'DELETE FROM "table" RETURNING "column"',
    )
