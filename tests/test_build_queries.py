import datetime as dt

from sea_query import DBEngine, Expr, Query
from sea_query.expr import Condition


def test_select_query_build():
    query = (
        Query.select().all().from_table("table").and_where(Expr.column("column").eq(1))
    )

    assert query.build(DBEngine.Postgres) == (
        'SELECT * FROM "table" WHERE "column" = $1',
        [1],
    )

    assert query.build(DBEngine.Mysql) == (
        "SELECT * FROM `table` WHERE `column` = ?",
        [1],
    )

    assert query.build(DBEngine.Sqlite) == (
        'SELECT * FROM "table" WHERE "column" = ?',
        [1],
    )


def test_select_query_build_many_values():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .cond_where(
            Condition.any()
            .add(Expr.column("column1").eq(1))
            .add(Expr.column("column2").gt(2.7))
            .add(Expr.column("column3").is_in([3, 4.35, 5]))
            .add(Expr.column("email").ne("test@email.com"))
            .add(Expr.column("is_active").is_(True))
        )
    )

    assert query.build(DBEngine.Postgres) == (
        'SELECT * FROM "table" WHERE "column1" = $1 OR "column2" > $2 OR "column3" IN ($3, $4, $5) OR "email" <> $6 OR "is_active" IS $7',
        [1, 2.7, 3, 4.35, 5, "test@email.com", True],
    )


def test_insert_query_build():
    query = (
        Query.insert()
        .into("table")
        .columns(["column1", "column2"])
        .values([1, "value"])
    )

    assert query.build(DBEngine.Postgres) == (
        'INSERT INTO "table" ("column1", "column2") VALUES ($1, $2)',
        [1, "value"],
    )

    assert query.build(DBEngine.Mysql) == (
        "INSERT INTO `table` (`column1`, `column2`) VALUES (?, ?)",
        [1, "value"],
    )

    assert query.build(DBEngine.Sqlite) == (
        'INSERT INTO "table" ("column1", "column2") VALUES (?, ?)',
        [1, "value"],
    )


def test_bulk_insert_query_build():
    query = (
        Query.insert()
        .into("table")
        .columns(["col1", "col2", "col3"])
        .values([1, "val1", 1000])
        .values([2, "val2", 2000])
        .values([3, "val3", 3000])
        .values([4, "val4", 4000])
    )

    assert query.build(DBEngine.Postgres) == (
        'INSERT INTO "table" ("col1", "col2", "col3") VALUES ($1, $2, $3), ($4, $5, $6), ($7, $8, $9), ($10, $11, $12)',
        [1, "val1", 1000, 2, "val2", 2000, 3, "val3", 3000, 4, "val4", 4000],
    )

    assert query.build(DBEngine.Mysql) == (
        "INSERT INTO `table` (`col1`, `col2`, `col3`) VALUES (?, ?, ?), (?, ?, ?), (?, ?, ?), (?, ?, ?)",
        [1, "val1", 1000, 2, "val2", 2000, 3, "val3", 3000, 4, "val4", 4000],
    )

    assert query.build(DBEngine.Sqlite) == (
        'INSERT INTO "table" ("col1", "col2", "col3") VALUES (?, ?, ?), (?, ?, ?), (?, ?, ?), (?, ?, ?)',
        [1, "val1", 1000, 2, "val2", 2000, 3, "val3", 3000, 4, "val4", 4000],
    )


def test_insert_build_with_diff_types():
    query = (
        Query.insert()
        .into("table")
        .columns(
            ["boo", "int", "float", "str", "time", "date", "datetime", "datetime_tz"]
        )
        .values(
            [
                True,
                1,
                1.5,
                "string",
                dt.time(12, 30, 00),
                dt.date(2024, 9, 12),
                dt.datetime(2024, 9, 12, 12, 30, 00),
                dt.datetime(2024, 9, 12, 12, 30, 00, tzinfo=dt.timezone.utc),
            ]
        )
    )

    assert query.build(DBEngine.Postgres) == (
        'INSERT INTO "table" ("boo", "int", "float", "str", "time", "date", "datetime", "datetime_tz") VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        [
            True,
            1,
            1.5,
            "string",
            dt.time(12, 30, 00),
            dt.date(2024, 9, 12),
            dt.datetime(2024, 9, 12, 12, 30, 00),
            dt.datetime(2024, 9, 12, 12, 30, 00, tzinfo=dt.timezone.utc),
        ],
    )


def test_update_query_build():
    query = (
        Query.update()
        .table("table")
        .value("column1", 1)
        .value("column2", "value")
        .and_where(Expr.column("column3").eq(3))
    )

    assert query.build(DBEngine.Postgres) == (
        'UPDATE "table" SET "column1" = $1, "column2" = $2 WHERE "column3" = $3',
        [1, "value", 3],
    )

    assert query.build(DBEngine.Mysql) == (
        "UPDATE `table` SET `column1` = ?, `column2` = ? WHERE `column3` = ?",
        [1, "value", 3],
    )

    assert query.build(DBEngine.Sqlite) == (
        'UPDATE "table" SET "column1" = ?, "column2" = ? WHERE "column3" = ?',
        [1, "value", 3],
    )


def test_delete_query_build():
    query = Query.delete().from_table("table").and_where(Expr.column("column").eq(1))

    assert query.build(DBEngine.Postgres) == (
        'DELETE FROM "table" WHERE "column" = $1',
        [1],
    )

    assert query.build(DBEngine.Mysql) == (
        "DELETE FROM `table` WHERE `column` = ?",
        [1],
    )

    assert query.build(DBEngine.Sqlite) == (
        'DELETE FROM "table" WHERE "column" = ?',
        [1],
    )
