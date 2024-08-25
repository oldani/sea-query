use pyo3::prelude::*;

#[pyclass(eq, eq_int)]
#[derive(PartialEq)]
pub enum DBEngine {
    Mysql,
    Postgres,
    Sqlite,
}
