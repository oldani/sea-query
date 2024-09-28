from typing import List, Tuple, Union

from sea_query import Expr
from sea_query.mysql import (
    ForeignKey as MysqlForeignKey,
    Index as MysqlIndex,
    Query as MysqlQuery,
    Table as MysqlTable,
)
from sea_query.postgres import (
    ForeignKey as PostgresForeignKey,
    Index as PostgresIndex,
    Query as PostgresQuery,
    Table as PostgresTable,
)
from sea_query.sqlite import (
    Index as SqliteIndex,
    Query as SqliteQuery,
    Table as SqliteTable,
)
from sea_query.table import Column


def test_select_query():
    builders: List[Tuple[Union[SqliteQuery, PostgresQuery], str]] = [
        (SqliteQuery(), "?"),
        (PostgresQuery(), "$1"),
    ]
    for builder, _ in builders:
        assert (
            builder.select().all().from_table("table").to_string()
            == 'SELECT * FROM "table"'
        )

    assert (
        MysqlQuery().select().all().from_table("table").to_string()
        == "SELECT * FROM `table`"
    )

    for builder, placeholder in builders:
        query = (
            builder.select()
            .all()
            .from_table("table")
            .and_where(Expr.column("id").eq(1))
            .build()
        )
        assert query == (f'SELECT * FROM "table" WHERE "id" = {placeholder}', [1])

    assert (
        MysqlQuery.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("id").eq(1))
        .build()
    ) == ("SELECT * FROM `table` WHERE `id` = ?", [1])


def test_update_query():
    builders: List[Tuple[Union[SqliteQuery, PostgresQuery], str]] = [
        (SqliteQuery(), "?"),
        (PostgresQuery(), "$1"),
    ]
    for builder, _ in builders:
        assert (
            builder.update().table("table").value("id", 1).to_string()
            == 'UPDATE "table" SET "id" = 1'
        )

    assert (
        MysqlQuery().update().table("table").value("column", 1).to_string()
        == "UPDATE `table` SET `column` = 1"
    )

    for builder, placeholder in builders:
        query = (
            builder.update()
            .table("table")
            .value("id", 2)
            .and_where(Expr.column("id").eq(1))
            .build()
        )
        assert query == (
            f'UPDATE "table" SET "id" = {placeholder} WHERE "id" = {placeholder.replace("1", "2")}',
            [2, 1],
        )

    assert (
        MysqlQuery()
        .update()
        .table("table")
        .value("id", 2)
        .and_where(Expr.column("id").eq(1))
        .build()
    ) == ("UPDATE `table` SET `id` = ? WHERE `id` = ?", [2, 1])


def test_insert_query():
    builders: List[Tuple[Union[SqliteQuery, PostgresQuery], str]] = [
        (SqliteQuery(), "?"),
        (PostgresQuery(), "$1"),
    ]
    for builder, _ in builders:
        assert (
            builder.insert()
            .into("table")
            .columns(["column1", "column2"])
            .values([1, "value"])
            .to_string()
            == 'INSERT INTO "table" ("column1", "column2") VALUES (1, \'value\')'
        )
    assert (
        MysqlQuery()
        .insert()
        .into("table")
        .columns(["column1", "column2"])
        .values([1, "value"])
        .to_string()
        == "INSERT INTO `table` (`column1`, `column2`) VALUES (1, 'value')"
    )

    for builder, placeholder in builders:
        query = (
            builder.insert()
            .into("table")
            .columns(["column1", "column2"])
            .values([1, "value"])
            .build()
        )
        assert query == (
            f'INSERT INTO "table" ("column1", "column2") VALUES ({placeholder}, {placeholder.replace("1", "2")})',
            [1, "value"],
        )

    assert (
        MysqlQuery()
        .insert()
        .into("table")
        .columns(["column1", "column2"])
        .values([1, "value"])
        .build()
    ) == (
        "INSERT INTO `table` (`column1`, `column2`) VALUES (?, ?)",
        [1, "value"],
    )


def test_delete_query():
    builders: List[Tuple[Union[SqliteQuery, PostgresQuery], str]] = [
        (SqliteQuery(), "?"),
        (PostgresQuery(), "$1"),
    ]
    for builder, _ in builders:
        assert builder.delete().from_table("table").to_string() == 'DELETE FROM "table"'
    assert (
        MysqlQuery().delete().from_table("table").to_string() == "DELETE FROM `table`"
    )

    for builder, placeholder in builders:
        query = (
            builder.delete()
            .from_table("table")
            .and_where(Expr.column("id").eq(1))
            .build()
        )
        assert query == (f'DELETE FROM "table" WHERE "id" = {placeholder}', [1])

    query = (
        MysqlQuery()
        .delete()
        .from_table("table")
        .and_where(Expr.column("id").eq(1))
        .build()
    )
    assert query == ("DELETE FROM `table` WHERE `id` = ?", [1])


def test_table_create_query():
    builders: List[Union[SqliteTable, PostgresTable]] = [SqliteTable(), PostgresTable()]
    for query in builders:
        assert (
            query.create().name("table").column(Column("name").text()).to_string()
            == 'CREATE TABLE "table" ( "name" text )'
        )

    assert (
        MysqlTable().create().name("table").column(Column("name").text()).to_string()
        == "CREATE TABLE `table` ( `name` text )"
    )


def test_table_alter_query():
    builders: List[Union[SqliteTable, PostgresTable]] = [SqliteTable(), PostgresTable()]
    for query in builders:
        assert (
            query.alter().table("table").add_column(Column("name").text()).to_string()
            == 'ALTER TABLE "table" ADD COLUMN "name" text'
        )

    assert (
        MysqlTable()
        .alter()
        .table("table")
        .add_column(Column("name").text())
        .to_string()
        == "ALTER TABLE `table` ADD COLUMN `name` text"
    )


def test_table_rename_query():
    builders: List[Union[SqliteTable, PostgresTable]] = [SqliteTable(), PostgresTable()]
    for query in builders:
        assert (
            query.rename().table("table", "new_table").to_string()
            == 'ALTER TABLE "table" RENAME TO "new_table"'
        )

    assert (
        MysqlTable().rename().table("table", "new_table").to_string()
        == "RENAME TABLE `table` TO `new_table`"
    )


def test_table_drop_query():
    builders: List[Union[SqliteTable, PostgresTable]] = [SqliteTable(), PostgresTable()]
    for query in builders:
        assert query.drop().table("table").to_string() == 'DROP TABLE "table"'

    assert MysqlTable().drop().table("table").to_string() == "DROP TABLE `table`"


def test_table_truncate_query():
    assert (
        PostgresTable().truncate().table("table").to_string()
        == 'TRUNCATE TABLE "table"'
    )

    assert (
        MysqlTable().truncate().table("table").to_string() == "TRUNCATE TABLE `table`"
    )


def test_index_create_query():
    builders: List[Union[SqliteIndex, PostgresIndex]] = [SqliteIndex(), PostgresIndex()]
    for query in builders:
        assert (
            query.create().name("index").table("table").column("column").to_string()
            == 'CREATE INDEX "index" ON "table" ("column")'
        )

    assert (
        MysqlIndex().create().name("index").table("table").column("column").to_string()
        == "CREATE INDEX `index` ON `table` (`column`)"
    )


def test_drop_index_query():
    builders: List[Union[SqliteIndex, PostgresIndex]] = [SqliteIndex(), PostgresIndex()]
    for query in builders:
        assert (
            query.drop().name("index").table("table").to_string()
            == 'DROP INDEX "index"'
        )

    assert (
        MysqlIndex().drop().name("index").table("table").to_string()
        == "DROP INDEX `index` ON `table`"
    )


def test_create_foreign_key_query():
    assert (
        PostgresForeignKey()
        .create()
        .name("fk")
        .from_table("table")
        .from_column("column")
        .to_table("ref_table")
        .to_column("ref_column")
        .to_string()
        == 'ALTER TABLE "table" ADD CONSTRAINT "fk" FOREIGN KEY ("column") REFERENCES "ref_table" ("ref_column")'
    )

    assert (
        MysqlForeignKey()
        .create()
        .name("fk")
        .from_table("table")
        .from_column("column")
        .to_table("ref_table")
        .to_column("ref_column")
        .to_string()
        == "ALTER TABLE `table` ADD CONSTRAINT `fk` FOREIGN KEY (`column`) REFERENCES `ref_table` (`ref_column`)"
    )
