use pyo3::{pyclass, pymethods, PyRefMut};
use sea_query::{
    backend::{MysqlQueryBuilder, PostgresQueryBuilder, SqliteQueryBuilder},
    table::{
        ColumnDef, TableAlterStatement as SeaTableAlterStatement,
        TableCreateStatement as SeaTableCreateStatement,
        TableDropStatement as SeaTableDropStatement,
        TableRenameStatement as SeaTableRenameStatement,
        TableTruncateStatement as SeaTableTruncateStatement,
    },
    Alias,
};

use crate::{
    expr::{Expr, SimpleExpr},
    foreign_key::ForeignKeyCreateStatement,
    index::IndexCreateStatement,
    types::{ColumnType, DBEngine},
};

#[pyclass]
#[derive(Clone)]
pub struct Column(ColumnDef);

#[pymethods]
impl Column {
    #[new]
    fn new(name: &str) -> Self {
        Self(ColumnDef::new(Alias::new(name)))
    }

    #[staticmethod]
    fn new_with_type(name: &str, column_type: ColumnType) -> Self {
        Self(ColumnDef::new_with_type(
            Alias::new(name),
            column_type.into(),
        ))
    }

    fn get_name(&self) -> String {
        self.0.get_column_name()
    }

    fn get_type(&self) -> Option<ColumnType> {
        self.0.get_column_type().cloned().map(Into::into)
    }

    fn not_null(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.not_null();
        slf
    }

    fn null(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.null();
        slf
    }

    fn default(mut slf: PyRefMut<Self>, mut expr: Expr) -> PyRefMut<Self> {
        slf.0.default(expr.take());
        slf
    }

    fn auto_increment(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.auto_increment();
        slf
    }

    fn unique(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.unique_key();
        slf
    }

    fn primary_key(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.primary_key();
        slf
    }

    fn char(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.char();
        slf
    }

    fn char_len(mut slf: PyRefMut<Self>, length: u32) -> PyRefMut<Self> {
        slf.0.char_len(length);
        slf
    }

    fn string(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.string();
        slf
    }

    fn string_len(mut slf: PyRefMut<Self>, length: u32) -> PyRefMut<Self> {
        slf.0.string_len(length);
        slf
    }

    fn text(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.text();
        slf
    }

    fn tiny_integer(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.tiny_integer();
        slf
    }

    fn small_integer(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.small_integer();
        slf
    }

    fn integer(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.integer();
        slf
    }

    fn big_integer(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.big_integer();
        slf
    }

    fn tiny_unsigned(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.tiny_unsigned();
        slf
    }

    fn small_unsigned(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.small_unsigned();
        slf
    }

    fn unsigned(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.unsigned();
        slf
    }

    fn big_unsigned(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.big_unsigned();
        slf
    }

    fn float(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.float();
        slf
    }

    fn double(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.double();
        slf
    }

    fn decimal(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.decimal();
        slf
    }

    fn decimal_len(mut slf: PyRefMut<Self>, precision: u32, scale: u32) -> PyRefMut<Self> {
        slf.0.decimal_len(precision, scale);
        slf
    }

    fn datetime(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.date_time();
        slf
    }

    // TODO: Add interval

    fn timestamp(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.timestamp();
        slf
    }

    fn timestamp_with_tz(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.timestamp_with_time_zone();
        slf
    }

    fn date(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.date();
        slf
    }

    fn time(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.time();
        slf
    }

    fn blob(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.blob();
        slf
    }

    fn boolean(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.boolean();
        slf
    }

    fn json(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.json();
        slf
    }

    fn jsonb(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.json_binary();
        slf
    }

    fn uuid(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.uuid();
        slf
    }

    // TODO: Add array

    fn check(mut slf: PyRefMut<Self>, expr: SimpleExpr) -> PyRefMut<Self> {
        slf.0.check(expr.0);
        slf
    }

    fn comment(mut slf: PyRefMut<Self>, comment: String) -> PyRefMut<Self> {
        slf.0.comment(comment);
        slf
    }
}

#[pyclass(subclass)]
pub struct TableCreateStatement(SeaTableCreateStatement);

#[pymethods]
impl TableCreateStatement {
    #[new]
    fn new() -> Self {
        Self(SeaTableCreateStatement::new())
    }

    fn name(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.table(Alias::new(name));
        slf
    }

    fn if_not_exists(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.if_not_exists();
        slf
    }

    fn column(mut slf: PyRefMut<'_, Self>, column: Column) -> PyRefMut<Self> {
        slf.0.col(column.0);
        slf
    }

    fn check(mut slf: PyRefMut<Self>, expr: SimpleExpr) -> PyRefMut<Self> {
        slf.0.check(expr.0);
        slf
    }

    fn index(mut slf: PyRefMut<Self>, mut index: IndexCreateStatement) -> PyRefMut<Self> {
        // TODO: Mysql only
        slf.0.index(&mut index.0);
        slf
    }

    fn primary_key(mut slf: PyRefMut<Self>, mut index: IndexCreateStatement) -> PyRefMut<Self> {
        slf.0.index(&mut index.0);
        slf
    }

    fn foreign_key(
        mut slf: PyRefMut<Self>,
        mut foreign_key: ForeignKeyCreateStatement,
    ) -> PyRefMut<Self> {
        slf.0.foreign_key(&mut foreign_key.0);
        slf
    }

    fn comment(mut slf: PyRefMut<Self>, comment: String) -> PyRefMut<Self> {
        slf.0.comment(comment);
        slf
    }

    fn to_string(&self, builder: &DBEngine) -> String {
        match builder {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
    }
}

#[pyclass(subclass)]
pub struct TableAlterStatement(SeaTableAlterStatement);

#[pymethods]
impl TableAlterStatement {
    #[new]
    fn new() -> Self {
        Self(SeaTableAlterStatement::new())
    }

    fn table(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.table(Alias::new(name));
        slf
    }

    fn add_column(mut slf: PyRefMut<Self>, column: Column) -> PyRefMut<Self> {
        slf.0.add_column(column.0);
        slf
    }

    fn add_column_if_not_exists(mut slf: PyRefMut<Self>, column: Column) -> PyRefMut<Self> {
        slf.0.add_column_if_not_exists(column.0);
        slf
    }

    fn modify_column(mut slf: PyRefMut<Self>, column: Column) -> PyRefMut<Self> {
        slf.0.modify_column(column.0);
        slf
    }

    fn rename_column(
        mut slf: PyRefMut<Self>,
        from_name: String,
        to_name: String,
    ) -> PyRefMut<Self> {
        slf.0
            .rename_column(Alias::new(from_name), Alias::new(to_name));
        slf
    }

    fn drop_column(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.drop_column(Alias::new(name));
        slf
    }

    fn add_foreign_key(
        mut slf: PyRefMut<Self>,
        foreign_key: ForeignKeyCreateStatement,
    ) -> PyRefMut<Self> {
        slf.0.add_foreign_key(foreign_key.0.get_foreign_key());
        slf
    }

    fn drop_foreign_key(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.drop_foreign_key(Alias::new(name));
        slf
    }

    fn to_string(&self, builder: &DBEngine) -> String {
        match builder {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
    }
}

#[pyclass(subclass)]
pub struct TableDropStatement(SeaTableDropStatement);

#[pymethods]
impl TableDropStatement {
    #[new]
    fn new() -> Self {
        Self(SeaTableDropStatement::new())
    }

    fn table(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.table(Alias::new(name));
        slf
    }

    fn if_exists(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.if_exists();
        slf
    }

    fn restrict(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.restrict();
        slf
    }

    fn cascade(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.cascade();
        slf
    }

    fn to_string(&self, builder: &DBEngine) -> String {
        match builder {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
    }
}

#[pyclass(subclass)]
pub struct TableRenameStatement(SeaTableRenameStatement);

#[pymethods]
impl TableRenameStatement {
    #[new]
    fn new() -> Self {
        Self(SeaTableRenameStatement::new())
    }

    fn table(mut slf: PyRefMut<Self>, from_name: String, to_name: String) -> PyRefMut<Self> {
        slf.0.table(Alias::new(from_name), Alias::new(to_name));
        slf
    }

    fn to_string(&self, builder: &DBEngine) -> String {
        match builder {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
    }
}

#[pyclass(subclass)]
pub struct TableTruncateStatement(SeaTableTruncateStatement);

#[pymethods]
impl TableTruncateStatement {
    #[new]
    fn new() -> Self {
        Self(SeaTableTruncateStatement::new())
    }

    fn table(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.table(Alias::new(name));
        slf
    }

    fn to_string(&self, builder: &DBEngine) -> String {
        match builder {
            DBEngine::Mysql => self.0.to_string(MysqlQueryBuilder),
            DBEngine::Postgres => self.0.to_string(PostgresQueryBuilder),
            DBEngine::Sqlite => self.0.to_string(SqliteQueryBuilder),
        }
    }
}

#[pyclass]
pub struct Table;

#[pymethods]
impl Table {
    #[staticmethod]
    fn create() -> TableCreateStatement {
        TableCreateStatement::new()
    }

    #[staticmethod]
    fn alter() -> TableAlterStatement {
        TableAlterStatement::new()
    }

    #[staticmethod]
    fn drop() -> TableDropStatement {
        TableDropStatement::new()
    }

    #[staticmethod]
    fn rename() -> TableRenameStatement {
        TableRenameStatement::new()
    }

    #[staticmethod]
    fn truncate() -> TableTruncateStatement {
        TableTruncateStatement::new()
    }
}
