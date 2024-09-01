from sea_query import DBEngine, Index, IndexType, OrderBy

from tests.utils import assert_query


def test_create_index():
    index = Index.create().name("index_name").table("table").column("col1")
    assert_query(index, 'CREATE INDEX "index_name" ON "table" ("col1")')


def test_create_index_multiple_columns():
    index = (
        Index.create().name("index_name").table("table").column("col1").column("col2")
    )
    assert_query(index, 'CREATE INDEX "index_name" ON "table" ("col1", "col2")')


def test_create_index_if_not_exists():
    index = (
        Index.create().name("index_name").table("table").column("col1").if_not_exists()
    )
    assert_query(
        index,
        'CREATE INDEX IF NOT EXISTS "index_name" ON "table" ("col1")',
        mysql_expected="CREATE INDEX `index_name` ON `table` (`col1`)",
    )


def test_create_index_with_order():
    index = Index.create().name("index_name").table("table").column("col1", OrderBy.Asc)
    assert_query(
        index,
        'CREATE INDEX "index_name" ON "table" ("col1" ASC)',
        mysql_expected="CREATE INDEX `index_name` ON `table` (`col1` ASC)",
    )


def test_create_index_columns_with_order():
    index = (
        Index.create()
        .name("index_name")
        .table("table")
        .column("col1", OrderBy.Asc)
        .column("col2", OrderBy.Desc)
    )
    assert_query(
        index,
        'CREATE INDEX "index_name" ON "table" ("col1" ASC, "col2" DESC)',
    )


def test_create_index_unique():
    index = Index.create().name("index_name").table("table").column("col1").unique()
    assert_query(
        index,
        'CREATE UNIQUE INDEX "index_name" ON "table" ("col1")',
    )


def test_create_primary_index():
    index = Index.create().name("index_name").table("table").column("col1").primary()
    assert_query(
        index,
        'CREATE PRIMARY KEY INDEX "index_name" ON "table" ("col1")',
        mysql_expected="CREATE PRIMARY INDEX `index_name` ON `table` (`col1`)",
    )


def test_create_primary_index_multiple_columns():
    index = (
        Index.create()
        .name("index_name")
        .table("table")
        .column("col1")
        .column("col2")
        .primary()
    )
    assert_query(
        index,
        'CREATE PRIMARY KEY INDEX "index_name" ON "table" ("col1", "col2")',
        mysql_expected="CREATE PRIMARY INDEX `index_name` ON `table` (`col1`, `col2`)",
    )


# TODO: Mark only for Postgres
def test_create_index_nulls_not_distinct():
    index = (
        Index.create()
        .name("index_name")
        .table("table")
        .column("col1")
        .nulls_not_distinct()
    )

    assert (
        index.build_sql(DBEngine.Postgres)
        == 'CREATE INDEX "index_name" ON "table" ("col1") NULLS NOT DISTINCT'
    )


def test_create_btree_index():
    index = (
        Index.create()
        .name("index_name")
        .table("table")
        .column("col1")
        .index_type(IndexType.BTree)
    )

    assert (
        index.build_sql(DBEngine.Postgres)
        == 'CREATE INDEX "index_name" ON "table" USING BTREE ("col1")'
    )
    assert (
        index.build_sql(DBEngine.Mysql)
        == "CREATE INDEX `index_name` ON `table` (`col1`) USING BTREE"
    )
    # TODO: not supported by SQLite


def test_create_gin_index():
    index = (
        Index.create()
        .name("index_name")
        .table("table")
        .column("col1")
        .index_type(IndexType.FullText)
    )

    assert (
        index.build_sql(DBEngine.Postgres)
        == 'CREATE INDEX "index_name" ON "table" USING GIN ("col1")'
    )
    assert (
        index.build_sql(DBEngine.Mysql)
        == "CREATE FULLTEXT INDEX `index_name` ON `table` (`col1`)"
    )


def test_create_hash_index():
    index = (
        Index.create()
        .name("index_name")
        .table("table")
        .column("col1")
        .index_type(IndexType.Hash)
    )

    assert (
        index.build_sql(DBEngine.Postgres)
        == 'CREATE INDEX "index_name" ON "table" USING HASH ("col1")'
    )
    assert (
        index.build_sql(DBEngine.Mysql)
        == "CREATE INDEX `index_name` ON `table` (`col1`) USING HASH"
    )


def test_drop_index():
    index = Index.drop().name("index_name").table("table")
    assert_query(
        index,
        'DROP INDEX "index_name"',
        mysql_expected="DROP INDEX `index_name` ON `table`",
    )


def test_drop_index_if_exists():
    index = Index.drop().name("index_name").table("table").if_exists()

    assert index.build_sql(DBEngine.Postgres) == 'DROP INDEX IF EXISTS "index_name"'
    assert index.build_sql(DBEngine.Sqlite) == 'DROP INDEX IF EXISTS "index_name"'
    # TODO: not supported by MySQL
