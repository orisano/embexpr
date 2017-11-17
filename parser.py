# coding: utf-8
import ast
import typing as ty

import six


def parse(text):  # type: (ty.Text) -> ast.AST
    SAFE_NODES = {
        ast.Add,
        ast.BinOp,
        ast.Call,
        ast.Compare,
        ast.Dict,
        ast.Div,
        ast.Expression,
        ast.List,
        ast.Load,
        ast.Mult,
        ast.Name,
        ast.Str,
        ast.Sub,
        ast.USub,
        ast.Tuple,
        ast.UnaryOp,
        ast.Set,
    }
    if six.PY34:
        SAFE_NODES.add(ast.NameConstant)

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

    class CleansingNodeVisitor(ast.NodeVisitor):
        def generic_visit(self, node, inside_call=False):
            if type(node) not in SAFE_NODES:
                raise ConditionSyntaxError("invalid condition ({})".format(text))
            elif isinstance(node, ast.Call):
                inside_call = True
            elif isinstance(node, ast.Name) and inside_call:
                if hasattr(builtins, node.id) and node.id not in CALL_WHITELIST:
                    raise ConditionSyntaxError("invalid function: {}".format(node.id))

            for child_node in ast.iter_child_nodes(node):
                self.generic_visit(child_node, inside_call)

    cnv = CleansingNodeVisitor()
    try:
        parsed_tree = ast.parse(text, mode=b"eval")
        cnv.visit(parsed_tree)
        compiled = compile(parsed_tree, filename="<condition>", mode=b"eval")
        return compiled
    except Exception as e:
        raise ConditionSyntaxError("invalid expression: {}".format(e.message))