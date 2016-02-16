#!/usr/bin/env python3

# -------------------------------
# projects/collatz/TestCollatz.py
# -------------------------------

# -------
# imports
# -------
from io       import StringIO
from unittest import main, TestCase

from Netflix  import  \
  function_1,       \
  # function_2,       \
  # function_3

# -----------
# TestNetflix
# -----------
class TestNetflix(TestCase):
  # ----------
  # function_1
  # ----------

  # test desc
  def test_function_1_1(self):
    pass
    # s    = "1 10\n"
    # i, j = netflix_read(s)
    # self.assertEqual(i,  1)
    # self.assertEqual(j, 10)

  # empty input. should skip and keep going.
  def test_function_1_2(self):
    pass
    # s    = ""
    # self.assertRaises(ValueError, collatz_read, s)


# ----
# main
# ----
if __name__ == "__main__": # pragma: no cover
  main()
