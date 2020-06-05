"""Type expressions definition."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

import metadsl

# Expressions definition


def constructor(fn: Callable):
    """Decorator for expression constructor."""

    def _fn(*args, **kwargs):
        fn.__qualname__ = fn.__qualname__.split('.')[0]
        return metadsl.expression(fn)(*args, **kwargs)

    return _fn


def register(name: str, klass: Expr, f_source_name: str, f_target: Callable):
    """
    Register a function expression.

    Parameters
    ----------
    name : str
    klass : Expr
    f_source_name : str
    f_target : Callable
    """
    f_target.__qualname__ = name
    setattr(klass, f_source_name, metadsl.expression(f_target))


class Expr(metadsl.Expression):
    """Base expression class."""

    @property
    def _display_name(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def expr(*args, **kwargs):
        """Create an expression with the given value."""
        raise NotImplementedError('Operation not supported yet.')

    def __repr__(self) -> str:
        fn_name = (
            self.function
            if not str(self.function) == 'expr'
            else self._display_name
        )

        output = '{}({})'.format(fn_name, self.args)
        return output


class Database(Expr):
    """Database expression."""


class DatabaseSchema(Expr):
    """Database schema expression."""


@dataclass
class TableSchema(Expr):
    """Table schema expression."""

    @staticmethod
    @constructor
    def expr(structure: Dict[str, Dict[str, Any]]) -> TableSchema:
        """
        Create a table schema expression from a dictionary.

        Parameters
        ----------
        structure : dict

        Returns
        -------
        TableSchema
        """

    @property
    def structure(self) -> dict:
        return self.args[0]

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        output = '{}\n'.format(self._display_name)
        for k, v in self.structure.items():
            output += '  {}: {}({})\n'.format(
                k, v['type'], 'nullale' if v['nullable'] else 'non-nullable'
            )
        return output


@dataclass
class TableBase(Expr):
    """Table base expression class."""

    @metadsl.expression
    def __getitem__(self, key: Union[str, List[str]]) -> Projection:
        """
        Get item from Table.

        Parameters
        ----------
        key : Union[str, list[str]]
            The key could be a string or a list of keys.

        Returns
        -------
        Projection
        """

    @metadsl.expression
    def __add__(self, other: Union[int, float]) -> TableBase:
        """
        Add a number to a table expression.

        Parameters
        ----------
        other : int or float

        Returns
        -------
        TableBase
        """

    @metadsl.expression
    def __truediv__(self, other: Union[int, float]) -> TableBase:
        """
        Divide a table expression by a given number.

        Parameters
        ----------
        other : int or float

        Returns
        -------
        TableBase
        """

    @metadsl.expression
    def __floordiv__(self, other: Union[int, float]) -> TableBase:
        """
        Divide a table expression by a given number.

        The result should be truncated to the integer value.

        Parameters
        ----------
        other : int or float

        Returns
        -------
        TableBase
        """

    @metadsl.expression
    def __mod__(self, other: Union[int, float]) -> TableBase:
        """
        Calculate the modulus of table expression by a number.

        Parameters
        ----------
        other : int or float

        Returns
        -------
        TableBase
        """

    @metadsl.expression
    def __mul__(self, other: Union[int, float]) -> TableBase:
        """
        Multiply a number to a table expression.

        Parameters
        ----------
        other : int or float

        Returns
        -------
        TableBase
        """

    @metadsl.expression
    def __sub__(self, other: Union[int, float]) -> TableBase:
        """
        Subtract a number from a table expression.

        Parameters
        ----------
        other : int or float

        Returns
        -------
        TableBase
        """

    @metadsl.expression
    def __pow__(self, other: Union[int, float]) -> TableBase:
        """
        Calculate the power of the table expression to the given number.

        Parameters
        ----------
        other : int or float

        Returns
        -------
        TableBase
        """


@dataclass
class Table(TableBase):
    """Table expression class."""

    @staticmethod
    @constructor
    def expr(
        name: str,
        schema: TableSchema,
        database_name: Optional[str] = None,
        database_schema_name: Optional[str] = None,
    ) -> Table:
        """
        Create a table expression from a schema.

        Parameters
        ----------
        name : str
        schema : Schema
        database_name : str, optional, default None
        database_schema_name : str, optional, default None

        Returns
        -------
        Table
        """

    @property
    def name(self) -> str:
        return self.args[0]

    @property
    def schema(self) -> TableSchema:
        return self.args[1]

    @property
    def database_name(self) -> Optional[str]:
        return self.args[2]

    @property
    def database_schema_name(self) -> Optional[str]:
        return self.args[3]

    @property
    def _display_name(self) -> str:
        return '{}{}{}'.format(
            '{}.'.format(self.database_name) if self.database_name else '',
            '{}.'.format(self.database_schema_name)
            if self.database_schema_name
            else '',
            self.name,
        )

    def __repr__(self) -> str:
        output = '{}: {}\n'.format(self._display_name, self.__class__.__name__)
        for k, v in self.schema.structure.items():
            output += '  {}: {}({})\n'.format(
                k, v['type'], 'nullale' if v['nullable'] else 'non-nullable'
            )
        return output


class Projection(TableBase):
    """Collection of columns expression"""

    @property
    def source(self) -> Table:
        return self.args[0]

    @property
    def columns(self) -> Union[str, List[str]]:
        return self.args[1]

    @property
    def _display_name(self) -> str:
        return '{}[{}]'.format(self.__class__.__name__, str(self.columns))

    def __repr__(self) -> str:
        output = '{}\n'.format(self._display_name)
        for l in repr(self.source).split('\n'):
            output += '  {}\n'.format(l)
        return output


class ValueExpr(Expr):
    """Column expression."""


class ColumnExpr(ValueExpr):
    """Column expression."""


class ScalarExpr(ValueExpr):
    """Column expression."""


class AnyValue(ValueExpr):
    """Any value expression."""


class AnyScalar(ScalarExpr, AnyValue):
    """Any scalar expression."""


class AnyColumn(ColumnExpr, AnyValue):
    """Any column expression."""