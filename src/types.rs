use pyo3::{pyclass, FromPyObject};
use sea_query::{
    index::{IndexOrder, IndexType as SeaIndexType},
    Value,
};

#[pyclass(eq, eq_int)]
#[derive(PartialEq)]
pub enum DBEngine {
    Mysql,
    Postgres,
    Sqlite,
}

#[derive(FromPyObject)]
pub enum PyValue {
    Bool(bool),
    Float(f64),
    Int(i64),
    String(String),
}

impl From<&PyValue> for Value {
    fn from(value: &PyValue) -> Self {
        match value {
            PyValue::Bool(v) => Value::Bool(Some(*v)),
            PyValue::Float(v) => Value::Double(Some(*v)),
            PyValue::Int(v) => Value::BigInt(Some(*v)),
            PyValue::String(v) => Value::String(Some(Box::new(v.clone()))),
            // TODO: Add support for other types
        }
    }
}

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Clone)]
pub enum OrderBy {
    Asc,
    Desc,
}

impl Into<IndexOrder> for OrderBy {
    fn into(self) -> IndexOrder {
        match self {
            OrderBy::Asc => IndexOrder::Asc,
            OrderBy::Desc => IndexOrder::Desc,
        }
    }
}

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Clone)]
pub enum NullsOrder {
    First,
    Last,
}

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Clone)]
pub enum UnionType {
    Intersect,
    Distinct,
    Except,
    All,
}

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Clone)]
pub enum LockType {
    Update,
    NoKeyUpdate,
    Share,
    KeyShare,
}

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Clone)]
pub enum LockBehavior {
    Nowait,
    SkipLocked,
}

#[pyclass(eq, eq_int)]
#[derive(Clone, PartialEq)]
pub enum IndexType {
    BTree,
    FullText,
    Hash,
    // TODO: Custom(String),
}

impl Into<SeaIndexType> for IndexType {
    fn into(self) -> SeaIndexType {
        match self {
            IndexType::BTree => SeaIndexType::BTree,
            IndexType::FullText => SeaIndexType::FullText,
            IndexType::Hash => SeaIndexType::Hash,
        }
    }
}
