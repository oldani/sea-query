use pyo3::prelude::*;

mod expr;
mod query;
mod utils;

#[pymodule]
fn sea_query(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<query::Query>()?;
    m.add_class::<query::Condition>()?;
    m.add_class::<expr::SimpleExpr>()?;
    m.add_class::<expr::Expr>()?;
    m.add_class::<utils::DBEngine>()?;
    Ok(())
}
