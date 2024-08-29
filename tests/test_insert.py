from sea_query import OnConflict, Query

from tests.utils import assert_query


def test_insert_into():
    query = (
        Query.insert()
        .into("table")
        .columns(["column1", "column2"])
        .values([1, "value"])
    )
    assert_query(
        query, 'INSERT INTO "table" ("column1", "column2") VALUES (1, \'value\')'
    )


def test_select_from():
    query = (
        Query.insert()
        .into("table")
        .columns(["column1", "column2"])
        .select_from(
            Query.select().from_table("table2").columns(["column3", "column4"])
        )
    )

    assert_query(
        query,
        'INSERT INTO "table" ("column1", "column2") SELECT "column3", "column4" FROM "table2"',
    )


def test_on_conflict_do_nothing():
    query = (
        Query.insert()
        .into("table")
        .columns(["column1", "column2"])
        .values([1, 3.5])
        .on_conflict(OnConflict.column("column1").do_nothing())
    )

    assert_query(
        query,
        'INSERT INTO "table" ("column1", "column2") VALUES (1, 3.5) ON CONFLICT ("column1") DO NOTHING',
        mysql_expected="INSERT INTO `table` (`column1`, `column2`) VALUES (1, 3.5) ON DUPLICATE KEY IGNORE",
    )


def test_returning_all():
    query = (
        Query.insert()
        .into("table")
        .columns(["column1", "column2"])
        .values([1, 3.5])
        .returning_all()
    )

    assert_query(
        query,
        'INSERT INTO "table" ("column1", "column2") VALUES (1, 3.5) RETURNING *',
    )


def test_insert_returning_column():
    query = (
        Query.insert()
        .into("table")
        .columns(["column1", "column2"])
        .values([1, 3.5])
        .returning_column("column1")
    )

    assert_query(
        query,
        'INSERT INTO "table" ("column1", "column2") VALUES (1, 3.5) RETURNING "column1"',
    )
