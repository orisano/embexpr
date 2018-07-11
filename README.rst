embexpr
============
.. image:: https://travis-ci.org/orisano/embexpr.svg?branch=master
    :target: https://travis-ci.org/orisano/embexpr

| safe embedded python expression parser (for mainly easy DSL or config file).

Getting Started
------------
.. code:: bash

  pip install embexpr


How to Use
------------
.. code:: python

  from embexpr import Expr, ParseError

  assert Expr('3 * 5')() == 15
  assert Expr('"foo" + "bar"')() == "foobar"
  assert Expr('len("example")')() == 7
  assert Expr('s.startswith("prefix_")')(s="prefix_suffix") == True

  try:
      Expr('eval("1")')()
  except ParseError as e:
      print(e)


Reference
------------
https://github.com/ansible/ansible/blob/devel/lib/ansible/template/safe_eval.py
http://stackoverflow.com/questions/12523516/using-ast-and-whitelists-to-make-pythons-eval-safe

License
------------
MIT
