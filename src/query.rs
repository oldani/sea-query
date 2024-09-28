use pyo3::prelude::*;
use sea_query::{
    backend::{MysqlQueryBuilder, PostgresQueryBuilder, SqliteQueryBuilder},
    expr::SimpleExpr as SeaSimpleExpr,
    query::{
        DeleteStatement as SeaDeleteStatement, InsertStatement as SeaInsertStatement,
        OnConflict as SeaOnConflict, SelectStatement as SeaSelectStatement,
        UpdateStatement as SeaUpdateStatement,
    },
    Alias, Asterisk,
};

use crate::expr::{Condition, ConditionExpression, IntoSimpleExpr, SimpleExpr};
use crate::types::{DBEngine, LockBehavior, LockType, NullsOrder, OrderBy, PyValue, UnionType};

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
pub struct OnConflict(pub SeaOnConflict);

#[pymethods]
impl OnConflict {
    #[staticmethod]
    fn column(name: String) -> Self {
        Self(SeaOnConflict::column(Alias::new(name)))
    }

    #[staticmethod]
    fn columns(columns: Vec<String>) -> Self {
        Self(SeaOnConflict::columns(
            columns.iter().map(Alias::new).collect::<Vec<Alias>>(),
        ))
    }

    fn do_nothing(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.do_nothing();
        slf
    }

    // TODO: Implement missing methods
}

#[pyclass(subclass)]
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

    fn expr_as(mut slf: PyRefMut<Self>, expr: IntoSimpleExpr, alias: String) -> PyRefMut<Self> {
        slf.0.expr_as(expr, Alias::new(alias));
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
        slf.0.order_by(Alias::new(column), order.into());
        slf
    }

    fn order_by_with_nulls(
        mut slf: PyRefMut<Self>,
        column: String,
        order: OrderBy,
        nulls: NullsOrder,
    ) -> PyRefMut<Self> {
        slf.0
            .order_by_with_nulls(Alias::new(column), order.into(), nulls.into());
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

    fn cross_join(
        mut slf: PyRefMut<Self>,
        table: String,
        condition: ConditionExpression,
    ) -> PyRefMut<Self> {
        slf.0.cross_join(Alias::new(table), condition);
        slf
    }

    fn left_join(
        mut slf: PyRefMut<Self>,
        table: String,
        condition: ConditionExpression,
    ) -> PyRefMut<Self> {
        slf.0.left_join(Alias::new(table), condition);
        slf
    }

    fn right_join(
        mut slf: PyRefMut<Self>,
        table: String,
        condition: ConditionExpression,
    ) -> PyRefMut<Self> {
        slf.0.right_join(Alias::new(table), condition);
        slf
    }

    fn inner_join(
        mut slf: PyRefMut<Self>,
        table: String,
        condition: ConditionExpression,
    ) -> PyRefMut<Self> {
        slf.0.inner_join(Alias::new(table), condition);
        slf
    }

    fn full_outer_join(
        mut slf: PyRefMut<Self>,
        table: String,
        condition: ConditionExpression,
    ) -> PyRefMut<Self> {
        slf.0.full_outer_join(Alias::new(table), condition);
        slf
    }

    fn union(
        mut slf: PyRefMut<Self>,
        query: SelectStatement,
        union_type: UnionType,
    ) -> PyRefMut<Self> {
        slf.0.union(union_type.into(), query.0);
        slf
    }

    fn lock(mut slf: PyRefMut<Self>, lock_type: LockType) -> PyRefMut<Self> {
        slf.0.lock(lock_type.into());
        slf
    }

    fn lock_with_tables(
        mut slf: PyRefMut<Self>,
        lock_type: LockType,
        tables: Vec<String>,
    ) -> PyRefMut<Self> {
        slf.0.lock_with_tables(
            lock_type.into(),
            tables.iter().map(Alias::new).collect::<Vec<Alias>>(),
        );
        slf
    }

    fn lock_with_behavior(
        mut slf: PyRefMut<Self>,
        lock_type: LockType,
        behavior: LockBehavior,
    ) -> PyRefMut<Self> {
        slf.0.lock_with_behavior(lock_type.into(), behavior.into());
        slf
    }

    fn lock_with_tables_behavior(
        mut slf: PyRefMut<Self>,
        lock_type: LockType,
        tables: Vec<String>,
        behavior: LockBehavior,
    ) -> PyRefMut<Self> {
        slf.0.lock_with_tables_behavior(
            lock_type.into(),
            tables.iter().map(Alias::new).collect::<Vec<Alias>>(),
            behavior.into(),
        );
        slf
    }

    fn lock_shared(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.lock_shared();
        slf
    }

    fn lock_exclusive(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.lock_exclusive();
        slf
    }

    fn to_string(&self, engine: &DBEngine) -> String {
        match engine {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
    }

    fn build(&self, engine: &DBEngine) -> (String, Vec<PyValue>) {
        let (sql, values) = self.0.build_any(&*engine.query_builder());
        (sql, values.iter().map(|v| v.into()).collect())
    }
}

#[pyclass(subclass)]
pub struct InsertStatement(SeaInsertStatement);

#[pymethods]
impl InsertStatement {
    #[new]
    fn new() -> Self {
        Self(SeaInsertStatement::new())
    }

    fn into(mut slf: PyRefMut<Self>, table: String) -> PyRefMut<Self> {
        slf.0.into_table(Alias::new(table));
        slf
    }

    fn columns(mut slf: PyRefMut<Self>, columns: Vec<String>) -> PyRefMut<Self> {
        slf.0
            .columns(columns.iter().map(Alias::new).collect::<Vec<Alias>>());
        slf
    }

    fn values(mut slf: PyRefMut<Self>, values: Vec<PyValue>) -> PyRefMut<Self> {
        let values = values
            .iter()
            .map(SeaSimpleExpr::from)
            .collect::<Vec<SeaSimpleExpr>>();
        slf.0.values(values).expect("Failed to add values");
        slf
    }

    fn select_from(mut slf: PyRefMut<Self>, select: SelectStatement) -> PyRefMut<Self> {
        slf.0
            .select_from(select.0)
            .expect("Failed to add select statement");
        slf
    }

    fn on_conflict(mut slf: PyRefMut<Self>, on_conflict: OnConflict) -> PyRefMut<Self> {
        slf.0.on_conflict(on_conflict.0);
        slf
    }

    fn returning_all(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.returning_all();
        slf
    }

    fn returning_column(mut slf: PyRefMut<Self>, column: String) -> PyRefMut<Self> {
        slf.0.returning_col(Alias::new(column));
        slf
    }

    fn to_string(&self, engine: &DBEngine) -> String {
        match engine {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
    }

    fn build(&self, engine: &DBEngine) -> (String, Vec<PyValue>) {
        let (sql, values) = self.0.build_any(&*engine.query_builder());
        (sql, values.iter().map(|v| v.into()).collect())
    }
}

#[pyclass(subclass)]
pub struct UpdateStatement(SeaUpdateStatement);

#[pymethods]
impl UpdateStatement {
    #[new]
    fn new() -> Self {
        Self(SeaUpdateStatement::new())
    }

    fn table(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.table(Alias::new(name));
        slf
    }

    fn value(mut slf: PyRefMut<Self>, column: String, value: PyValue) -> PyRefMut<Self> {
        slf.0.value(Alias::new(column), SeaSimpleExpr::from(&value));
        slf
    }

    fn values(mut slf: PyRefMut<Self>, values: Vec<(String, PyValue)>) -> PyRefMut<Self> {
        let values = values
            .iter()
            .map(|(c, v)| (Alias::new(c), SeaSimpleExpr::from(v)))
            .collect::<Vec<(Alias, SeaSimpleExpr)>>();
        slf.0.values(values);
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

    fn limit(mut slf: PyRefMut<Self>, limit: u64) -> PyRefMut<Self> {
        slf.0.limit(limit);
        slf
    }

    fn returning_all(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.returning_all();
        slf
    }

    fn returning_column(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.returning_col(Alias::new(name));
        slf
    }

    fn to_string(&self, engine: &DBEngine) -> String {
        match engine {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
    }

    fn build(&self, engine: &DBEngine) -> (String, Vec<PyValue>) {
        let (sql, values) = self.0.build_any(&*engine.query_builder());
        (sql, values.iter().map(|v| v.into()).collect())
    }
}

#[pyclass(subclass)]
pub struct DeleteStatement(SeaDeleteStatement);

#[pymethods]
impl DeleteStatement {
    #[new]
    fn new() -> Self {
        Self(SeaDeleteStatement::new())
    }

    fn from_table(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.from_table(Alias::new(name));
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

    fn limit(mut slf: PyRefMut<Self>, limit: u64) -> PyRefMut<Self> {
        slf.0.limit(limit);
        slf
    }

    fn returning_all(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.returning_all();
        slf
    }

    fn returning_column(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.returning_col(Alias::new(name));
        slf
    }

    fn to_string(&self, engine: &DBEngine) -> String {
        match engine {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
    }

    fn build(&self, engine: &DBEngine) -> (String, Vec<PyValue>) {
        let (sql, values) = self.0.build_any(&*engine.query_builder());
        (sql, values.iter().map(|v| v.into()).collect())
    }
}
