use pyo3::prelude::*;

mod expr;
mod foreign_key;
mod index;
mod query;
mod table;
mod types;

#[pymodule]
fn _internal(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<types::OrderBy>()?;
    m.add_class::<types::NullsOrder>()?;
    m.add_class::<types::UnionType>()?;
    m.add_class::<types::LockType>()?;
    m.add_class::<types::LockBehavior>()?;
    m.add_class::<types::IndexType>()?;
    m.add_class::<types::ColumnType>()?;
    m.add_class::<types::DBEngine>()?;
    m.add_class::<expr::SimpleExpr>()?;
    m.add_class::<expr::Expr>()?;
    m.add_class::<expr::Condition>()?;
    m.add_class::<query::Query>()?;
    m.add_class::<query::OnConflict>()?;
    m.add_class::<query::SelectStatement>()?;
    m.add_class::<query::InsertStatement>()?;
    m.add_class::<query::UpdateStatement>()?;
    m.add_class::<query::DeleteStatement>()?;
    m.add_class::<table::Column>()?;
    m.add_class::<table::Table>()?;
    m.add_class::<table::TableCreateStatement>()?;
    m.add_class::<table::TableAlterStatement>()?;
    m.add_class::<table::TableDropStatement>()?;
    m.add_class::<table::TableRenameStatement>()?;
    m.add_class::<table::TableTruncateStatement>()?;
    m.add_class::<foreign_key::ForeignKey>()?;
    m.add_class::<foreign_key::ForeignKeyAction>()?;
    m.add_class::<foreign_key::ForeignKeyCreateStatement>()?;
    m.add_class::<foreign_key::ForeignKeyDropStatement>()?;
    m.add_class::<index::Index>()?;
    m.add_class::<index::IndexCreateStatement>()?;
    m.add_class::<index::IndexDropStatement>()?;
    Ok(())
}
