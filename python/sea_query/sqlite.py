from typing import Any

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
        return super().to_string(DBEngine.Sqlite)

    def build(self) -> tuple[str, list[Any]]:
        return super().build(DBEngine.Sqlite)


class UpdateStatement(_UpdateStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Sqlite)

    def build(self) -> tuple[str, list[Any]]:
        return super().build(DBEngine.Sqlite)


class InsertStatement(_InsertStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Sqlite)

    def build(self) -> tuple[str, list[Any]]:
        return super().build(DBEngine.Sqlite)


class DeleteStatement(_DeleteStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Sqlite)

    def build(self) -> tuple[str, list[Any]]:
        return super().build(DBEngine.Sqlite)


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
        return super().to_string(DBEngine.Sqlite)


class TableAlterStatement(_TableAlterStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Sqlite)


class TableRenameStatement(_TableRenameStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Sqlite)


class TableDropStatement(_TableDropStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Sqlite)


class TableTruncateStatement(_TableTruncateStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Sqlite)


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
        return super().to_string(DBEngine.Sqlite)


class IndexDropStatement(_IndexDropStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Sqlite)


class Index:
    @staticmethod
    def create() -> IndexCreateStatement:
        return IndexCreateStatement()

    @staticmethod
    def drop() -> IndexDropStatement:
        return IndexDropStatement()


class ForeignKeyCreateStatement(_ForeignKeyCreateStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Sqlite)


class ForeignKeyDropStatement(_ForeignKeyDropStatement):
    def to_string(self) -> str:
        return super().to_string(DBEngine.Sqlite)


class ForeignKey:
    @staticmethod
    def create() -> ForeignKeyCreateStatement:
        return ForeignKeyCreateStatement()

    @staticmethod
    def drop() -> ForeignKeyDropStatement:
        return ForeignKeyDropStatement()