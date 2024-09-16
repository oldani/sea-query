use chrono::{DateTime, FixedOffset, NaiveDate, NaiveDateTime, NaiveTime};
use pyo3::{pyclass, FromPyObject, IntoPy, PyObject, Python};
use sea_query::{
    backend::{MysqlQueryBuilder, PostgresQueryBuilder, QueryBuilder, SqliteQueryBuilder},
    index::{IndexOrder, IndexType as SeaIndexType},
    query::{LockBehavior as SeaLockBehavior, LockType as SeaLockType, UnionType as SeaUnionType},
    table::ColumnType as SeaColumnType,
    value::Value,
    NullOrdering as SeaNullOrdering, Order as SeaOrder,
};

#[pyclass(eq, eq_int)]
#[derive(PartialEq)]
pub enum DBEngine {
    Mysql,
    Postgres,
    Sqlite,
}

impl DBEngine {
    pub fn query_builder(&self) -> Box<dyn QueryBuilder> {
        match self {
            DBEngine::Mysql => Box::new(MysqlQueryBuilder),
            DBEngine::Postgres => Box::new(PostgresQueryBuilder),
            DBEngine::Sqlite => Box::new(SqliteQueryBuilder),
        }
    }
}

#[derive(FromPyObject, Clone)]
pub enum PyValue {
    Bool(bool),
    Int(i64),
    Float(f64),
    DateTimeTz(DateTime<FixedOffset>),
    DateTime(NaiveDateTime),
    Date(NaiveDate),
    Time(NaiveTime),
    String(String),
}

impl From<&PyValue> for Value {
    fn from(value: &PyValue) -> Self {
        match value {
            PyValue::Bool(v) => Value::Bool(Some(*v)),
            PyValue::Float(v) => Value::Double(Some(*v)),
            PyValue::Int(v) => Value::BigInt(Some(*v)),
            PyValue::DateTimeTz(v) => Value::ChronoDateTimeWithTimeZone(Some(Box::new(*v))),
            PyValue::DateTime(v) => Value::ChronoDateTime(Some(Box::new(*v))),
            PyValue::Date(v) => Value::ChronoDate(Some(Box::new(*v))),
            PyValue::Time(v) => Value::ChronoTime(Some(Box::new(*v))),
            PyValue::String(v) => Value::String(Some(Box::new(v.clone()))),
            // TODO: Add support for other types
        }
    }
}

impl From<&Value> for PyValue {
    fn from(val: &Value) -> Self {
        match val {
            Value::Bool(v) => PyValue::Bool(v.unwrap()),
            Value::BigInt(v) => PyValue::Int(v.unwrap()),
            Value::Double(v) => PyValue::Float(v.unwrap()),
            Value::ChronoDateTimeWithTimeZone(v) => PyValue::DateTimeTz(*v.clone().unwrap()),
            Value::ChronoDateTime(v) => PyValue::DateTime(*v.clone().unwrap()),
            Value::ChronoDate(v) => PyValue::Date(*v.clone().unwrap()),
            Value::ChronoTime(v) => PyValue::Time(*v.clone().unwrap()),
            Value::String(v) => PyValue::String(*v.clone().unwrap()),
            _ => unimplemented!(),
        }
    }
}

impl IntoPy<PyObject> for PyValue {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            PyValue::Bool(v) => v.into_py(py),
            PyValue::Float(v) => v.into_py(py),
            PyValue::Int(v) => v.into_py(py),
            PyValue::DateTimeTz(v) => v.into_py(py),
            PyValue::DateTime(v) => v.into_py(py),
            PyValue::Date(v) => v.into_py(py),
            PyValue::Time(v) => v.into_py(py),
            PyValue::String(v) => v.into_py(py),
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

#[pyclass(eq, eq_int)]
#[derive(Clone, PartialEq)]
pub enum ColumnType {
    Char,
    String,
    Text,
    TinyInteger,
    SmallInteger,
    Integer,
    BigInteger,
    TinyUnsigned,
    SmallUnsigned,
    Unsigned,
    BigUnsigned,
    Float,
    Double,
    Decimal,
    DateTime,
    Timestamp,
    TimestampWithTz,
    Date,
    Time,
    Blob,
    Boolean,
    Json,
    Jsonb,
    Uuid,
}

impl From<ColumnType> for SeaColumnType {
    fn from(val: ColumnType) -> Self {
        match val {
            ColumnType::Char => SeaColumnType::Char(None),
            ColumnType::String => SeaColumnType::String(Default::default()),
            ColumnType::Text => SeaColumnType::Text,
            ColumnType::TinyInteger => SeaColumnType::TinyInteger,
            ColumnType::SmallInteger => SeaColumnType::SmallInteger,
            ColumnType::Integer => SeaColumnType::Integer,
            ColumnType::BigInteger => SeaColumnType::BigInteger,
            ColumnType::TinyUnsigned => SeaColumnType::TinyUnsigned,
            ColumnType::SmallUnsigned => SeaColumnType::SmallUnsigned,
            ColumnType::Unsigned => SeaColumnType::Unsigned,
            ColumnType::BigUnsigned => SeaColumnType::BigUnsigned,
            ColumnType::Float => SeaColumnType::Float,
            ColumnType::Double => SeaColumnType::Double,
            ColumnType::Decimal => SeaColumnType::Decimal(None),
            ColumnType::DateTime => SeaColumnType::DateTime,
            ColumnType::Timestamp => SeaColumnType::Timestamp,
            ColumnType::TimestampWithTz => SeaColumnType::TimestampWithTimeZone,
            ColumnType::Time => SeaColumnType::Time,
            ColumnType::Date => SeaColumnType::Date,
            ColumnType::Blob => SeaColumnType::Blob,
            ColumnType::Boolean => SeaColumnType::Boolean,
            ColumnType::Json => SeaColumnType::Json,
            ColumnType::Jsonb => SeaColumnType::JsonBinary,
            ColumnType::Uuid => SeaColumnType::Uuid,
        }
    }
}

impl From<SeaColumnType> for ColumnType {
    fn from(val: SeaColumnType) -> ColumnType {
        match val {
            SeaColumnType::Char(_) => ColumnType::Char,
            SeaColumnType::String(_) => ColumnType::String,
            SeaColumnType::Text => ColumnType::Text,
            SeaColumnType::TinyInteger => ColumnType::TinyInteger,
            SeaColumnType::SmallInteger => ColumnType::SmallInteger,
            SeaColumnType::Integer => ColumnType::Integer,
            SeaColumnType::BigInteger => ColumnType::BigInteger,
            SeaColumnType::TinyUnsigned => ColumnType::TinyUnsigned,
            SeaColumnType::SmallUnsigned => ColumnType::SmallUnsigned,
            SeaColumnType::Unsigned => ColumnType::Unsigned,
            SeaColumnType::BigUnsigned => ColumnType::BigUnsigned,
            SeaColumnType::Float => ColumnType::Float,
            SeaColumnType::Double => ColumnType::Double,
            SeaColumnType::Decimal(_) => ColumnType::Decimal,
            SeaColumnType::DateTime => ColumnType::DateTime,
            SeaColumnType::Timestamp => ColumnType::Timestamp,
            SeaColumnType::TimestampWithTimeZone => ColumnType::TimestampWithTz,
            SeaColumnType::Time => ColumnType::Time,
            SeaColumnType::Date => ColumnType::Date,
            SeaColumnType::Blob => ColumnType::Blob,
            SeaColumnType::Boolean => ColumnType::Boolean,
            SeaColumnType::Json => ColumnType::Json,
            SeaColumnType::JsonBinary => ColumnType::Jsonb,
            SeaColumnType::Uuid => ColumnType::Uuid,
            _ => unimplemented!(),
        }
    }
}
