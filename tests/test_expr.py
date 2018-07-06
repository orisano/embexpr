# coding: utf-8
from __future__ import unicode_literals

import embexpr


def test_parse_number_add():
    expr = embexpr.Expr("1 + 1")
    assert expr() == 2


def test_parse_number_sub():
    expr = embexpr.Expr("5 - 3")
    assert expr() == 2


def test_parse_number_mul():
    expr = embexpr.Expr("10 * -5")
    assert expr() == -50


def test_parse_number_div():
    expr = embexpr.Expr("10 / 2")
    assert expr() == 5.0


def test_parse_number_floor_div():
    expr = embexpr.Expr("30 // 7")
    assert expr() == 4


def test_parse_number_mod():
    expr = embexpr.Expr("9 % 4")
    assert expr() == 1


def test_parse_pow():
    expr = embexpr.Expr("2 ** 8")
    assert expr() == 256


def test_parse_not():
    expr = embexpr.Expr("not True")
    assert not expr()


def test_parse_gt():
    expr = embexpr.Expr("1 > 2")
    assert not expr()


def test_parse_gte():
    expr = embexpr.Expr("2 >= 2")
    assert expr()


def test_parse_lt():
    expr = embexpr.Expr("2 < 3")
    assert expr()


def test_parse_lte():
    expr = embexpr.Expr("0 <= -1")
    assert not expr()


def test_parse_eq():
    expr = embexpr.Expr("1 == 0")
    assert not expr()


def test_parse_neq():
    expr = embexpr.Expr("10 != 5")
    assert expr()


def test_parse_in():
    expr = embexpr.Expr("5 in [1, 2, 3, 4, 5]")
    assert expr()


def test_parse_not_in():
    expr = embexpr.Expr("'a' not in ['1', '2', '3']")
    assert expr()


def test_parse_string():
    expr = embexpr.Expr('"s" * 5')
    assert expr() == "sssss"


def test_parse_variable():
    expr = embexpr.Expr("a // 2")
    assert expr(a=10) == 5


def test_parse_multi_variable():
    expr = embexpr.Expr("x != y")
    assert expr(x=True, y=False)


def test_parse_builtin_func():
    expr = embexpr.Expr("len(s)")
    assert expr(s="test") == 4


def test_parse_method():
    expr = embexpr.Expr("s.startswith('NAME_')")
    assert expr(s="NAME_hoge")


def test_parse_keyword_arg():
    expr = embexpr.Expr("int('10', base=8)")
    assert expr() == 8


def test_parse_eval():
    expr = embexpr.Expr("eval('1')")
    try:
        assert expr() != 1
    except embexpr.ParseError as e:
        pass


def test_parse_multi_bytes():
    expr = embexpr.Expr("""s.startswith(u"こんにちは")""")
    assert expr(s="こんにちは世界")