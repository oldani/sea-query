# SeaQuery

[![CI](https://github.com/oldani/sea-query/actions/workflows/release.yml/badge.svg)](https://github.com/oldani/sea-query/actions/workflows/release.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/sea-query)](https://pypi.org/project/sea-query/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sea-query)](https://pypi.org/project/sea-query/)

SeaQuery is a query builder to help you construct dynamic SQL queries in Python for PostgreSQL, MySQL, and SQLite.
This project is a port of the [SeaQuery.rs](https://github.com/SeaQL/sea-query-rs) project to Python using PyO3.

## Install

You can install the package from PyPI using pip:

```bash
pip install sea-query
```

Or if you are using [uv](https://github.com/astral-sh/uv):

```bash
uv add sea-query
```

## Usage

Here are some examples of how to use SeaQuery to build SQL queries:

### SELECT Query

```python
from sea_query import Query, Expr, DBEngine

query = (
    Query.select()
    .all()
    .from_table("table")
    .and_where(Expr.column("column1").ne(1))
    .and_where(Expr.column("column2").gt(2))
)
assert query.to_string(DBEngine.Postgres) == (
    'SELECT * FROM "table" WHERE "column1" <> 1 AND "column2" > 2'
)
# Or if you want to use parameter bindings
assert query.build(DBEngine.Postgres) == (
    'SELECT * FROM "table" WHERE "column1" <> $1 AND "column2" > $2',
    [1, 2]
)
```

### INSERT Query

```python
from sea_query import Query, Expr, DBEngine

query = (
    Query.insert()
    .into("table")
    .columns(["column1", "column2"])
    .values([1, "str1"])
    .values([2, "str2"])
)
assert query.to_string(DBEngine.Postgres) == (
    'INSERT INTO "table" ("column1", "column2") VALUES (1, \'str1\'), (2, \'str2\')'
)
# With parameter bindings
assert query.build(DBEngine.Postgres) == (
    'INSERT INTO "table" ("column1", "column2") VALUES ($1, $2), ($3, $4)',
    [1, "str1", 2, "str2"],
)
```

### UPDATE Query

```python
from sea_query import Query, Expr, DBEngine

query = (
    Query.update()
    .table("table")
    .value("column", 1)
    .cond_where(
        Condition.any()
        .add(Expr.column("column2").eq("value"))
        .add(Expr.column("column3").eq(3))
    )
)
assert query.to_string(DBEngine.Postgres) == (
    'UPDATE "table" SET "column" = 1 WHERE "column2" = \'value\' OR "column3" = 3'
)
```

### DELETE Query

```python
from sea_query import Query, Expr, DBEngine

query = (
    Query.delete()
    .from_table("table")
    .and_where(Expr.column("column1").eq(1))
)
assert query.to_string(DBEngine.Postgres) == (
    'DELETE FROM "table" WHERE "column1" = 1'
)
```

### Table Create

```python
from sea_query import Table, Column, DBEngine

statement = (
    Table.create()
    .name("users")
    .column(Column("id").big_integer().primary_key().auto_increment())
    .column(
        Column("name").string().string_len(128).not_null().default(Expr.value(""))
    )
    .column(Column("email").string().string_len(255).null().unique())
)

assert statement.to_string(DBEngine.Postgres) == (
    'CREATE TABLE "users" ( '
        '"id" bigserial PRIMARY KEY, '
        '"name" varchar(128) NOT NULL DEFAULT \'\', '
        '"email" varchar(255) NULL UNIQUE '
    ')'
)
```

### Table Alter

```python
from sea_query import Table, Column, DBEngine

statement = (
    Table.alter()
    .table("users")
    .add_column(
        Column("created_at").timestamp().null()
    )
)

assert statement.to_string(DBEngine.Postgres) == (
    'ALTER TABLE "users" ADD COLUMN "created_at" timestamp NULL'
)
```

### Table Drop

```python
from sea_query import Table, DBEngine

assert (
    Table.drop().table("users").to_string(DBEngine.Postgres)
    == 'DROP TABLE "users"'
)
```

### Create Index

```python
from sea_query import Index, DBEngine

index = (
    Index.create()
    .name("index_name")
    .   table("table")
    .column("col1")
    .column("col2")
)

assert index.to_string(DBEngine.Postgres) == (
    'CREATE INDEX "index_name" ON "table" ("col1", "col2")'
)
```

### Drop Index

```python
from sea_query import Index, DBEngine

index = (
    Index.drop().name("index_name").table("table")
)

assert index.to_string(DBEngine.Postgres) == (
    'DROP INDEX "index_name"'
)
```
