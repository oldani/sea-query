from enum import IntEnum
from typing import Optional, Self, TypeAlias, Union

class DBEngine(IntEnum):
    Mysql = 1
    Postgres = 2
    Sqlite = 3

class OrderBy(IntEnum):
    Asc = 1
    Desc = 2

class NullsOrder(IntEnum):
    First = 1
    Last = 2

class UnionType(IntEnum):
    Intersect = 1
    Distinct = 2
    Except = 3
    All = 4

class LockType(IntEnum):
    Update = 1
    NoKeyUpdate = 2
    Share = 3
    KeyShare = 4

class LockBehavior(IntEnum):
    Nowait = 1
    SkipLocked = 2

class SimpleExpr:
    def __or__(self, other: SimpleExpr) -> SimpleExpr: ...
    def __and__(self, other: SimpleExpr) -> SimpleExpr: ...
    def __invert__(self) -> SimpleExpr: ...

ValueType: TypeAlias = Union[int, float, str, bool]

class Expr:
    @staticmethod
    def column(name: str, table: Optional[str] = None) -> Self: ...
    @staticmethod
    def expr(expr: Expr) -> Self: ...
    def equals(self, column: str, table: Optional[str] = None) -> SimpleExpr: ...
    def not_equals(self, column: str, table: Optional[str] = None) -> SimpleExpr: ...
    def eq(self, other: ValueType) -> SimpleExpr: ...
    def ne(self, other: ValueType) -> SimpleExpr: ...
    def gt(self, other: ValueType) -> SimpleExpr: ...
    def gte(self, other: ValueType) -> SimpleExpr: ...
    def lt(self, other: ValueType) -> SimpleExpr: ...
    def lte(self, other: ValueType) -> SimpleExpr: ...
    def is_(self, other: ValueType) -> SimpleExpr: ...
    def is_not(self, other: ValueType) -> SimpleExpr: ...
    def is_in(self, values: list[ValueType]) -> SimpleExpr: ...
    def is_not_in(self, values: list[ValueType]) -> SimpleExpr: ...
    def between(self, start: ValueType, end: ValueType) -> SimpleExpr: ...
    def not_between(self, start: ValueType, end: ValueType) -> SimpleExpr: ...
    def like(self, pattern: str) -> SimpleExpr: ...
    def not_like(self, pattern: str) -> SimpleExpr: ...
    def is_null(self) -> SimpleExpr: ...
    def is_not_null(self) -> SimpleExpr: ...
    def max(self) -> SimpleExpr: ...
    def min(self) -> SimpleExpr: ...
    def sum(self) -> SimpleExpr: ...
    def count(self) -> SimpleExpr: ...
    def count_distinct(self) -> SimpleExpr: ...
    def if_null(self, value: ValueType) -> SimpleExpr: ...
    @staticmethod
    def exists(query: SelectStatement) -> SimpleExpr: ...

ConditionExpression: TypeAlias = Union[SimpleExpr, Condition]

class Condition:
    @staticmethod
    def all() -> Self: ...
    @staticmethod
    def any() -> Self: ...
    def add(self, expr: ConditionExpression) -> Self: ...
    def __invert__(self) -> Self: ...

class OnConflict:
    @staticmethod
    def column(name: str) -> Self: ...
    @staticmethod
    def columns(columns: list[str]) -> Self: ...
    def do_nothing(self) -> Self: ...

class SelectStatement:
    def __init__(self) -> None: ...
    def from_table(self, name: str) -> Self: ...
    def from_subquery(self, query: SelectStatement) -> Self: ...
    def all(self) -> Self: ...
    def column(self, name: str, table: Optional[str] = None) -> Self: ...
    def columns(self, columns: list[str], table: Optional[str] = None) -> Self: ...
    def expr(self, expr: Expr) -> Self: ...
    def expr_as(self, expr: Expr, alias: str) -> Self: ...
    def distinct(self) -> Self: ...
    def and_where(self, expr: SimpleExpr) -> Self: ...
    def cond_where(self, cond: Condition) -> Self: ...
    def group_by(self, column: str, table: Optional[str] = None) -> Self: ...
    def and_having(self, expr: SimpleExpr) -> Self: ...
    def cond_having(self, cond: Condition) -> Self: ...
    def order_by(self, column: str, order: OrderBy) -> Self: ...
    def order_by_with_nulls(
        self, column: str, order: OrderBy, nulls: NullsOrder
    ) -> Self: ...
    def limit(self, limit: int) -> Self: ...
    def offset(self, offset: int) -> Self: ...
    def cross_join(self, table: str, condition: ConditionExpression) -> Self: ...
    def left_join(self, table: str, condition: ConditionExpression) -> Self: ...
    def right_join(self, table: str, condition: ConditionExpression) -> Self: ...
    def inner_join(self, table: str, condition: ConditionExpression) -> Self: ...
    def full_outer_join(self, table: str, condition: ConditionExpression) -> Self: ...
    def union(self, query: SelectStatement, union_type: UnionType) -> Self: ...
    def lock(self, lock_type: LockType) -> Self: ...
    def lock_with_tables(self, lock_type: LockType, tables: list[str]) -> Self: ...
    def lock_with_behavior(
        self, lock_type: LockType, behavior: LockBehavior
    ) -> Self: ...
    def lock_with_tables_behavior(
        self, lock_type: LockType, tables: list[str], behavior: LockBehavior
    ) -> Self: ...
    def lock_shared(self) -> Self: ...
    def lock_exclusive(self) -> Self: ...
    def build_sql(self, engine: DBEngine) -> str: ...

class InsertStatement:
    def __init__(self) -> None: ...
    def into(self, table: str) -> Self: ...
    def columns(self, columns: list[str]) -> Self: ...
    def values(self, values: list[ValueType]) -> Self: ...
    def select_from(self, query: SelectStatement) -> Self: ...
    def on_conflict(self, on_conflict: OnConflict) -> Self: ...
    def returning_all(self) -> Self: ...
    def returning_column(self, column: str) -> Self: ...
    def build_sql(self, engine: DBEngine) -> str: ...

class Query:
    @staticmethod
    def select() -> SelectStatement: ...
    @staticmethod
    def insert() -> InsertStatement: ...
