use pyo3::{pyclass, FromPyObject};
use sea_query::{
    index::{IndexOrder, IndexType as SeaIndexType},
    query::{LockBehavior as SeaLockBehavior, LockType as SeaLockType, UnionType as SeaUnionType},
    NullOrdering as SeaNullOrdering, Order as SeaOrder, Value,
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

impl From<OrderBy> for SeaOrder {
    fn from(order: OrderBy) -> Self {
        match order {
            OrderBy::Asc => SeaOrder::Asc,
            OrderBy::Desc => SeaOrder::Desc,
        }
    }
}

impl From<OrderBy> for IndexOrder {
    fn from(order: OrderBy) -> Self {
        match order {
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

impl From<NullsOrder> for SeaNullOrdering {
    fn from(order: NullsOrder) -> Self {
        match order {
            NullsOrder::First => SeaNullOrdering::First,
            NullsOrder::Last => SeaNullOrdering::Last,
        }
    }
}

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Clone)]
pub enum UnionType {
    Intersect,
    Distinct,
    Except,
    All,
}

impl From<UnionType> for SeaUnionType {
    fn from(union: UnionType) -> Self {
        match union {
            UnionType::Intersect => SeaUnionType::Intersect,
            UnionType::Distinct => SeaUnionType::Distinct,
            UnionType::Except => SeaUnionType::Except,
            UnionType::All => SeaUnionType::All,
        }
    }
}

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Clone)]
pub enum LockType {
    Update,
    NoKeyUpdate,
    Share,
    KeyShare,
}

impl From<LockType> for SeaLockType {
    fn from(lock: LockType) -> Self {
        match lock {
            LockType::Update => SeaLockType::Update,
            LockType::NoKeyUpdate => SeaLockType::NoKeyUpdate,
            LockType::Share => SeaLockType::Share,
            LockType::KeyShare => SeaLockType::KeyShare,
        }
    }
}

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Clone)]
pub enum LockBehavior {
    Nowait,
    SkipLocked,
}

impl From<LockBehavior> for SeaLockBehavior {
    fn from(behavior: LockBehavior) -> Self {
        match behavior {
            LockBehavior::Nowait => SeaLockBehavior::Nowait,
            LockBehavior::SkipLocked => SeaLockBehavior::SkipLocked,
        }
    }
}

#[pyclass(eq, eq_int)]
#[derive(Clone, PartialEq)]
pub enum IndexType {
    BTree,
    FullText,
    Hash,
    // TODO: Custom(String),
}

impl From<IndexType> for SeaIndexType {
    fn from(index: IndexType) -> Self {
        match index {
            IndexType::BTree => SeaIndexType::BTree,
            IndexType::FullText => SeaIndexType::FullText,
            IndexType::Hash => SeaIndexType::Hash,
        }
    }
}
