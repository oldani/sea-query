use pyo3::prelude::*;
use sea_query::{
    backend::{MysqlQueryBuilder, PostgresQueryBuilder, SqliteQueryBuilder},
    expr::SimpleExpr as SeaSimpleExpr,
    query::{
        DeleteStatement as SeaDeleteStatement, InsertStatement as SeaInsertStatement,
        LockBehavior as SeaLockBehavior, LockType as SeaLockType,
        SelectStatement as SeaSelectStatement, UnionType as SeaUnionType,
        UpdateStatement as SeaUpdateStatement,
    },
    Alias, Asterisk, NullOrdering, Order,
};

use crate::expr::{Condition, ConditionExpression, OnConflict, SimpleExpr};
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

    fn cross_join(
        mut slf: PyRefMut<Self>,
        table: String,
        condition: ConditionExpression,
    ) -> PyRefMut<Self> {
        match condition {
            ConditionExpression::Condition(cond) => {
                slf.0.cross_join(Alias::new(table), cond.0);
            }
            ConditionExpression::SimpleExpr(expr) => {
                slf.0.cross_join(Alias::new(table), expr.0);
            }
        }
        slf
    }

    fn left_join(
        mut slf: PyRefMut<Self>,
        table: String,
        condition: ConditionExpression,
    ) -> PyRefMut<Self> {
        match condition {
            ConditionExpression::Condition(cond) => {
                slf.0.left_join(Alias::new(table), cond.0);
            }
            ConditionExpression::SimpleExpr(expr) => {
                slf.0.left_join(Alias::new(table), expr.0);
            }
        }
        slf
    }

    fn right_join(
        mut slf: PyRefMut<Self>,
        table: String,
        condition: ConditionExpression,
    ) -> PyRefMut<Self> {
        match condition {
            ConditionExpression::Condition(cond) => {
                slf.0.right_join(Alias::new(table), cond.0);
            }
            ConditionExpression::SimpleExpr(expr) => {
                slf.0.right_join(Alias::new(table), expr.0);
            }
        }
        slf
    }

    fn inner_join(
        mut slf: PyRefMut<Self>,
        table: String,
        condition: ConditionExpression,
    ) -> PyRefMut<Self> {
        match condition {
            ConditionExpression::Condition(cond) => {
                slf.0.inner_join(Alias::new(table), cond.0);
            }
            ConditionExpression::SimpleExpr(expr) => {
                slf.0.inner_join(Alias::new(table), expr.0);
            }
        }
        slf
    }

    fn full_outer_join(
        mut slf: PyRefMut<Self>,
        table: String,
        condition: ConditionExpression,
    ) -> PyRefMut<Self> {
        match condition {
            ConditionExpression::Condition(cond) => {
                slf.0.full_outer_join(Alias::new(table), cond.0);
            }
            ConditionExpression::SimpleExpr(expr) => {
                slf.0.full_outer_join(Alias::new(table), expr.0);
            }
        }
        slf
    }

    fn union(
        mut slf: PyRefMut<Self>,
        query: SelectStatement,
        union_type: UnionType,
    ) -> PyRefMut<Self> {
        let union_type = match union_type {
            UnionType::Intersect => SeaUnionType::Intersect,
            UnionType::Distinct => SeaUnionType::Distinct,
            UnionType::Except => SeaUnionType::Except,
            UnionType::All => SeaUnionType::All,
        };
        slf.0.union(union_type, query.0);
        slf
    }

    fn lock(mut slf: PyRefMut<Self>, lock_type: LockType) -> PyRefMut<Self> {
        let lock_type = match lock_type {
            LockType::Update => SeaLockType::Update,
            LockType::NoKeyUpdate => SeaLockType::NoKeyUpdate,
            LockType::Share => SeaLockType::Share,
            LockType::KeyShare => SeaLockType::KeyShare,
        };
        slf.0.lock(lock_type);
        slf
    }

    fn lock_with_tables(
        mut slf: PyRefMut<Self>,
        lock_type: LockType,
        tables: Vec<String>,
    ) -> PyRefMut<Self> {
        let lock_type = match lock_type {
            LockType::Update => SeaLockType::Update,
            LockType::NoKeyUpdate => SeaLockType::NoKeyUpdate,
            LockType::Share => SeaLockType::Share,
            LockType::KeyShare => SeaLockType::KeyShare,
        };
        slf.0.lock_with_tables(
            lock_type,
            tables.iter().map(Alias::new).collect::<Vec<Alias>>(),
        );
        slf
    }

    fn lock_with_behavior(
        mut slf: PyRefMut<Self>,
        lock_type: LockType,
        behavior: LockBehavior,
    ) -> PyRefMut<Self> {
        let lock_type = match lock_type {
            LockType::Update => SeaLockType::Update,
            LockType::NoKeyUpdate => SeaLockType::NoKeyUpdate,
            LockType::Share => SeaLockType::Share,
            LockType::KeyShare => SeaLockType::KeyShare,
        };
        let behavior = match behavior {
            LockBehavior::Nowait => SeaLockBehavior::Nowait,
            LockBehavior::SkipLocked => SeaLockBehavior::SkipLocked,
        };
        slf.0.lock_with_behavior(lock_type, behavior);
        slf
    }

    fn lock_with_tables_behavior(
        mut slf: PyRefMut<Self>,
        lock_type: LockType,
        tables: Vec<String>,
        behavior: LockBehavior,
    ) -> PyRefMut<Self> {
        let lock_type = match lock_type {
            LockType::Update => SeaLockType::Update,
            LockType::NoKeyUpdate => SeaLockType::NoKeyUpdate,
            LockType::Share => SeaLockType::Share,
            LockType::KeyShare => SeaLockType::KeyShare,
        };
        let behavior = match behavior {
            LockBehavior::Nowait => SeaLockBehavior::Nowait,
            LockBehavior::SkipLocked => SeaLockBehavior::SkipLocked,
        };
        slf.0.lock_with_tables_behavior(
            lock_type,
            tables.iter().map(Alias::new).collect::<Vec<Alias>>(),
            behavior,
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

    fn build_sql(&self, engine: &DBEngine) -> String {
        match engine {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
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
