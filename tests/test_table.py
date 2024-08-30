from sea_query import Column, DBEngine, Expr, Table

from tests.utils import assert_query


def test_create_table():
    statement = Table.create().name("users")
    assert_query(statement, 'CREATE TABLE "users" (  )')


def test_create_table_if_not_exists():
    statement = Table.create().name("users").if_not_exists()
    assert_query(statement, 'CREATE TABLE IF NOT EXISTS "users" (  )')


def test_create_table_with_columns():
    statement = (
        Table.create()
        .name("users")
        .column(Column("id").big_integer().primary_key().auto_increment())
        .column(
            Column("name").string().string_len(128).not_null().default(Expr.value(""))
        )
        .column(Column("age").integer().null())
    )

    assert statement.build_sql(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( '
        '"id" bigserial PRIMARY KEY, '
        "\"name\" varchar(128) NOT NULL DEFAULT '', "
        '"age" integer NULL '
        ")"
    )

    assert statement.build_sql(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( '
        '"id" integer PRIMARY KEY AUTOINCREMENT, '
        "\"name\" varchar(128) NOT NULL DEFAULT '', "
        '"age" integer NULL '
        ")"
    )

    assert statement.build_sql(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( "
        "`id` bigint PRIMARY KEY AUTO_INCREMENT, "
        "`name` varchar(128) NOT NULL DEFAULT '', "
        "`age` int NULL "
        ")"
    )


def test_drop_table():
    statement = Table.drop().table("table")
    assert_query(statement, 'DROP TABLE "table"')


def test_drop_multiple_tables():
    statement = Table.drop().table("table1").table("table2")
    assert_query(statement, 'DROP TABLE "table1", "table2"')


def test_drop_table_if_exists():
    statement = Table.drop().table("table").if_exists()
    assert_query(statement, 'DROP TABLE IF EXISTS "table"')


def test_drop_table_restrict():
    statement = Table.drop().table("table").restrict()

    assert statement.build_sql(DBEngine.Postgres) == 'DROP TABLE "table" RESTRICT'
    assert statement.build_sql(DBEngine.Sqlite) == 'DROP TABLE "table"'
    assert statement.build_sql(DBEngine.Mysql) == "DROP TABLE `table` RESTRICT"


def test_drop_table_cascade():
    statement = Table.drop().table("table").cascade()

    assert statement.build_sql(DBEngine.Postgres) == 'DROP TABLE "table" CASCADE'
    assert statement.build_sql(DBEngine.Sqlite) == 'DROP TABLE "table"'
    assert statement.build_sql(DBEngine.Mysql) == "DROP TABLE `table` CASCADE"


def test_rename_table():
    statement = Table.rename().table("old_table", "new_table")
    assert_query(
        statement,
        'ALTER TABLE "old_table" RENAME TO "new_table"',
        mysql_expected="RENAME TABLE `old_table` TO `new_table`",
    )


def test_truncate_table():
    statement = Table.truncate().table("table")
    assert statement.build_sql(DBEngine.Postgres) == 'TRUNCATE TABLE "table"'
    # TODO: Sqlite does not support TRUNCATE TABLE
    # TODO: Add test to catch the exception
    assert statement.build_sql(DBEngine.Mysql) == "TRUNCATE TABLE `table`"
