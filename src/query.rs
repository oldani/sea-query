use pyo3::prelude::*;
use sea_query::{
    backend::{MysqlQueryBuilder, PostgresQueryBuilder, SqliteQueryBuilder},
    query::{
        Condition as SeaCondition, ConditionExpression as SeaConditionExpression,
        DeleteStatement as SeaDeleteStatement, InsertStatement as SeaInsertStatement,
        SelectStatement as SeaSelectStatement, UpdateStatement as SeaUpdateStatement,
    },
    Alias, Asterisk, NullOrdering, Order,
};

use crate::expr::{Expr, SimpleExpr};
use crate::utils::DBEngine;

#[pyclass]
pub struct Query;

#[pymethods]
impl Query {
    #[staticmethod]
    fn select() -> SelectStatement {
        SelectStatement::new()
    }

    #[staticmethod]
    fn insert() -> InsertStatement {
        InsertStatement::new()
    }

    #[staticmethod]
    fn update() -> UpdateStatement {
        UpdateStatement::new()
    }

    #[staticmethod]
    fn delete() -> DeleteStatement {
        DeleteStatement::new()
    }
}

#[pyclass]
#[derive(Clone)]
pub struct Condition(pub SeaCondition);

#[pymethods]
impl Condition {
    #[staticmethod]
    fn all() -> Self {
        Self(SeaCondition::all())
    }

    #[staticmethod]
    fn any() -> Self {
        Self(SeaCondition::any())
    }

    fn add(&self, expr: ConditionExpression) -> Self {
        Self(self.0.clone().add(match expr {
            ConditionExpression::Condition(cond) => SeaConditionExpression::Condition(cond.0),
            ConditionExpression::SimpleExpr(expr) => SeaConditionExpression::SimpleExpr(expr.0),
        }))
    }

    fn __invert__(&self) -> Self {
        Self(self.0.clone().not())
    }
}

#[derive(FromPyObject)]
pub enum ConditionExpression {
    Condition(Condition),
    SimpleExpr(SimpleExpr),
}

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Clone)]
pub enum OrderBy {
    Asc,
    Desc,
}

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Clone)]
pub enum NullsOrder {
    First,
    Last,
}

#[pyclass]
#[derive(Clone)]
pub struct SelectStatement(pub SeaSelectStatement);

#[pymethods]
impl SelectStatement {
    #[new]
    fn new() -> Self {
        Self(SeaSelectStatement::new())
    }

    fn from_table(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.from(Alias::new(name));
        slf
    }

    fn from_subquery(
        mut slf: PyRefMut<Self>,
        subquery: SelectStatement,
        alias: String,
    ) -> PyRefMut<Self> {
        slf.0.from_subquery(subquery.0, Alias::new(alias));
        slf
    }

    fn all(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.column(Asterisk);
        slf
    }

    #[pyo3(signature = (name, table=None))]
    fn column(mut slf: PyRefMut<Self>, name: String, table: Option<String>) -> PyRefMut<Self> {
        if let Some(table) = table {
            slf.0.column((Alias::new(table), Alias::new(name)));
        } else {
            slf.0.column(Alias::new(name));
        }
        slf
    }

    #[pyo3(signature = (columns, table=None))]
    fn columns(
        mut slf: PyRefMut<Self>,
        columns: Vec<String>,
        table: Option<String>,
    ) -> PyRefMut<Self> {
        if let Some(table) = table {
            let table = Alias::new(table);
            slf.0.columns(
                columns
                    .iter()
                    .map(|c| (table.clone(), Alias::new(c)))
                    .collect::<Vec<(Alias, Alias)>>(),
            );
        } else {
            slf.0
                .columns(columns.iter().map(Alias::new).collect::<Vec<Alias>>());
        }
        slf
    }

    fn expr(mut slf: PyRefMut<Self>, expr: SimpleExpr) -> PyRefMut<Self> {
        slf.0.expr(expr.0);
        slf
    }

    fn expr_as(mut slf: PyRefMut<Self>, expr: SimpleExpr, alias: String) -> PyRefMut<Self> {
        slf.0.expr_as(expr.0, Alias::new(alias));
        slf
    }

    fn distinct(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.distinct();
        slf
    }

    fn and_where(mut slf: PyRefMut<Self>, expr: SimpleExpr) -> PyRefMut<Self> {
        slf.0.and_where(expr.0);
        slf
    }

    fn cond_where(mut slf: PyRefMut<Self>, cond: Condition) -> PyRefMut<Self> {
        slf.0.cond_where(cond.0);
        slf
    }

    #[pyo3(signature = (column, table=None))]
    fn group_by(mut slf: PyRefMut<Self>, column: String, table: Option<String>) -> PyRefMut<Self> {
        if let Some(table) = table {
            slf.0.group_by_col((Alias::new(table), Alias::new(column)));
        } else {
            slf.0.group_by_col(Alias::new(column));
        }
        slf
    }

    fn and_having(mut slf: PyRefMut<Self>, expr: SimpleExpr) -> PyRefMut<Self> {
        slf.0.and_having(expr.0);
        slf
    }

    fn cond_having(mut slf: PyRefMut<Self>, cond: Condition) -> PyRefMut<Self> {
        slf.0.cond_having(cond.0);
        slf
    }

    fn order_by(mut slf: PyRefMut<Self>, column: String, order: OrderBy) -> PyRefMut<Self> {
        let order = match order {
            OrderBy::Asc => Order::Asc,
            OrderBy::Desc => Order::Desc,
        };
        slf.0.order_by(Alias::new(column), order);
        slf
    }

    fn order_by_with_nulls(
        mut slf: PyRefMut<Self>,
        column: String,
        order: OrderBy,
        nulls: NullsOrder,
    ) -> PyRefMut<Self> {
        let order = match order {
            OrderBy::Asc => Order::Asc,
            OrderBy::Desc => Order::Desc,
        };
        let nulls = match nulls {
            NullsOrder::First => NullOrdering::First,
            NullsOrder::Last => NullOrdering::Last,
        };
        slf.0.order_by_with_nulls(Alias::new(column), order, nulls);
        slf
    }

    fn limit(mut slf: PyRefMut<Self>, limit: u64) -> PyRefMut<Self> {
        slf.0.limit(limit);
        slf
    }

    fn offset(mut slf: PyRefMut<Self>, offset: u64) -> PyRefMut<Self> {
        slf.0.offset(offset);
        slf
    }

    fn build_sql(&self, engine: &DBEngine) -> String {
        match engine {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
    }
}

#[pyclass]
pub struct InsertStatement(SeaInsertStatement);

#[pymethods]
impl InsertStatement {
    #[new]
    fn new() -> Self {
        Self(SeaInsertStatement::new())
    }
}

#[pyclass]
pub struct UpdateStatement(SeaUpdateStatement);

#[pymethods]
impl UpdateStatement {
    #[new]
    fn new() -> Self {
        Self(SeaUpdateStatement::new())
    }
}

#[pyclass]
pub struct DeleteStatement(SeaDeleteStatement);

#[pymethods]
impl DeleteStatement {
    #[new]
    fn new() -> Self {
        Self(SeaDeleteStatement::new())
    }
}
