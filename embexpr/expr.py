# coding: utf-8
from __future__ import absolute_import, unicode_literals

import ast
import types
import typing as ty

import six

from six.moves import builtins

from .error import ParseError

CALL_WHITELIST = {
    "abs",
    "all",
    "any",
    "chr",
    "float",
    "int",
    "len",
    "max",
    "min",
    "ord",
    "reversed",
    "round",
    "sorted",
    "str",
    "sum",
    "tuple",
    "unichr",
    "unicode",
}

SAFE_NODES = {
    ast.Add,
    ast.Attribute,
    ast.BinOp,
    ast.Call,
    ast.Compare,
    ast.Dict,
    ast.Div,
    ast.Eq,
    ast.Expression,
    ast.FloorDiv,
    ast.Gt,
    ast.GtE,
    ast.In,
    ast.keyword,
    ast.List,
    ast.Load,
    ast.Lt,
    ast.LtE,
    ast.Mod,
    ast.Mult,
    ast.Name,
    ast.Not,
    ast.NotEq,
    ast.NotIn,
    ast.Num,
    ast.Pow,
    ast.Str,
    ast.Sub,
    ast.USub,
    ast.Tuple,
    ast.UnaryOp,
    ast.Set,
}
if six.PY34:
    SAFE_NODES.add(ast.NameConstant)


class Expr(object):
    def __init__(self, expr):  # type: (ty.Text) -> None
        self.expr = expr  # type: ty.Text
        self._cache = None  # type: ty.Optional[types.CodeType]

    def purge_cache(self):  # type: () -> None
        self._cache = None

    @property
    def code(self):  # type: () -> types.CodeType
        if self._cache:
            return self._cache

        self._cache = parse(self.expr)
        return self._cache

    def __call__(self, **kwargs):
        return eval(self.code, {b"__builtins__": builtins}, kwargs)


def parse(text):  # type: (ty.Text) -> types.CodeType
    class CleansingNodeVisitor(ast.NodeVisitor):
        def generic_visit(self, node, inside_call=False):
            if type(node) not in SAFE_NODES:
                raise ParseError("invalid node: {}".format(type(node)), getattr(node, "col_offset", 0))
            elif isinstance(node, ast.Call):
                inside_call = True
            elif isinstance(node, ast.Name) and inside_call:
                if hasattr(builtins, node.id) and node.id not in CALL_WHITELIST:
                    raise ParseError("invalid function: {}".format(node.id), getattr(node, "col_offset", 0))

            for child_node in ast.iter_child_nodes(node):
                self.generic_visit(child_node, inside_call)

    cnv = CleansingNodeVisitor()
    try:
        parsed_tree = ast.parse(text, mode=b"eval")
        cnv.visit(parsed_tree)
        compiled = compile(parsed_tree, filename="<embexpr>", mode=b"eval")
        return compiled
    except ParseError as e:
        raise e
    except Exception as e:
        raise ParseError("invalid expression: {}".format(e.message), 0)
