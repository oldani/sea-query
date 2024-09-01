from sea_query import DBEngine, ForeignKey, ForeignKeyAction


def test_create_foreign_key():
    foreign_key = (
        ForeignKey.create()
        .name("fk_name")
        .from_table("from_table")
        .from_column("from_col")
        .to_table("to_table")
        .to_column("to_col")
    )

    assert foreign_key.build_sql(DBEngine.Postgres) == (
        'ALTER TABLE "from_table" ADD CONSTRAINT "fk_name" FOREIGN KEY ("from_col") REFERENCES "to_table" ("to_col")'
    )
    assert foreign_key.build_sql(DBEngine.Mysql) == (
        "ALTER TABLE `from_table` ADD CONSTRAINT `fk_name` FOREIGN KEY (`from_col`) REFERENCES `to_table` (`to_col`)"
    )
    # TODO: SQLite does not support adding foreign key constraints after table creation


def test_create_foreign_key_on_delete():
    foreign_key = (
        ForeignKey.create()
        .name("fk_name")
        .from_table("orders")
        .from_column("customer_id")
        .to_table("customers")
        .to_column("id")
        .on_delete(ForeignKeyAction.Cascade)
    )

    assert foreign_key.build_sql(DBEngine.Postgres) == (
        'ALTER TABLE "orders" ADD CONSTRAINT "fk_name" FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") ON DELETE CASCADE'
    )
    assert foreign_key.build_sql(DBEngine.Mysql) == (
        "ALTER TABLE `orders` ADD CONSTRAINT `fk_name` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE CASCADE"
    )


def test_create_foreign_key_on_update():
    foreign_key = (
        ForeignKey.create()
        .name("fk_name")
        .from_table("orders")
        .from_column("customer_id")
        .to_table("customers")
        .to_column("id")
        .on_update(ForeignKeyAction.Cascade)
    )

    assert foreign_key.build_sql(DBEngine.Postgres) == (
        'ALTER TABLE "orders" ADD CONSTRAINT "fk_name" FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") ON UPDATE CASCADE'
    )
    assert foreign_key.build_sql(DBEngine.Mysql) == (
        "ALTER TABLE `orders` ADD CONSTRAINT `fk_name` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON UPDATE CASCADE"
    )


def test_create_foreign_key_on_delete_and_update():
    foreign_key = (
        ForeignKey.create()
        .name("fk_name")
        .from_table("orders")
        .from_column("customer_id")
        .to_table("customers")
        .to_column("id")
        .on_delete(ForeignKeyAction.Cascade)
        .on_update(ForeignKeyAction.Cascade)
    )

    assert foreign_key.build_sql(DBEngine.Postgres) == (
        'ALTER TABLE "orders" ADD CONSTRAINT "fk_name" FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") ON DELETE CASCADE ON UPDATE CASCADE'
    )
    assert foreign_key.build_sql(DBEngine.Mysql) == (
        "ALTER TABLE `orders` ADD CONSTRAINT `fk_name` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE"
    )


def test_drop_foreign_key():
    foreign_key = ForeignKey.drop().name("fk_name").table("table")

    assert (
        foreign_key.build_sql(DBEngine.Postgres)
        == 'ALTER TABLE "table" DROP CONSTRAINT "fk_name"'
    )
    assert (
        foreign_key.build_sql(DBEngine.Mysql)
        == "ALTER TABLE `table` DROP FOREIGN KEY `fk_name`"
    )
