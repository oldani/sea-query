use pyo3::{pyclass, pymethods, PyRefMut};
use sea_query::{
    backend::{MysqlQueryBuilder, PostgresQueryBuilder, SqliteQueryBuilder},
    index::{
        Index as SeaIndex, IndexCreateStatement as SeaIndexCreateStatement,
        IndexDropStatement as SeaIndexDropStatement, IndexOrder,
    },
    Alias,
};

use crate::types::{DBEngine, IndexType, OrderBy};

#[pyclass(subclass)]
#[derive(Clone)]
pub struct IndexCreateStatement(pub(crate) SeaIndexCreateStatement);

#[pymethods]
impl IndexCreateStatement {
    #[new]
    fn new() -> Self {
        Self(SeaIndexCreateStatement::new())
    }

    fn if_not_exists(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.if_not_exists();
        slf
    }

    fn name(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.name(name);
        slf
    }

    fn table(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.table(Alias::new(name));
        slf
    }

    #[pyo3(signature = (name, order=None))]
    fn column(mut slf: PyRefMut<Self>, name: String, order: Option<OrderBy>) -> PyRefMut<Self> {
        if let Some(order) = order {
            slf.0
                .col::<(Alias, IndexOrder)>((Alias::new(name), order.into()));
        } else {
            slf.0.col(Alias::new(name));
        }
        slf
    }

    fn primary(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.primary();
        slf
    }

    fn unique(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.unique();
        slf
    }

    fn nulls_not_distinct(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.nulls_not_distinct();
        slf
    }

    fn full_text(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.full_text();
        slf
    }

    fn index_type(mut slf: PyRefMut<Self>, index_type: IndexType) -> PyRefMut<Self> {
        slf.0.index_type(index_type.into());
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
pub struct IndexDropStatement(pub(crate) SeaIndexDropStatement);

#[pymethods]
impl IndexDropStatement {
    #[new]
    fn new() -> Self {
        Self(SeaIndexDropStatement::new())
    }

    fn name(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.name(name);
        slf
    }

    fn table(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.table(Alias::new(name));
        slf
    }

    fn if_exists(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.if_exists();
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
pub struct Index(SeaIndex);

#[pymethods]
impl Index {
    #[staticmethod]
    fn create() -> IndexCreateStatement {
        IndexCreateStatement::new()
    }

    #[staticmethod]
    fn drop() -> IndexDropStatement {
        IndexDropStatement::new()
    }
}
