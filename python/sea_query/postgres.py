from typing import Any, List, Tuple

from ._internal import (
    DBEngine,
    DeleteStatement as _DeleteStatement,
    ForeignKeyCreateStatement as _ForeignKeyCreateStatement,
    ForeignKeyDropStatement as _ForeignKeyDropStatement,
    IndexCreateStatement as _IndexCreateStatement,
    IndexDropStatement as _IndexDropStatement,
    InsertStatement as _InsertStatement,
    SelectStatement as _SelectStatement,
    TableAlterStatement as _TableAlterStatement,
    TableCreateStatement as _TableCreateStatement,
    TableDropStatement as _TableDropStatement,
    TableRenameStatement as _TableRenameStatement,
    TableTruncateStatement as _TableTruncateStatement,
    UpdateStatement as _UpdateStatement,
)


class SelectStatement(_SelectStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)

    def build(self) -> Tuple[str, List[Any]]:
        return super().build(DBEngine.Postgres)


class UpdateStatement(_UpdateStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)

    def build(self) -> Tuple[str, List[Any]]:
        return super().build(DBEngine.Postgres)


class InsertStatement(_InsertStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)

    def build(self) -> Tuple[str, List[Any]]:
        return super().build(DBEngine.Postgres)


class DeleteStatement(_DeleteStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)

    def build(self) -> Tuple[str, List[Any]]:
        return super().build(DBEngine.Postgres)


class Query:
    @staticmethod
    def select() -> SelectStatement:
        return SelectStatement()

    @staticmethod
    def update() -> UpdateStatement:
        return UpdateStatement()

    @staticmethod
    def insert() -> InsertStatement:
        return InsertStatement()

    @staticmethod
    def delete() -> DeleteStatement:
        return DeleteStatement()


class TableCreateStatement(_TableCreateStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)


class TableAlterStatement(_TableAlterStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)


class TableRenameStatement(_TableRenameStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)


class TableDropStatement(_TableDropStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)


class TableTruncateStatement(_TableTruncateStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)


class Table:
    @staticmethod
    def create() -> TableCreateStatement:
        return TableCreateStatement()

    @staticmethod
    def alter() -> TableAlterStatement:
        return TableAlterStatement()

    @staticmethod
    def rename() -> TableRenameStatement:
        return TableRenameStatement()

    @staticmethod
    def drop() -> TableDropStatement:
        return TableDropStatement()

    @staticmethod
    def truncate() -> TableTruncateStatement:
        return TableTruncateStatement()


class IndexCreateStatement(_IndexCreateStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)


class IndexDropStatement(_IndexDropStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)


class Index:
    @staticmethod
    def create() -> IndexCreateStatement:
        return IndexCreateStatement()

    @staticmethod
    def drop() -> IndexDropStatement:
        return IndexDropStatement()


class ForeignKeyCreateStatement(_ForeignKeyCreateStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)


class ForeignKeyDropStatement(_ForeignKeyDropStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Postgres)


class ForeignKey:
    @staticmethod
    def create() -> ForeignKeyCreateStatement:
        return ForeignKeyCreateStatement()

    @staticmethod
    def drop() -> ForeignKeyDropStatement:
        return ForeignKeyDropStatement()
