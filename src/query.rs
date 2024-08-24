use pyo3::prelude::*;
use sea_query::{DeleteStatement, InsertStatement, SelectStatement, UpdateStatement};

#[pyclass]
pub struct Query;

#[pymethods]
impl Query {
    #[staticmethod]
    fn select() -> SelectQuery {
        SelectQuery::new()
    }

    #[staticmethod]
    fn insert() -> InsertQuery {
        InsertQuery::new()
    }

    #[staticmethod]
    fn update() -> UpdateQuery {
        UpdateQuery::new()
    }

    #[staticmethod]
    fn delete() -> DeleteQuery {
        DeleteQuery::new()
    }
}

#[pyclass]
struct SelectQuery(SelectStatement);

#[pymethods]
impl SelectQuery {
    #[new]
    fn new() -> Self {
        Self(SelectStatement::new())
    }
}

#[pyclass]
struct InsertQuery(InsertStatement);

#[pymethods]
impl InsertQuery {
    #[new]
    fn new() -> Self {
        Self(InsertStatement::new())
    }
}

#[pyclass]
struct UpdateQuery(UpdateStatement);

#[pymethods]
impl UpdateQuery {
    #[new]
    fn new() -> Self {
        Self(UpdateStatement::new())
    }
}

#[pyclass]
struct DeleteQuery(DeleteStatement);

#[pymethods]
impl DeleteQuery {
    #[new]
    fn new() -> Self {
        Self(DeleteStatement::new())
    }
}
