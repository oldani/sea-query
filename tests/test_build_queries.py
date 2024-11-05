import datetime as dt

from sea_query import DBEngine, Expr, Query
from sea_query.expr import Condition

from tests.utils import format_mysql, format_sqlite


def test_select_query_build():
    query = (
        Query.select().all().from_table("table").and_where(Expr.column("column").eq(1))
    )

    sql = 'SELECT * FROM "table" WHERE "column" = $1'
    assert query.build(DBEngine.Postgres) == (sql, [1])

    assert query.build(DBEngine.Mysql) == (format_mysql(sql), [1])

    assert query.build(DBEngine.Sqlite) == (format_sqlite(sql), [1])


def test_select_query_build_many_values():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .cond_where(
            Condition.any()
            .add(Expr.column("col1").eq(1))
            .add(Expr.column("col2").gt(2.7))
            .add(Expr.column("col3").is_in([3, 4.35, 5]))
            .add(Expr.column("col4").ne("test@email.com"))
            .add(Expr.column("col5").is_(True))
            .add(Expr.column("col6").is_(None))
        )
    )

    assert query.build(DBEngine.Postgres) == (
        'SELECT * FROM "table" WHERE "col1" = $1 OR "col2" > $2 OR "col3" IN ($3, $4, $5) OR "col4" <> $6 OR "col5" IS $7 OR "col6" IS $8',
        [1, 2.7, 3, 4.35, 5, "test@email.com", True, None],
    )


def test_select_with_limit():
    query = Query.select().all().from_table("table").limit(10)
    sql = 'SELECT * FROM "table" LIMIT $1'

    assert query.build(DBEngine.Postgres) == (sql, [10])
    assert query.build(DBEngine.Mysql) == (format_mysql(sql), [10])
    assert query.build(DBEngine.Sqlite) == (format_sqlite(sql), [10])


def test_select_with_limit_and_offset():
    query = Query.select().all().from_table("table").limit(10).offset(5)
    sql = 'SELECT * FROM "table" LIMIT $1 OFFSET $2'

    assert query.build(DBEngine.Postgres) == (sql, [10, 5])
    assert query.build(DBEngine.Mysql) == (format_mysql(sql), [10, 5])
    assert query.build(DBEngine.Sqlite) == (format_sqlite(sql), [10, 5])


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
            [
                "boo",
                "int",
                "float",
                "str",
                "time",
                "date",
                "datetime",
                "datetime_tz",
                "none",
            ]
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
                None,
            ]
        )
    )

    assert query.build(DBEngine.Postgres) == (
        'INSERT INTO "table" ("boo", "int", "float", "str", "time", "date", "datetime", "datetime_tz", "none") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
        [
            True,
            1,
            1.5,
            "string",
            dt.time(12, 30, 00),
            dt.date(2024, 9, 12),
            dt.datetime(2024, 9, 12, 12, 30, 00),
            dt.datetime(2024, 9, 12, 12, 30, 00, tzinfo=dt.timezone.utc),
            None,
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
