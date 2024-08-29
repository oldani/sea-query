use pyo3::prelude::*;

mod expr;
mod query;
mod types;

#[pymodule]
fn sea_query(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<types::OrderBy>()?;
    m.add_class::<types::NullsOrder>()?;
    m.add_class::<types::UnionType>()?;
    m.add_class::<types::LockType>()?;
    m.add_class::<types::LockBehavior>()?;
    m.add_class::<types::DBEngine>()?;
    m.add_class::<query::Query>()?;
    m.add_class::<query::SelectStatement>()?;
    m.add_class::<query::InsertStatement>()?;
    m.add_class::<query::UpdateStatement>()?;
    m.add_class::<query::DeleteStatement>()?;
    m.add_class::<expr::SimpleExpr>()?;
    m.add_class::<expr::Expr>()?;
    m.add_class::<expr::Condition>()?;
    Ok(())
}
