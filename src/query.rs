use pyo3::prelude::*;
use sea_query::{
    query::{
        DeleteStatement as SeaDeleteStatement, InsertStatement as SeaInsertStatement,
        SelectStatement as SeaSelectStatement, UpdateStatement as SeaUpdateStatement,
    },
    Alias, Asterisk, NullOrdering, Order,
};

#[pyclass]
pub struct Query;

#[pymethods]
impl Query {
    #[staticmethod]
    fn select() -> SelectStatement {
        SelectStatement::new()
    }

    #[staticmethod]
    fn insert() -> InsertStatement {
        InsertStatement::new()
    }

    #[staticmethod]
    fn update() -> UpdateStatement {
        UpdateStatement::new()
    }

    #[staticmethod]
    fn delete() -> DeleteStatement {
        DeleteStatement::new()
    }
}

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Clone)]
enum OrderBy {
    Asc,
    Desc,
}

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Clone)]
enum NullsOrder {
    First,
    Last,
}

#[pyclass]
#[derive(Clone)]
pub struct SelectStatement(pub SeaSelectStatement);

#[pymethods]
impl SelectStatement {
    #[new]
    fn new() -> Self {
        Self(SeaSelectStatement::new())
    }

    fn from_table(mut slf: PyRefMut<Self>, name: String) -> PyRefMut<Self> {
        slf.0.from(Alias::new(name));
        slf
    }

    fn from_subquery(
        mut slf: PyRefMut<Self>,
        subquery: SelectStatement,
        alias: String,
    ) -> PyRefMut<Self> {
        slf.0.from_subquery(subquery.0, Alias::new(alias));
        slf
    }

    fn all(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.column(Asterisk);
        slf
    }

    #[pyo3(signature = (name, table=None))]
    fn column(mut slf: PyRefMut<Self>, name: String, table: Option<String>) -> PyRefMut<Self> {
        if let Some(table) = table {
            slf.0.column((Alias::new(table), Alias::new(name)));
        } else {
            slf.0.column(Alias::new(name));
        }
        slf
    }

    #[pyo3(signature = (columns, table=None))]
    fn columns(
        mut slf: PyRefMut<Self>,
        columns: Vec<String>,
        table: Option<String>,
    ) -> PyRefMut<Self> {
        if let Some(table) = table {
            let table = Alias::new(table);
            slf.0.columns(
                columns
                    .iter()
                    .map(|c| (table.clone(), Alias::new(c)))
                    .collect::<Vec<(Alias, Alias)>>(),
            );
        } else {
            slf.0
                .columns(columns.iter().map(Alias::new).collect::<Vec<Alias>>());
        }
        slf
    }

    fn distinct(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.distinct();
        slf
    }

    #[pyo3(signature = (column, table=None))]
    fn group_by(mut slf: PyRefMut<Self>, column: String, table: Option<String>) -> PyRefMut<Self> {
        if let Some(table) = table {
            slf.0.group_by_col((Alias::new(table), Alias::new(column)));
        } else {
            slf.0.group_by_col(Alias::new(column));
        }
        slf
    }

    fn order_by(mut slf: PyRefMut<Self>, column: String, order: OrderBy) -> PyRefMut<Self> {
        let order = match order {
            OrderBy::Asc => Order::Asc,
            OrderBy::Desc => Order::Desc,
        };
        slf.0.order_by(Alias::new(column), order);
        slf
    }

    fn order_by_with_nulls(
        mut slf: PyRefMut<Self>,
        column: String,
        order: OrderBy,
        nulls: NullsOrder,
    ) -> PyRefMut<Self> {
        let order = match order {
            OrderBy::Asc => Order::Asc,
            OrderBy::Desc => Order::Desc,
        };
        let nulls = match nulls {
            NullsOrder::First => NullOrdering::First,
            NullsOrder::Last => NullOrdering::Last,
        };
        slf.0.order_by_with_nulls(Alias::new(column), order, nulls);
        slf
    }

    fn limit(mut slf: PyRefMut<Self>, limit: u64) -> PyRefMut<Self> {
        slf.0.limit(limit);
        slf
    }

    fn offset(mut slf: PyRefMut<Self>, offset: u64) -> PyRefMut<Self> {
        slf.0.offset(offset);
        slf
    }
}

#[pyclass]
struct InsertStatement(SeaInsertStatement);

#[pymethods]
impl InsertStatement {
    #[new]
    fn new() -> Self {
        Self(SeaInsertStatement::new())
    }
}

#[pyclass]
struct UpdateStatement(SeaUpdateStatement);

#[pymethods]
impl UpdateStatement {
    #[new]
    fn new() -> Self {
        Self(SeaUpdateStatement::new())
    }
}

#[pyclass]
struct DeleteStatement(SeaDeleteStatement);

#[pymethods]
impl DeleteStatement {
    #[new]
    fn new() -> Self {
        Self(SeaDeleteStatement::new())
    }
}
