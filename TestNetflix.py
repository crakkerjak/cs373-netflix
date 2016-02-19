#!/usr/bin/env python3

# -------------------------------
# netflix/TestNetflix.py
# Copyrights (C) are for the weak
# Chris A. Timaeus
# -------------------------------

# -------
# imports
# -------
from io import StringIO
from unittest import main, \
                     TestCase

from Netflix import rmse, \
                    print_rmse, \
                    netflix_predict, \
                    netflix_print, \
                    load_data, \
                    netflix_solve


# -----------
# TestNetflix
# -----------
class TestNetflix(TestCase):


    # ----
    # rmse
    # ----

    # 0-error
    def test_rmse_0(self):
        n1, n2 = [1, 2, 3], [1, 2, 3]
        r = rmse(n1, n2)
        self.assertEqual(r, 0)

    # off by 1
    def test_rmse_1(self):
        n1, n2 = [1, 2, 3], [2, 3, 4]
        r = rmse(n1, n2)
        self.assertEqual(r, 1)

    # lists reversed
    def test_rmse_2(self):
        n1, n2 = [2, 3, 4], [1, 2, 3]
        r = rmse(n1, n2)
        self.assertEqual(r, 1)

    # lists of length 1
    def test_rmse_3(self):
        n1, n2 = [1], [1]
        r = rmse(n1, n2)
        self.assertEqual(r, 0)

    # negative numbers
    def test_rmse_4(self):
        n1, n2 = [1, 1, 1], [-1, -1, -1]
        r = rmse(n1, n2)
        self.assertEqual(r, 2)

    #floats
    def test_rmse_5(self):
        n1, n2 = [-1.5], [1.5]
        r = rmse(n1, n2)
        self.assertEqual(r, 3)



    # empty input. should skip and keep going.
    def test_netflix_solve_2(self):
        pass
        # s        = ""
        # self.assertRaises(ValueError, collatz_read, s)


# ----
# main
# ----
if __name__ == "__main__": # pragma: no cover
    main()
