#!/usr/bin/env python3

# -------------------------------
# netflix/TestNetflix.py
# Copyrights (C) are for the weak
# Chris A. Timaeus
# -------------------------------

# -------
# imports
# -------
from io import TextIOBase
from io import StringIO
from unittest import main, \
                     TestCase

from Netflix import rmse, \
                    print_rmse, \
                    netflix_predict, \
                    netflix_print, \
                    load_data, \
                    netflix_solve

TRAINING_SET_AVG = 3.604289964420661


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


    # ----------
    # print_rmse
    # ----------
    # zero error
    def test_print_rmse_0(self):
        w = StringIO()
        movie_id = 1
        customer_id = 1
        calculated_rating = 1.0
        actual_rating = 1.0
        ratings = [(movie_id, customer_id, calculated_rating)]
        answers = {movie_id: {customer_id: actual_rating}}
        print_rmse(w, ratings, answers)
        self.assertEqual(w.getvalue(), "RMSE: 0.00\n")

    # real error
    def test_print_rmse_1(self):
        w = StringIO()
        movie_id = 1
        customer_id = 1
        calculated_rating = 1.5
        actual_rating = 1.0
        ratings = [(movie_id, customer_id, calculated_rating)]
        answers = {movie_id: {customer_id: actual_rating}}
        print_rmse(w, ratings, answers)
        self.assertEqual(w.getvalue(), "RMSE: 0.50\n")

    # inverted error
    def test_print_rmse_2(self):
        w = StringIO()
        movie_id = 1
        customer_id = 1
        calculated_rating = 1.0
        actual_rating = 1.5
        ratings = [(movie_id, customer_id, calculated_rating)]
        answers = {movie_id: {customer_id: actual_rating}}
        print_rmse(w, ratings, answers)
        self.assertEqual(w.getvalue(), "RMSE: 0.50\n")


    # ---------------
    # netflix_predict
    # ---------------
    # tests i/o format
    def test_netflix_predict_0(self):
        movie_id = 1
        customer_ids = [1, 2, 3]
        movie_data = {movie_id: {'year': 2000, 'avgr': TRAINING_SET_AVG}}
        customer_data = {1: {'avgr': {2000: 3.0}, 'caby': {2000: 3.0}},
                         2: {'avgr': {2000: 3.0}, 'caby': {2000: 3.0}},
                         3: {'avgr': {2000: 3.0}, 'caby': {2000: 3.0}}}
        r = netflix_predict(movie_id, customer_ids, movie_data, customer_data)
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 3)
        for x in r:
            self.assertTrue(isinstance(x, float))
            self.assertEqual(x, 3.0)

    # no movie release year
    def test_netflix_predict_1(self):
        movie_id = 1
        customer_ids = [1, 2, 3]
        movie_data = {movie_id: {'year': -1, 'avgr': 3}}
        customer_data = {1: {'avgr': {2000: 3.0}, 'caby': {2000: 3.0}},
                         2: {'avgr': {2000: 3.0}, 'caby': {2000: 3.0}},
                         3: {'avgr': {2000: 3.0}, 'caby': {2000: 3.0}}}
        r = netflix_predict(movie_id, customer_ids, movie_data, customer_data)
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 3)
        for x in r:
            self.assertTrue(isinstance(x, float))

    # negative predictions corrected to 1
    def test_netflix_predict_2(self):
        movie_id = 1
        customer_ids = [1, 2, 3]
        movie_data = {movie_id: {'year': 2000, 'avgr': -1.0}}
        customer_data = {1: {'avgr': {2000: -1.0}, 'caby': {2000: -1.0}},
                         2: {'avgr': {2000: -1.0}, 'caby': {2000: -1.0}},
                         3: {'avgr': {2000: -1.0}, 'caby': {2000: -1.0}}}
        r = netflix_predict(movie_id, customer_ids, movie_data, customer_data)
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 3)
        for x in r:
            self.assertTrue(isinstance(x, float))
            self.assertEqual(x, 1)

    # predictions over 5 corrected to 5
    def test_netflix_predict_3(self):
        movie_id = 1
        customer_ids = [1, 2, 3]
        movie_data = {movie_id: {'year': 2000, 'avgr': 6.0}}
        customer_data = {1: {'avgr': {2000: 6.0}, 'caby': {2000: 6.0}},
                         2: {'avgr': {2000: 6.0}, 'caby': {2000: 6.0}},
                         3: {'avgr': {2000: 6.0}, 'caby': {2000: 6.0}}}
        r = netflix_predict(movie_id, customer_ids, movie_data, customer_data)
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 3)
        for x in r:
            self.assertTrue(isinstance(x, float))
            self.assertEqual(x, 5)

    # movie_id's release_year NULL in movie_titles.txt
    def test_netflix_predict_4(self):
        movie_id = 4388
        customer_ids = [1, 2, 3]
        movie_data = {movie_id: {'year': 2000, 'avgr': TRAINING_SET_AVG}}
        customer_data = {1: {'avgr': {2000: 3.0}, 'caby': {2000: 3.0}},
                         2: {'avgr': {2000: 3.0}, 'caby': {2000: 3.0}},
                         3: {'avgr': {2000: 3.0}, 'caby': {2000: 3.0}}}
        r = netflix_predict(movie_id, customer_ids, movie_data, customer_data)
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 3)
        for x in r:
            self.assertTrue(isinstance(x, float))
            self.assertEqual(x, 3.0)


    # -------------
    # netflix_print
    # -------------
    # base test
    def test_netflix_print_0(self):
        w = StringIO()
        movie_id = 1
        customer_ids = [1, 2, 3]
        ratings = [3, 3, 3]

        netflix_print(movie_id, customer_ids, ratings, w)
        self.assertEqual(w.getvalue(), "1:\n3.0\n3.0\n3.0\n")

    # varied input should see appropriate changes
    def test_netflix_print_1(self):
        w = StringIO()
        movie_id = 7
        customer_ids = [3, 2, 1]
        ratings = [5.1, 4.2, 3.3]

        netflix_print(movie_id, customer_ids, ratings, w)
        self.assertEqual(w.getvalue(), "7:\n5.1\n4.2\n3.3\n")

    # ---------
    # load_data
    # ---------
    def test_load_data_0(self):
        movie_data, cust_data, answers = load_data()

    #--------------
    # netflix_solve
    #--------------
    # def test_netflix_solve_0(self):
    #     r = StringIO('1:\n30878\n2647871\n1283744\n')
    #     w = StringIO()
    #
    #     # answers = {movie_id: {customer_id: actual_rating}}
    #     netflix_solve(r, w)
    #     self.assertEqual(w.getvalue(), "1 10 1\n100 200 1\n201 210 1\n900 1000 1\n")


# ----
# main
# ----
if __name__ == "__main__": # pragma: no cover
    main()
