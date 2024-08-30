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


def test_truncate_table():
    statement = Table.truncate().table("table")
    assert statement.build_sql(DBEngine.Postgres) == 'TRUNCATE TABLE "table"'
    # TODO: Sqlite does not support TRUNCATE TABLE
    # TODO: Add test to catch the exception
    assert statement.build_sql(DBEngine.Mysql) == "TRUNCATE TABLE `table`"
