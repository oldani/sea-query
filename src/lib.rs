use pyo3::prelude::*;

mod expr;
mod query;
mod table;
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
    m.add_class::<expr::OnConflict>()?;
    m.add_class::<table::Column>()?;
    m.add_class::<table::Table>()?;
    m.add_class::<table::TableCreateStatement>()?;
    m.add_class::<table::TableAlterStatement>()?;
    m.add_class::<table::TableDropStatement>()?;
    m.add_class::<table::TableRenameStatement>()?;
    m.add_class::<table::TableTruncateStatement>()?;
    Ok(())
}
