from sea_query import (
    Condition,
    DBEngine,
    Expr,
    NullsOrder,
    OrderBy,
    Query,
    SelectStatement,
    UnionType,
)


def assert_query(
    query: SelectStatement,
    expected: str,
    mysql_expected: str = None,
):
    assert query.build_sql(DBEngine.Postgres) == expected
    assert query.build_sql(DBEngine.Sqlite) == expected
    assert query.build_sql(DBEngine.Mysql) == mysql_expected or expected.replace(
        '"', "`"
    )


def test_select_all():
    query = Query.select().from_table("table").all()
    assert_query(query, 'SELECT * FROM "table"')


def test_select_all_distinct():
    query = Query.select().from_table("table").all().distinct()
    assert_query(query, 'SELECT DISTINCT * FROM "table"')


def test_select_column():
    query = Query.select().from_table("table").column("column")
    assert_query(query, 'SELECT "column" FROM "table"')


def test_select_column_chained():
    query = Query.select().from_table("table").column("column1").column("column2")
    assert_query(query, 'SELECT "column1", "column2" FROM "table"')


def test_select_columns():
    query = Query.select().from_table("table").columns(("column1", "column2"))
    assert_query(query, 'SELECT "column1", "column2" FROM "table"')


def test_select_column_with_table():
    table = "table"
    query = Query.select().from_table("table").column("column", table)
    assert_query(query, f'SELECT "{table}"."column" FROM "{table}"')


def test_select_columns_with_table():
    table = "table"
    query = Query.select().from_table("table").columns(("column1", "column2"), table)
    assert_query(
        query, f'SELECT "{table}"."column1", "{table}"."column2" FROM "{table}"'
    )


def test_and_where():
    query = (
        Query.select().all().from_table("table").and_where(Expr.column("column1").eq(1))
    )
    assert_query(query, 'SELECT * FROM "table" WHERE "column1" = 1')


def test_and_where_chained():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column1").ne(1))
        .and_where(Expr.column("column2").gt(2))
    )
    assert_query(query, 'SELECT * FROM "table" WHERE "column1" <> 1 AND "column2" > 2')


def test_and_where_simple_expr_and():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column1").eq(1) & Expr.column("column2").eq(2))
    )
    assert_query(query, 'SELECT * FROM "table" WHERE "column1" = 1 AND "column2" = 2')


def test_and_where_simple_expr_or():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(Expr.column("column1").eq(1) | Expr.column("column2").eq(2))
    )
    assert_query(query, 'SELECT * FROM "table" WHERE "column1" = 1 OR "column2" = 2')


def test_and_where_simple_expr_chained():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(
            (Expr.column("column1").eq(1) & Expr.column("column2").eq(2))
            | (Expr.column("column3").eq(3) | Expr.column("column4").eq(4))
        )
    )
    assert_query(
        query,
        'SELECT * FROM "table" WHERE ("column1" = 1 AND "column2" = 2) OR ("column3" = 3 OR "column4" = 4)',
    )


def test_and_where_simple_expr_not():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .and_where(~Expr.column("column1").eq(1))
    )
    assert_query(query, 'SELECT * FROM "table" WHERE NOT "column1" = 1')


def test_cond_where_all_condition():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .cond_where(
            Condition.all()
            .add(Expr.column("column1").eq(1))
            .add(Expr.column("column2").eq(2))
        )
    )
    assert_query(query, 'SELECT * FROM "table" WHERE "column1" = 1 AND "column2" = 2')


def test_cond_where_any_condition():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .cond_where(
            Condition.any()
            .add(Expr.column("column1").eq(1))
            .add(Expr.column("column2").eq(2))
        )
    )
    assert_query(query, 'SELECT * FROM "table" WHERE "column1" = 1 OR "column2" = 2')


def test_cond_where_nested_condition():
    query = (
        Query.select()
        .all()
        .from_table("table")
        .cond_where(
            Condition.all()
            .add(Expr.column("column1").eq(1))
            .add(Expr.column("column2").eq(2))
            .add(
                Condition.any()
                .add(Expr.column("column3").eq(3))
                .add(Expr.column("column4").eq(4))
            )
        )
    )
    assert_query(
        query,
        'SELECT * FROM "table" WHERE "column1" = 1 AND "column2" = 2 AND ("column3" = 3 OR "column4" = 4)',
    )


def test_group_by():
    query = Query.select().from_table("table").group_by("column1")
    assert_query(query, 'SELECT  FROM "table" GROUP BY "column1"')

    query = Query.select().from_table("table").group_by("column1").group_by("column2")
    assert_query(query, 'SELECT  FROM "table" GROUP BY "column1", "column2"')

    query = (
        Query.select()
        .from_table("table")
        .group_by("column1")
        .group_by("column2", table="table")
    )
    assert_query(query, 'SELECT  FROM "table" GROUP BY "column1", "table"."column2"')


def test_group_by_and_having():
    query = (
        Query.select()
        .from_table("table")
        .group_by("column1")
        .and_having(Expr.column("column1").gt(1))
    )
    assert_query(query, 'SELECT  FROM "table" GROUP BY "column1" HAVING "column1" > 1')


def test_group_by_and_having_chained():
    query = (
        Query.select()
        .from_table("table")
        .group_by("column1")
        .and_having(Expr.column("column1").gt(1))
        .and_having(Expr.column("column2").lt(2))
    )
    assert_query(
        query,
        'SELECT  FROM "table" GROUP BY "column1" HAVING "column1" > 1 AND "column2" < 2',
    )


def test_group_by_cond_having_all_condition():
    query = (
        Query.select()
        .from_table("table")
        .group_by("column1")
        .cond_having(
            Condition.all()
            .add(Expr.column("column1").gt(1))
            .add(Expr.column("column2").lt(2))
        )
    )
    assert_query(
        query,
        'SELECT  FROM "table" GROUP BY "column1" HAVING "column1" > 1 AND "column2" < 2',
    )


def test_group_by_cond_having_any_condition():
    query = (
        Query.select()
        .from_table("table")
        .group_by("column1")
        .cond_having(
            Condition.any()
            .add(Expr.column("column1").gt(1))
            .add(Expr.column("column2").lt(2))
        )
    )
    assert_query(
        query,
        'SELECT  FROM "table" GROUP BY "column1" HAVING "column1" > 1 OR "column2" < 2',
    )


def test_group_by_cond_having_nested_condition():
    query = (
        Query.select()
        .from_table("table")
        .group_by("column1")
        .cond_having(
            Condition.all()
            .add(Expr.column("column1").gt(1))
            .add(Expr.column("column2").lt(2))
            .add(
                Condition.any()
                .add(Expr.column("column3").eq(3))
                .add(Expr.column("column4").ne(4))
            )
        )
    )
    assert_query(
        query,
        'SELECT  FROM "table" GROUP BY "column1" HAVING "column1" > 1 AND "column2" < 2 AND ("column3" = 3 OR "column4" <> 4)',
    )


def test_order_by():
    query = Query.select().from_table("table").order_by("column1", OrderBy.Asc)
    assert_query(query, 'SELECT  FROM "table" ORDER BY "column1" ASC')

    query = Query.select().from_table("table").order_by("column1", OrderBy.Desc)
    assert_query(query, 'SELECT  FROM "table" ORDER BY "column1" DESC')


def test_order_by_chained():
    query = (
        Query.select()
        .from_table("table")
        .order_by("column1", OrderBy.Asc)
        .order_by("column2", OrderBy.Desc)
    )
    assert_query(query, 'SELECT  FROM "table" ORDER BY "column1" ASC, "column2" DESC')


def test_order_by_with_nulls():
    query = (
        Query.select()
        .from_table("table")
        .order_by_with_nulls("column1", order=OrderBy.Asc, nulls=NullsOrder.First)
    )
    assert_query(
        query,
        'SELECT  FROM "table" ORDER BY "column1" ASC NULLS FIRST',
        mysql_expected="SELECT  FROM `table` ORDER BY `column1` IS NULL DESC, `column1` ASC",
    )


def test_limit():
    query = Query.select().from_table("table").limit(1)
    assert_query(query, 'SELECT  FROM "table" LIMIT 1')


def test_limit_and_offset():
    query = Query.select().from_table("table").limit(10).offset(5)
    assert_query(query, 'SELECT  FROM "table" LIMIT 10 OFFSET 5')


def test_select_from_subquery():
    subquery = (
        Query.select().all().from_table("table").and_where(Expr.column("column1").gt(1))
    )
    query = Query.select().all().from_subquery(subquery, "subquery")
    assert_query(
        query,
        'SELECT * FROM (SELECT * FROM "table" WHERE "column1" > 1) AS "subquery"',
    )


def test_select_expr():
    query = Query.select().expr(Expr.column("column1").max()).from_table("table")
    assert_query(query, 'SELECT MAX("column1") FROM "table"')


def test_select_expr_as():
    query = (
        Query.select()
        .expr_as(Expr.column("column1").count(), "count")
        .from_table("table")
    )
    assert_query(query, 'SELECT COUNT("column1") AS "count" FROM "table"')


def test_cross_join():
    query = (
        Query.select()
        .from_table("table1")
        .cross_join("table2", Expr.column("column1").equals("column2"))
    )
    assert_query(
        query,
        'SELECT  FROM "table1" CROSS JOIN "table2" ON "column1" = "column2"',
    )


def test_left_join():
    query = (
        Query.select()
        .from_table("table1")
        .left_join(
            "table2",
            Expr.column("column1", table="table1").equals("column2", table="table2"),
        )
    )
    assert_query(
        query,
        'SELECT  FROM "table1" LEFT JOIN "table2" ON "table1"."column1" = "table2"."column2"',
    )


def test_right_join():
    query = (
        Query.select()
        .from_table("table1")
        .right_join(
            "table2",
            Expr.column("column1", table="table1").equals("column2", table="table2"),
        )
    )
    assert_query(
        query,
        'SELECT  FROM "table1" RIGHT JOIN "table2" ON "table1"."column1" = "table2"."column2"',
    )


def test_inner_join():
    query = (
        Query.select()
        .from_table("table1")
        .inner_join(
            "table2",
            Expr.column("column1", table="table1").equals("column2", table="table2")
            & Expr.column("column3", table="table1").equals("column4", table="table2"),
        )
    )
    assert_query(
        query,
        'SELECT  FROM "table1" INNER JOIN "table2" ON "table1"."column1" = "table2"."column2" AND "table1"."column3" = "table2"."column4"',
    )


def test_inner_join_chained():
    query = (
        Query.select()
        .from_table("table1")
        .inner_join(
            "table2",
            Expr.column("column1", table="table1").equals("column2", table="table2"),
        )
        .inner_join(
            "table3",
            Expr.column("column3", table="table1").equals("column4", table="table3"),
        )
    )
    assert_query(
        query,
        'SELECT  FROM "table1" INNER JOIN "table2" ON "table1"."column1" = "table2"."column2" INNER JOIN "table3" ON "table1"."column3" = "table3"."column4"',
    )


def test_full_outer_join():
    query = (
        Query.select()
        .from_table("table1")
        .full_outer_join(
            "table2",
            Expr.column("column1", table="table1").equals("column2", table="table2"),
        )
    )

    assert (
        query.build_sql(DBEngine.Postgres)
        == 'SELECT  FROM "table1" FULL OUTER JOIN "table2" ON "table1"."column1" = "table2"."column2"'
    )

    assert (
        query.build_sql(DBEngine.Sqlite)
        == 'SELECT  FROM "table1" FULL OUTER JOIN "table2" ON "table1"."column1" = "table2"."column2"'
    )


def test_mixed_joins_chained():
    query = (
        Query.select()
        .from_table("table1")
        .left_join(
            "table2",
            Expr.column("column1", table="table1").equals("column2", table="table2"),
        )
        .right_join(
            "table3",
            Expr.column("column3", table="table1").equals("column4", table="table3"),
        )
        .inner_join(
            "table4",
            Expr.column("column5", table="table1").equals("column6", table="table4"),
        )
    )
    assert_query(
        query,
        'SELECT  FROM "table1" LEFT JOIN "table2" ON "table1"."column1" = "table2"."column2" RIGHT JOIN "table3" ON "table1"."column3" = "table3"."column4" INNER JOIN "table4" ON "table1"."column5" = "table4"."column6"',
    )


def test_union_intersect():
    query = (
        Query.select()
        .from_table("table1")
        .union(Query.select().from_table("table2"), UnionType.Intersect)
    )

    assert (
        query.build_sql(DBEngine.Postgres)
        == 'SELECT  FROM "table1" INTERSECT (SELECT  FROM "table2")'
    )
    assert (
        query.build_sql(DBEngine.Sqlite)
        == 'SELECT  FROM "table1" INTERSECT SELECT  FROM "table2"'
    )
    assert (
        query.build_sql(DBEngine.Mysql)
        == "SELECT  FROM `table1` INTERSECT (SELECT  FROM `table2`)"
    )


def test_union_distinct():
    query = (
        Query.select()
        .from_table("table1")
        .union(Query.select().from_table("table2"), UnionType.Distinct)
    )

    assert (
        query.build_sql(DBEngine.Postgres)
        == 'SELECT  FROM "table1" UNION (SELECT  FROM "table2")'
    )
    assert (
        query.build_sql(DBEngine.Sqlite)
        == 'SELECT  FROM "table1" UNION SELECT  FROM "table2"'
    )
    assert (
        query.build_sql(DBEngine.Mysql)
        == "SELECT  FROM `table1` UNION (SELECT  FROM `table2`)"
    )


def test_union_except():
    query = (
        Query.select()
        .from_table("table1")
        .union(Query.select().from_table("table2"), UnionType.Except)
    )

    assert (
        query.build_sql(DBEngine.Postgres)
        == 'SELECT  FROM "table1" EXCEPT (SELECT  FROM "table2")'
    )
    assert (
        query.build_sql(DBEngine.Sqlite)
        == 'SELECT  FROM "table1" EXCEPT SELECT  FROM "table2"'
    )
    assert (
        query.build_sql(DBEngine.Mysql)
        == "SELECT  FROM `table1` EXCEPT (SELECT  FROM `table2`)"
    )


def test_union_all():
    query = (
        Query.select()
        .from_table("table1")
        .union(Query.select().from_table("table2"), UnionType.All)
    )

    assert (
        query.build_sql(DBEngine.Postgres)
        == 'SELECT  FROM "table1" UNION ALL (SELECT  FROM "table2")'
    )
    assert (
        query.build_sql(DBEngine.Sqlite)
        == 'SELECT  FROM "table1" UNION ALL SELECT  FROM "table2"'
    )
    assert (
        query.build_sql(DBEngine.Mysql)
        == "SELECT  FROM `table1` UNION ALL (SELECT  FROM `table2`)"
    )


def test_union_chained():
    query = (
        Query.select()
        .from_table("table1")
        .union(Query.select().from_table("table2"), UnionType.Distinct)
        .union(Query.select().from_table("table3"), UnionType.All)
    )

    assert (
        query.build_sql(DBEngine.Postgres)
        == 'SELECT  FROM "table1" UNION (SELECT  FROM "table2") UNION ALL (SELECT  FROM "table3")'
    )
    assert (
        query.build_sql(DBEngine.Sqlite)
        == 'SELECT  FROM "table1" UNION SELECT  FROM "table2" UNION ALL SELECT  FROM "table3"'
    )
    assert (
        query.build_sql(DBEngine.Mysql)
        == "SELECT  FROM `table1` UNION (SELECT  FROM `table2`) UNION ALL (SELECT  FROM `table3`)"
    )
