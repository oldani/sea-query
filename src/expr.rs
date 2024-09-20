use pyo3::prelude::*;
use sea_query::{
    expr::{Expr as SeaExpr, SimpleExpr as SeaSimpleExpr},
    query::{CaseStatement as SeaCaseStatement, Condition as SeaCondition},
    Alias, IntoCondition,
};

use crate::query::SelectStatement;
use crate::types::PyValue;

#[pyclass]
#[derive(Clone)]
pub struct SimpleExpr(pub SeaSimpleExpr);

#[pymethods]
impl SimpleExpr {
    fn __or__(&self, other: &Self) -> Self {
        Self(self.0.clone().or(other.0.clone()))
    }

    fn __and__(&self, other: &Self) -> Self {
        Self(self.0.clone().and(other.0.clone()))
    }

    fn __invert__(&self) -> Self {
        Self(self.0.clone().not())
    }
}

#[pyclass]
#[derive(Clone)]
pub struct Expr(Option<SeaExpr>);

impl Expr {
    pub fn take(&mut self) -> SeaExpr {
        self.0.take().unwrap()
    }
}

#[pymethods]
impl Expr {
    #[staticmethod]
    #[pyo3(signature = (name, table=None))]
    fn column(name: String, table: Option<String>) -> Self {
        if let Some(table) = table {
            return Self(Some(SeaExpr::col((Alias::new(table), Alias::new(name)))));
        }
        Self(Some(SeaExpr::col(Alias::new(name))))
    }

    #[staticmethod]
    fn value(value: PyValue) -> Self {
        Self(Some(SeaExpr::val(&value)))
    }

    #[allow(clippy::self_named_constructors)]
    #[staticmethod]
    fn expr(mut expr: Expr) -> Self {
        Self(Some(SeaExpr::expr(expr.take())))
    }

    #[pyo3(signature = (column, table=None))]
    fn equals(&mut self, column: String, table: Option<String>) -> SimpleExpr {
        if let Some(table) = table {
            return SimpleExpr(self.take().equals((Alias::new(table), Alias::new(column))));
        }
        SimpleExpr(self.take().equals(Alias::new(column)))
    }

    #[pyo3(signature = (column, table=None))]
    fn not_equals(&mut self, column: String, table: Option<String>) -> SimpleExpr {
        if let Some(table) = table {
            return SimpleExpr(self.take().equals((Alias::new(table), Alias::new(column))));
        }
        SimpleExpr(self.take().equals(Alias::new(column)))
    }

    fn eq(&mut self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.take().eq(&value))
    }

    fn ne(&mut self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.take().ne(&value))
    }

    fn gt(&mut self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.take().gt(&value))
    }

    fn gte(&mut self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.take().gte(&value))
    }

    fn lt(&mut self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.take().lt(&value))
    }

    fn lte(&mut self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.take().lte(&value))
    }

    fn is_(&mut self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.take().is(&value))
    }

    fn is_not(&mut self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.take().is_not(&value))
    }

    fn is_in(&mut self, values: Vec<PyValue>) -> SimpleExpr {
        SimpleExpr(self.take().is_in(&values))
    }

    fn is_not_in(&mut self, values: Vec<PyValue>) -> SimpleExpr {
        SimpleExpr(self.take().is_not_in(&values))
    }

    fn between(&mut self, start: PyValue, end: PyValue) -> SimpleExpr {
        SimpleExpr(self.take().between(&start, &end))
    }

    fn not_between(&mut self, start: PyValue, end: PyValue) -> SimpleExpr {
        SimpleExpr(self.take().not_between(&start, &end))
    }

    fn like(&mut self, value: String) -> SimpleExpr {
        SimpleExpr(self.take().like(&value))
    }

    fn not_like(&mut self, value: String) -> SimpleExpr {
        SimpleExpr(self.take().not_like(&value))
    }

    fn is_null(&mut self) -> SimpleExpr {
        SimpleExpr(self.take().is_null())
    }

    fn is_not_null(&mut self) -> SimpleExpr {
        SimpleExpr(self.take().is_not_null())
    }

    fn max(&mut self) -> SimpleExpr {
        SimpleExpr(self.take().max())
    }

    fn min(&mut self) -> SimpleExpr {
        SimpleExpr(self.take().min())
    }

    fn sum(&mut self) -> SimpleExpr {
        SimpleExpr(self.take().sum())
    }

    fn count(&mut self) -> SimpleExpr {
        SimpleExpr(self.take().count())
    }

    fn count_distinct(&mut self) -> SimpleExpr {
        SimpleExpr(self.take().count_distinct())
    }

    fn if_null(&mut self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.take().if_null(&value))
    }

    #[staticmethod]
    fn exists(query: SelectStatement) -> SimpleExpr {
        SimpleExpr(SeaExpr::exists(query.0))
    }

    #[staticmethod]
    fn case() -> CaseStatement {
        CaseStatement::new()
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
        Self(self.0.clone().add(expr.into_condition()))
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

impl IntoCondition for ConditionExpression {
    fn into_condition(self) -> SeaCondition {
        match self {
            ConditionExpression::Condition(cond) => cond.0,
            ConditionExpression::SimpleExpr(expr) => expr.0.into_condition(),
        }
    }
}

#[pyclass]
#[derive(Clone)]
pub struct CaseStatement(pub(crate) SeaCaseStatement);

#[pymethods]
impl CaseStatement {
    #[staticmethod]
    fn new() -> Self {
        Self(SeaCaseStatement::new())
    }

    fn when(&self, condition: ConditionExpression, mut then: Expr) -> Self {
        Self(self.0.clone().case(condition.into_condition(), then.take()))
    }

    fn else_(&self, mut expr: Expr) -> Self {
        Self(self.0.clone().finally(expr.take()))
    }
}

// PyO3 doesn't support generic types in methods, so we have to take a different approach
#[derive(FromPyObject)]
pub(crate) enum IntoSimpleExpr {
    SimpleExpr(SimpleExpr),
    Expr(Expr),
    CaseStatement(CaseStatement),
}

impl From<IntoSimpleExpr> for SeaSimpleExpr {
    fn from(expr: IntoSimpleExpr) -> Self {
        match expr {
            IntoSimpleExpr::SimpleExpr(expr) => expr.0,
            IntoSimpleExpr::Expr(mut expr) => expr.take().into(),
            IntoSimpleExpr::CaseStatement(case) => case.0.into(),
        }
    }
}
