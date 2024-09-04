from sea_query import (
    Column,
    DBEngine,
    Expr,
    ForeignKey,
    ForeignKeyAction,
    IndexCreateStatement,
    Table,
)

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

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( '
        '"id" bigserial PRIMARY KEY, '
        "\"name\" varchar(128) NOT NULL DEFAULT '', "
        '"age" integer NULL '
        ")"
    )

    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( '
        '"id" integer PRIMARY KEY AUTOINCREMENT, '
        "\"name\" varchar(128) NOT NULL DEFAULT '', "
        '"age" integer NULL '
        ")"
    )

    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( "
        "`id` bigint PRIMARY KEY AUTO_INCREMENT, "
        "`name` varchar(128) NOT NULL DEFAULT '', "
        "`age` int NULL "
        ")"
    )


def test_create_table_add_check_constraint():
    statement = (
        Table.create()
        .name("users")
        .column(Column("id").big_integer().primary_key().auto_increment())
        .column(Column("positive_int").integer().null())
        .check(Expr.column("positive_int").gte(0))
    )

    assert statement.to_string(DBEngine.Postgres) == (
        'CREATE TABLE "users" ( '
        '"id" bigserial PRIMARY KEY, '
        '"positive_int" integer NULL, '
        'CHECK ("positive_int" >= 0) '
        ")"
    )

    assert statement.to_string(DBEngine.Sqlite) == (
        'CREATE TABLE "users" ( '
        '"id" integer PRIMARY KEY AUTOINCREMENT, '
        '"positive_int" integer NULL, '
        'CHECK ("positive_int" >= 0) '
        ")"
    )

    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( "
        "`id` bigint PRIMARY KEY AUTO_INCREMENT, "
        "`positive_int` int NULL, "
        "CHECK (`positive_int` >= 0) "
        ")"
    )


# TODO: Mark mysql only
def test_create_table_add_index():
    statement = (
        Table.create()
        .name("users")
        .column(Column("id").big_integer().primary_key().auto_increment())
        .column(Column("email").string().string_len(64))
        .index(IndexCreateStatement().column("email"))
    )

    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `id` bigint PRIMARY KEY AUTO_INCREMENT, `email` varchar(64), KEY (`email`) )"
    )


def test_create_table_add_primary_key():
    statement = (
        Table.create()
        .name("users")
        .column(Column("id").big_integer().auto_increment())
        .column(Column("email").string().string_len(64))
        .primary_key(IndexCreateStatement().column("id").column("email").primary())
    )

    assert (
        statement.to_string(DBEngine.Postgres)
        == 'CREATE TABLE "users" ( "id" bigserial, "email" varchar(64), PRIMARY KEY ("id", "email") )'
    )
    assert (
        statement.to_string(DBEngine.Sqlite)
        == 'CREATE TABLE "users" ( "id" integer AUTOINCREMENT, "email" varchar(64), PRIMARY KEY ("id", "email") )'
    )

    assert statement.to_string(DBEngine.Mysql) == (
        "CREATE TABLE `users` ( `id` bigint AUTO_INCREMENT, `email` varchar(64), PRIMARY KEY (`id`, `email`) )"
    )


def test_create_table_add_foreign_key():
    statement = (
        Table.create()
        .name("profiles")
        .column(Column("id").big_integer().auto_increment().primary_key())
        .column(Column("user_id").big_integer())
        .foreign_key(
            ForeignKey.create()
            .name("fk_profile_user_id")
            .from_table("profiles")
            .from_column("user_id")
            .to_table("users")
            .to_column("id")
        )
    )

    assert (
        statement.to_string(DBEngine.Postgres)
        == 'CREATE TABLE "profiles" ( "id" bigserial PRIMARY KEY, "user_id" bigint, CONSTRAINT "fk_profile_user_id" FOREIGN KEY ("user_id") REFERENCES "users" ("id") )'
    )
    assert (
        statement.to_string(DBEngine.Sqlite)
        == 'CREATE TABLE "profiles" ( "id" integer PRIMARY KEY AUTOINCREMENT, "user_id" bigint, FOREIGN KEY ("user_id") REFERENCES "users" ("id") )'
    )
    assert (
        statement.to_string(DBEngine.Mysql)
        == "CREATE TABLE `profiles` ( `id` bigint AUTO_INCREMENT PRIMARY KEY, `user_id` bigint, CONSTRAINT `fk_profile_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) )"
    )


def test_alter_table_add_column():
    statement = (
        Table.alter()
        .table("users")
        .add_column(Column("email").string().string_len(128))
    )
    assert_query(
        statement,
        'ALTER TABLE "users" ADD COLUMN "email" varchar(128)',
    )


def test_alter_table_add_columns():
    statement = (
        Table.alter()
        .table("users")
        .add_column(Column("email").string().string_len(128))
        .add_column(Column("phone").string().string_len(16))
    )
    assert statement.to_string(DBEngine.Postgres) == (
        'ALTER TABLE "users" ADD COLUMN "email" varchar(128), ADD COLUMN "phone" varchar(16)'
    )
    # TODO: Catch sqlite does not support multiple alter options
    assert statement.to_string(DBEngine.Mysql) == (
        "ALTER TABLE `users` ADD COLUMN `email` varchar(128), ADD COLUMN `phone` varchar(16)"
    )


def test_alter_table_add_column_if_not_exists():
    statement = (
        Table.alter()
        .table("users")
        .add_column_if_not_exists(Column("email").string().string_len(128))
    )

    assert statement.to_string(DBEngine.Postgres) == (
        'ALTER TABLE "users" ADD COLUMN IF NOT EXISTS "email" varchar(128)'
    )
    assert statement.to_string(DBEngine.Sqlite) == (
        'ALTER TABLE "users" ADD COLUMN "email" varchar(128)'
    )
    assert statement.to_string(DBEngine.Mysql) == (
        "ALTER TABLE `users` ADD COLUMN IF NOT EXISTS `email` varchar(128)"
    )


def test_alter_table_modify_column():
    statement = Table.alter().table("table").modify_column(Column("created_at").date())

    assert statement.to_string(DBEngine.Postgres) == (
        'ALTER TABLE "table" ALTER COLUMN "created_at" TYPE date'
    )
    # TODO: Catch sqlite does not support modify column
    assert statement.to_string(DBEngine.Mysql) == (
        "ALTER TABLE `table` MODIFY COLUMN `created_at` date"
    )


def test_alter_table_rename_column():
    statement = Table.alter().table("table").rename_column("old_name", "new_name")
    assert_query(
        statement,
        'ALTER TABLE "table" RENAME COLUMN "old_name" TO "new_name"',
    )


def test_alter_table_drop_column():
    statement = Table.alter().table("table").drop_column("column")
    assert_query(statement, 'ALTER TABLE "table" DROP COLUMN "column"')


def test_alter_table_add_foreign_key():
    statement = (
        Table.alter()
        .table("users")
        .add_foreign_key(
            ForeignKey.create()
            .name("fk_users_id")
            .from_table("users")
            .from_column("id")
            .to_table("profiles")
            .to_column("user_id")
            .on_delete(ForeignKeyAction.Cascade)
        )
    )

    assert statement.to_string(DBEngine.Postgres) == (
        'ALTER TABLE "users" ADD CONSTRAINT "fk_users_id" FOREIGN KEY ("id") REFERENCES "profiles" ("user_id") ON DELETE CASCADE'
    )

    assert statement.to_string(DBEngine.Mysql) == (
        "ALTER TABLE `users` ADD CONSTRAINT `fk_users_id` FOREIGN KEY (`id`) REFERENCES `profiles` (`user_id`) ON DELETE CASCADE"
    )


def test_alter_table_drop_foreign_key():
    statement = Table.alter().table("users").drop_foreign_key("fk_users_id")

    assert (
        statement.to_string(DBEngine.Postgres)
        == 'ALTER TABLE "users" DROP CONSTRAINT "fk_users_id"'
    )
    assert (
        statement.to_string(DBEngine.Mysql)
        == "ALTER TABLE `users` DROP FOREIGN KEY `fk_users_id`"
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

    assert statement.to_string(DBEngine.Postgres) == 'DROP TABLE "table" RESTRICT'
    assert statement.to_string(DBEngine.Sqlite) == 'DROP TABLE "table"'
    assert statement.to_string(DBEngine.Mysql) == "DROP TABLE `table` RESTRICT"


def test_drop_table_cascade():
    statement = Table.drop().table("table").cascade()

    assert statement.to_string(DBEngine.Postgres) == 'DROP TABLE "table" CASCADE'
    assert statement.to_string(DBEngine.Sqlite) == 'DROP TABLE "table"'
    assert statement.to_string(DBEngine.Mysql) == "DROP TABLE `table` CASCADE"


def test_rename_table():
    statement = Table.rename().table("old_table", "new_table")
    assert_query(
        statement,
        'ALTER TABLE "old_table" RENAME TO "new_table"',
        mysql_expected="RENAME TABLE `old_table` TO `new_table`",
    )


def test_truncate_table():
    statement = Table.truncate().table("table")
    assert statement.to_string(DBEngine.Postgres) == 'TRUNCATE TABLE "table"'
    # TODO: Sqlite does not support TRUNCATE TABLE
    # TODO: Add test to catch the exception
    assert statement.to_string(DBEngine.Mysql) == "TRUNCATE TABLE `table`"
