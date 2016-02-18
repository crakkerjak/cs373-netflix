#!/usr/bin/env python3

# -------------------------------
# netflix/Netflix.py
# Copyrights (C) are for the weak
# Chris A. Timaeus
# -------------------------------
from os.path import isfile
from urllib.request import urlopen
# from requests import get
from pickle import load, \
                   loads
from numpy import mean, \
                  sqrt, \
                  square, \
                  subtract

CACHE_LOC = '/u/downing/public_html/netflix-caches/'
CACHE_URL = 'http://www.cs.utexas.edu/users/downing/netflix-caches/'
ANSWER_PICKLE =  'cat3263-a.pickle'

calculated_ratings = []


def netflix_predict(movie_id, customer_ids):
    """Predicts ratings for one movie and a list of customer_ids

    Simple implementation: for each customer, just returns the same arbitrary
    rating for every (movie, customer).

    Args:
        movie_id: A movie id number in string format, including a colon at the
                  end.
        customer_ids: A list of customer_id's, again in string format.

    Returns:
        A list floats, the predicted ratings rounded to 1/10th of a star
        predicted. For example:

        [3.0, 3.4, 4.0]
    """
    ratings = []
    for customer_id in customer_ids:
        ratings.append(3.5)
    return ratings


def netflix_print(movie_id, customer_ids, ratings, o_stream):
    """Records predicted ratings for one movie and a list of customer_ids

    Writes the movie_id, colon included, to the output stream, then writes each
    rating to the output stream, saving a (movie_id, customer_id, rating) tuple
    for each as it goes.

    Args:
        movie_id: A movie id number in string format, including a colon at the
                  end.
        customer_ids: A list of customer_id's, again in string format.
        ratings: A list of the ratings predicted for each customer.
    """
    global calculated_ratings

    o_stream.write(movie_id + '\n')
    for customer_id, rating in zip(customer_ids, ratings):
        o_stream.write(str(rating) + '\n')
        calculated_ratings.append((movie_id, customer_id, rating))


def print_rmse(o_stream):
    """Creates a string representation of the (root mean squared error).

    Collates predicted and actual ratings, then prints a labeled line with the
    rmse for all predicted ratings to the output stream.

    Args:
        o_stream: A writer, the output stream.
    """
    # read in answers
    answers = {}
    if isfile(CACHE_LOC + ANSWER_PICKLE):
        with open(CACHE_LOC + ANSWER_PICKLE, 'rb') as answer_file:
            answers = load(answer_file)
    else:
        # answers = loads(get(CACHE_URL + ANSWER_PICKLE).content)
        answers = loads(urlopen(CACHE_URL + ANSWER_PICKLE).read())

    # format data for rmse calculation
    data = ([],[])
    for movie_id, customer_id, rating in calculated_ratings:
         data[0].append(rating)
         data[1].append(answers[movie_id][customer_id])

    # calculate, format and output rmse
    error = rmse(data[0], data[1])
    o_stream.write('RMSE: ' + '{:.2f}'.format(error) + '\n')


def rmse (nums_1, nums_2) :
    """Calculates the root mean squared error between two iterable containers
    of numbers.

    Requires numpy.

    Args:
        nums_1, nums_2: Two iterable containers of floats or integers.

    Returns:
        The root mean squared error as a raw float value.
    """
    return sqrt(mean(square(subtract(nums_1, nums_2))))


def netflix_solve(i_stream, o_stream):
    """Creates prediction output for any valid input for the Netflix Prize
    problem.

    Args:
        i_stream: The input stream.
        o_stream: The output stream.
    """
    # pre-conditions
    assert hasattr(i_stream, 'read')
    assert hasattr(o_stream, 'write')

    customer_ids = []
    for line in i_stream:
        line = line.strip()
        if line[-1] == ':':
            if len(customer_ids) > 0:
                netflix_print(movie_id,
                              customer_ids,
                              netflix_predict(movie_id, customer_ids),
                              o_stream)
            movie_id = line
            customer_ids = []
        else:
            customer_ids.append(line)

    netflix_print(movie_id,
                  customer_ids,
                  netflix_predict(movie_id, customer_ids),
                  o_stream)
    print_rmse(o_stream)
