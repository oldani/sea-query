use crate::types::DBEngine;
use pyo3::{pyclass, pymethods, PyRefMut};
use sea_query::{
    backend::{MysqlQueryBuilder, PostgresQueryBuilder, SqliteQueryBuilder},
    foreign_key::{
        ForeignKeyAction as SeaForeignKeyAction,
        ForeignKeyCreateStatement as SeaForeignKeyCreateStatement,
        ForeignKeyDropStatement as SeaForeignKeyDropStatement,
    },
    Alias,
};

#[pyclass(eq, eq_int)]
#[derive(Clone, PartialEq)]
pub enum ForeignKeyAction {
    Restrict,
    Cascade,
    SetNull,
    NoAction,
    SetDefault,
}

impl From<ForeignKeyAction> for SeaForeignKeyAction {
    fn from(action: ForeignKeyAction) -> Self {
        match action {
            ForeignKeyAction::Restrict => SeaForeignKeyAction::Restrict,
            ForeignKeyAction::Cascade => SeaForeignKeyAction::Cascade,
            ForeignKeyAction::SetNull => SeaForeignKeyAction::SetNull,
            ForeignKeyAction::NoAction => SeaForeignKeyAction::NoAction,
            ForeignKeyAction::SetDefault => SeaForeignKeyAction::SetDefault,
        }
    }
}

#[pyclass(subclass)]
#[derive(Clone)]
pub struct ForeignKeyCreateStatement(pub SeaForeignKeyCreateStatement);

#[pymethods]
impl ForeignKeyCreateStatement {
    #[new]
    fn new() -> Self {
        Self(SeaForeignKeyCreateStatement::new())
    }

    fn name(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.name(name);
        slf
    }

    fn from_table(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.from_tbl(Alias::new(name));
        slf
    }

    fn from_column(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.from_col(Alias::new(name));
        slf
    }

    fn to_table(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.to_tbl(Alias::new(name));
        slf
    }

    fn to_column(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.to_col(Alias::new(name));
        slf
    }

    fn on_delete(mut slf: PyRefMut<Self>, action: ForeignKeyAction) -> PyRefMut<Self> {
        slf.0.on_delete(action.into());
        slf
    }

    fn on_update(mut slf: PyRefMut<Self>, action: ForeignKeyAction) -> PyRefMut<Self> {
        slf.0.on_update(action.into());
        slf
    }

    fn to_string(&self, engine: &DBEngine) -> String {
        match engine {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
    }
}

#[pyclass(subclass)]
pub struct ForeignKeyDropStatement(pub SeaForeignKeyDropStatement);

#[pymethods]
impl ForeignKeyDropStatement {
    #[new]
    fn new() -> Self {
        Self(SeaForeignKeyDropStatement::new())
    }

    fn name(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.name(name);
        slf
    }

    fn table(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.table(Alias::new(name));
        slf
    }

    fn to_string(&self, engine: &DBEngine) -> String {
        match engine {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
    }
}

#[pyclass]
pub struct ForeignKey;

#[pymethods]
impl ForeignKey {
    #[staticmethod]
    fn create() -> ForeignKeyCreateStatement {
        ForeignKeyCreateStatement::new()
    }

    #[staticmethod]
    fn drop() -> ForeignKeyDropStatement {
        ForeignKeyDropStatement::new()
    }
}
