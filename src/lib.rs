use pyo3::prelude::*;

mod expr;
mod query;
mod utils;

#[pymodule]
fn sea_query(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<query::Query>()?;
    m.add_class::<query::Condition>()?;
    m.add_class::<query::OrderBy>()?;
    m.add_class::<query::NullsOrder>()?;
    m.add_class::<query::UnionType>()?;
    m.add_class::<query::SelectStatement>()?;
    m.add_class::<query::InsertStatement>()?;
    m.add_class::<query::UpdateStatement>()?;
    m.add_class::<query::DeleteStatement>()?;
    m.add_class::<expr::SimpleExpr>()?;
    m.add_class::<expr::Expr>()?;
    m.add_class::<utils::DBEngine>()?;
    Ok(())
}
