use pyo3::prelude::*;
use sea_query::{
    expr::{Expr as SeaExpr, SimpleExpr as SeaSimpleExpr},
    value::Value,
    Alias,
};

use crate::query::SelectStatement;

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

#[derive(FromPyObject)]
pub enum PyValue {
    String(String),
    Int(i64),
    Float(f64),
    Bool(bool),
}

impl From<&PyValue> for Value {
    fn from(value: &PyValue) -> Self {
        match value {
            PyValue::Bool(v) => Value::Bool(Some(*v)),
            PyValue::Int(v) => Value::BigInt(Some(*v)),
            PyValue::Float(v) => Value::Double(Some(*v)),
            PyValue::String(v) => Value::String(Some(Box::new(v.clone()))),
        }
    }
}

#[pyclass]
#[derive(Clone)]
pub struct Expr(pub SeaExpr);

#[pymethods]
impl Expr {
    #[staticmethod]
    #[pyo3(signature = (name, table=None))]
    fn column(name: String, table: Option<String>) -> Self {
        if let Some(table) = table {
            return Self(SeaExpr::col((Alias::new(table), Alias::new(name))));
        }
        Self(SeaExpr::col(Alias::new(name)))
    }

    #[staticmethod]
    fn expr(expr: Expr) -> Self {
        Self(SeaExpr::expr(expr.0.clone()))
    }

    fn eq(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().eq(&value))
    }

    fn ne(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().ne(&value))
    }

    fn gt(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().gt(&value))
    }

    fn gte(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().gte(&value))
    }

    fn lt(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().lt(&value))
    }

    fn lte(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().lte(&value))
    }

    fn is_in(&self, values: Vec<PyValue>) -> SimpleExpr {
        SimpleExpr(self.0.clone().is_in(&values))
    }

    fn is_not_in(&self, values: Vec<PyValue>) -> SimpleExpr {
        SimpleExpr(self.0.clone().is_not_in(&values))
    }

    fn between(&self, start: PyValue, end: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().between(&start, &end))
    }

    fn not_between(&self, start: PyValue, end: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().not_between(&start, &end))
    }

    fn like(&self, value: String) -> SimpleExpr {
        SimpleExpr(self.0.clone().like(&value))
    }

    fn not_like(&self, value: String) -> SimpleExpr {
        SimpleExpr(self.0.clone().not_like(&value))
    }

    fn is_null(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().is_null())
    }

    fn is_not_null(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().is_not_null())
    }

    fn max(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().max())
    }

    fn min(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().min())
    }

    fn sum(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().sum())
    }

    fn count(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().count())
    }

    fn count_distinct(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().count_distinct())
    }

    fn if_null(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().if_null(&value))
    }

    #[staticmethod]
    fn exists(query: SelectStatement) -> SimpleExpr {
        SimpleExpr(SeaExpr::exists(query.0))
    }
}
