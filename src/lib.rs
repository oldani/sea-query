use pyo3::prelude::*;

mod query;

#[pymodule]
fn sea_query(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<query::Query>()?;
    Ok(())
}
