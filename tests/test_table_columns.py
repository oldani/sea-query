from sea_query import DBEngine, Expr, Table
from sea_query.table import Column, ColumnType

from tests.utils import assert_query


def test_char_col():
    statement = Table.create().name("users").column(Column("name").char())
    assert_query(statement, 'CREATE TABLE "users" ( "name" char )')


def test_char_col_len():
    statement = Table.create().name("users").column(Column("name").char_len(128))
    assert_query(statement, 'CREATE TABLE "users" ( "name" char(128) )')


def test_string_col():
    statement = Table.create().name("users").column(Column("name").string())
    assert_query(
        statement,
        'CREATE TABLE "users" ( "name" varchar )',
        mysql_expected="CREATE TABLE `users` ( `name` varchar(255) )",
    )


def test_string_col_len():
    statement = Table.create().name("users").column(Column("name").string_len(128))
    assert_query(statement, 'CREATE TABLE "users" ( "name" varchar(128) )')


def test_text_col():
    statement = Table.create().name("users").column(Column("description").text())
    assert_query(statement, 'CREATE TABLE "users" ( "description" text )')


def test_tiny_integer_col():
    statement = Table.create().name("users").column(Column("age").tiny_integer())

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "age" smallint )'
    )

    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "age" tinyint )'
    )

    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `age` tinyint )"
    )


def test_small_integer_col():
    statement = Table.create().name("users").column(Column("age").small_integer())
    assert_query(statement, 'CREATE TABLE "users" ( "age" smallint )')


def test_integer_col():
    statement = Table.create().name("users").column(Column("age").integer())
    assert_query(
        statement,
        'CREATE TABLE "users" ( "age" integer )',
        mysql_expected="CREATE TABLE `users` ( `age` int )",
    )


def test_big_integer_col():
    statement = Table.create().name("users").column(Column("age").big_integer())
    assert_query(statement, 'CREATE TABLE "users" ( "age" bigint )')


def test_tiny_unsigned_col():
    statement = Table.create().name("users").column(Column("age").tiny_unsigned())

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "age" smallint )'
    )

    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "age" tinyint )'
    )

    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `age` tinyint UNSIGNED )"
    )


def test_small_unsigned_col():
    statement = Table.create().name("users").column(Column("age").small_unsigned())
    assert_query(
        statement,
        'CREATE TABLE "users" ( "age" smallint )',
        mysql_expected="CREATE TABLE `users` ( `age` smallint UNSIGNED )",
    )


def test_unsigned_col():
    statement = Table.create().name("users").column(Column("age").unsigned())
    assert_query(
        statement,
        'CREATE TABLE "users" ( "age" integer )',
        mysql_expected="CREATE TABLE `users` ( `age` int UNSIGNED )",
    )


def test_big_unsigned_col():
    statement = Table.create().name("users").column(Column("age").big_unsigned())
    assert_query(
        statement,
        'CREATE TABLE "users" ( "age" bigint )',
        mysql_expected="CREATE TABLE `users` ( `age` bigint UNSIGNED )",
    )


def test_float_col():
    statement = Table.create().name("users").column(Column("amount").float())
    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "amount" real )'
    )
    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "amount" float )'
    )
    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `amount` float )"
    )


def test_double_col():
    statement = Table.create().name("users").column(Column("amount").double())
    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "amount" double precision )'
    )
    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "amount" double )'
    )
    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `amount` double )"
    )


def test_decimal_col():
    statement = Table.create().name("users").column(Column("amount").decimal())
    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "amount" decimal )'
    )
    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "amount" real )'
    )
    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `amount` decimal )"
    )


def test_decimal_col_len():
    statement = Table.create().name("users").column(Column("amount").decimal_len(10, 2))
    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "amount" decimal(10, 2) )'
    )
    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "amount" real(10, 2) )'
    )
    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `amount` decimal(10, 2) )"
    )


def test_datetime_col():
    statement = Table.create().name("users").column(Column("created_at").datetime())

    assert (
        statement.to_string(DBEngine.Postgres)
        == 'CREATE TABLE "users" ( "created_at" timestamp without time zone )'
    )
    assert (
        statement.to_string(DBEngine.Sqlite)
        == 'CREATE TABLE "users" ( "created_at" datetime_text )'
    )
    assert (
        statement.to_string(DBEngine.Mysql)
        == "CREATE TABLE `users` ( `created_at` datetime )"
    )


def test_timestamp_col():
    statement = Table.create().name("users").column(Column("created_at").timestamp())

    assert (
        statement.to_string(DBEngine.Postgres)
        == 'CREATE TABLE "users" ( "created_at" timestamp )'
    )
    assert (
        statement.to_string(DBEngine.Sqlite)
        == 'CREATE TABLE "users" ( "created_at" timestamp_text )'
    )
    assert (
        statement.to_string(DBEngine.Mysql)
        == "CREATE TABLE `users` ( `created_at` timestamp )"
    )


def test_timestamp_col_with_tz():
    statement = (
        Table.create().name("users").column(Column("created_at").timestamp_with_tz())
    )

    assert (
        statement.to_string(DBEngine.Postgres)
        == 'CREATE TABLE "users" ( "created_at" timestamp with time zone )'
    )
    assert (
        statement.to_string(DBEngine.Sqlite)
        == 'CREATE TABLE "users" ( "created_at" timestamp_with_timezone_text )'
    )
    assert (
        statement.to_string(DBEngine.Mysql)
        == "CREATE TABLE `users` ( `created_at` timestamp )"
    )


def test_date_col():
    statement = Table.create().name("users").column(Column("dob").date())

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "dob" date )'
    )
    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "dob" date_text )'
    )
    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `dob` date )"
    )


def test_time_col():
    statement = Table.create().name("users").column(Column("time").time())

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "time" time )'
    )
    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "time" time_text )'
    )
    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `time` time )"
    )


def test_blob_col():
    statement = Table.create().name("users").column(Column("data").blob())

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "data" bytea )'
    )
    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "data" blob )'
    )
    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `data` blob )"
    )


def test_boolean_col():
    statement = Table.create().name("users").column(Column("active").boolean())

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "active" bool )'
    )
    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "active" boolean )'
    )
    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `active` bool )"
    )


def test_json_col():
    statement = Table.create().name("users").column(Column("data").json())

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "data" json )'
    )
    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "data" json_text )'
    )
    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `data` json )"
    )


def test_jsonb_col():
    statement = Table.create().name("users").column(Column("data").jsonb())

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "data" jsonb )'
    )
    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "data" jsonb_text )'
    )
    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `data` json )"
    )


def test_uuid_col():
    statement = Table.create().name("users").column(Column("id").uuid())

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "id" uuid )'
    )
    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "id" uuid_text )'
    )
    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `id` binary(16) )"
    )


def test_new_column_with_type():
    statement = (
        Table.create()
        .name("users")
        .column(Column.new_with_type("name", ColumnType.String))
    )

    assert_query(
        statement,
        'CREATE TABLE "users" ( "name" varchar )',
        mysql_expected="CREATE TABLE `users` ( `name` varchar(255) )",
    )


def test_column_check():
    statement = (
        Table.create()
        .name("users")
        .column(Column("age").integer().check(Expr.column("age").gt(0)))
    )

    assert_query(
        statement,
        'CREATE TABLE "users" ( "age" integer CHECK ("age" > 0) )',
        mysql_expected="CREATE TABLE `users` ( `age` int CHECK (`age` > 0) )",
    )


def test_column_comment():
    statement = (
        Table.create().name("users").column(Column("id").uuid().comment("User uuid"))
    )

    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `id` binary(16) COMMENT 'User uuid' )"
    )


def test_col_not_null():
    statement = Table.create().name("users").column(Column("name").string().not_null())
    assert_query(
        statement,
        'CREATE TABLE "users" ( "name" varchar NOT NULL )',
        mysql_expected="CREATE TABLE `users` ( `name` varchar(255) NOT NULL )",
    )


def test_col_nullable():
    statement = Table.create().name("users").column(Column("name").string().null())
    assert_query(
        statement,
        'CREATE TABLE "users" ( "name" varchar NULL )',
        mysql_expected="CREATE TABLE `users` ( `name` varchar(255) NULL )",
    )


def test_col_unique():
    statement = (
        Table.create()
        .name("users")
        .column(Column("id").big_integer().unique())
        .column(Column("email").string().unique())
    )
    assert_query(
        statement,
        'CREATE TABLE "users" ( "id" bigint UNIQUE, "email" varchar UNIQUE )',
        mysql_expected="CREATE TABLE `users` ( `id` bigint UNIQUE, `email` varchar(255) UNIQUE )",
    )


def test_col_primary_key():
    statement = (
        Table.create().name("users").column(Column("id").big_integer().primary_key())
    )
    assert_query(statement, 'CREATE TABLE "users" ( "id" bigint PRIMARY KEY )')


def test_col_auto_increment():
    statement = (
        Table.create()
        .name("users")
        .column(Column("id").big_integer().primary_key().auto_increment())
    )

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "id" bigserial PRIMARY KEY )'
    )

    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( "id" integer PRIMARY KEY AUTOINCREMENT )'
    )

    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `id` bigint PRIMARY KEY AUTO_INCREMENT )"
    )

    statement = (
        Table.create()
        .name("users")
        .column(Column("id").small_integer().auto_increment())
    )

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( "id" smallserial )'
    )

    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `id` smallint AUTO_INCREMENT )"
    )
