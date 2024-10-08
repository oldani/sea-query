import datetime as dt

from sea_query import DBEngine, Expr, Query


def test_eq():
    query = (
        Query.select().all().from_table("table").and_where(Expr.column("column").eq(1))
    )
    assert (
        query.to_string(DBEngine.Postgres) == 'SELECT * FROM "table" WHERE "column" = 1'
    )


def test_ne():
    query = (
        Query.select().all().from_table("table").and_where(Expr.column("column").ne(1))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" <> 1'
    )


def test_gt():
    query = (
        Query.select().all().from_table("table").and_where(Expr.column("column").gt(1))
    )
    assert (
        query.to_string(DBEngine.Postgres) == 'SELECT * FROM "table" WHERE "column" > 1'
    )


def test_gte():
    query = (
        Query.select().all().from_table("table").and_where(Expr.column("column").gte(1))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" >= 1'
    )


def test_lt():
    query = (
        Query.select().all().from_table("table").and_where(Expr.column("column").lt(1))
    )
    assert (
        query.to_string(DBEngine.Postgres) == 'SELECT * FROM "table" WHERE "column" < 1'
    )


def test_lte():
    query = (
        Query.select().all().from_table("table").and_where(Expr.column("column").lte(1))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" <= 1'
    )


def test_is():
    query = (
        Query.select().from_table("table").and_where(Expr.column("column").is_(True))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT  FROM "table" WHERE "column" IS TRUE'
    )


def test_is_not():
    query = (
        Query.select()
        .from_table("table")
        .and_where(Expr.column("column").is_not(False))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT  FROM "table" WHERE "column" IS NOT FALSE'
    )


def test_is_in():
    # In list
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column").is_in([1, 2, 3]))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" IN (1, 2, 3)'
    )

    # In tuple
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column").is_in((1, 2, 3)))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" IN (1, 2, 3)'
    )


def test_is_not_in():
    # Not in list
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column").is_not_in([1, 2, 3]))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" NOT IN (1, 2, 3)'
    )

    # Not in tuple
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column").is_not_in((1, 2, 3)))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" NOT IN (1, 2, 3)'
    )


def test_between():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column").between(1, 2))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" BETWEEN 1 AND 2'
    )


def test_not_between():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column").not_between(1, 2))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" NOT BETWEEN 1 AND 2'
    )


def test_like():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column").like("abc%"))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" LIKE \'abc%\''
    )


def test_not_like():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column").not_like("abc%"))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" NOT LIKE \'abc%\''
    )


def test_is_null():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column").is_null())
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" IS NULL'
    )


def test_is_not_null():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column").is_not_null())
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT * FROM "table" WHERE "column" IS NOT NULL'
    )


def test_max():
    query = Query.select().from_table("table").expr(Expr.column("column").max())
    assert query.to_string(DBEngine.Postgres) == 'SELECT MAX("column") FROM "table"'


def test_min():
    query = Query.select().from_table("table").expr(Expr.column("column").min())
    assert query.to_string(DBEngine.Postgres) == 'SELECT MIN("column") FROM "table"'


def test_sum():
    query = Query.select().from_table("table").expr(Expr.column("column").sum())
    assert query.to_string(DBEngine.Postgres) == 'SELECT SUM("column") FROM "table"'


def test_count():
    query = Query.select().from_table("table").expr(Expr.column("column").count())
    assert query.to_string(DBEngine.Postgres) == 'SELECT COUNT("column") FROM "table"'


def test_count_distinct():
    query = (
        Query.select().from_table("table").expr(Expr.column("column").count_distinct())
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT COUNT(DISTINCT "column") FROM "table"'
    )


def test_if_null():
    query = Query.select().from_table("table").expr(Expr.column("column").if_null(1))
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT COALESCE("column", 1) FROM "table"'
    )


def test_exists():
    query = (
        Query.select()
        .from_table("table")
        .expr(
            Expr.exists(
                Query.select()
                .column("column")
                .from_table("table")
                .and_where(Expr.column("column").eq(1))
            )
        )
    )
    assert query.to_string(DBEngine.Postgres) == (
        'SELECT EXISTS(SELECT "column" FROM "table" WHERE "column" = 1) FROM "table"'
    )


def test_pyvalue_int():
    query = Query.select().from_table("table").and_where(Expr.column("column").eq(1))
    assert (
        query.to_string(DBEngine.Postgres) == 'SELECT  FROM "table" WHERE "column" = 1'
    )


def test_pyvalue_float():
    query = Query.select().from_table("table").and_where(Expr.column("column").eq(1.5))
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT  FROM "table" WHERE "column" = 1.5'
    )


def test_pyvalue_str():
    query = (
        Query.select().from_table("table").and_where(Expr.column("column").eq("abc"))
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT  FROM "table" WHERE "column" = \'abc\''
    )


def test_pyvalue_bool():
    query = Query.select().from_table("table").and_where(Expr.column("column").eq(True))
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT  FROM "table" WHERE "column" = TRUE'
    )


def test_pyvalue_date():
    query = (
        Query.select()
        .from_table("table")
        .and_where(Expr.column("column").eq(dt.date(2024, 9, 12)))
    )

    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT  FROM "table" WHERE "column" = \'2024-09-12\''
    )


def test_pyvalue_time():
    query = (
        Query.select()
        .from_table("table")
        .and_where(Expr.column("column").eq(dt.time(12, 30, 00)))
    )

    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT  FROM "table" WHERE "column" = \'12:30:00\''
    )


def test_pyvalue_datetime():
    query = (
        Query.select()
        .from_table("table")
        .and_where(Expr.column("column").eq(dt.datetime(2024, 9, 12, 12, 30, 00)))
    )

    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT  FROM "table" WHERE "column" = \'2024-09-12 12:30:00\''
    )


def test_pyvalue_datetime_with_tz():
    query = (
        Query.select()
        .from_table("table")
        .and_where(
            Expr.column("column").eq(
                dt.datetime(2024, 9, 12, 12, 30, 00, tzinfo=dt.timezone.utc)
            )
        )
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT  FROM "table" WHERE "column" = \'2024-09-12 12:30:00 +00:00\''
    )

    query = (
        Query.select()
        .from_table("table")
        .and_where(
            Expr.column("column").eq(
                dt.datetime(
                    2024, 9, 12, 12, 30, 00, tzinfo=dt.timezone(dt.timedelta(hours=5))
                )
            )
        )
    )
    assert (
        query.to_string(DBEngine.Postgres)
        == 'SELECT  FROM "table" WHERE "column" = \'2024-09-12 12:30:00 +05:00\''
    )
