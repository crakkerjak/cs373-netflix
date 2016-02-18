#!/usr/bin/env python3

# -------------------------------
# netflix/Netflix.py
# Copyrights (C) are for the weak
# Chris A. Timaeus
# -------------------------------
from os.path import isfile
from requests import get
from pickle import load, loads
from numpy import mean, sqrt, square, subtract

CACHE_LOC = '/u/downing/public_html/netflix-caches'
CACHE_URL = 'http://www.cs.utexas.edu/u/downing/public_html/netflix-caches'
ANSWER_PICKLE =  'cat3263-a.pickle'

calculated_ratings = []


def netflix_predict(movie_id, customer_ids):
    """Predicts ratings for one movie and a list of customer_ids

    Simple implementation: for each customer, just returns the average rating
    from the training_set: 3.62.

    Args:
        movie_id: A movie id number in string format, including a colon at the
                  end.
        customer_ids: A list of customer_id's, again in string format.

    Returns:
        A list floats : the predicted ratings, rounded to 1/10th of a star
        predicted. For example:

        [3.0, 3.4, 4.0]

        If a key from the keys argument is missing from the dictionary,
        then that row was not found in the table.
    """
    ratings = []
    for customer_id in customer_ids:
        ratings.append(3.62)
    print ('len(ratings): ' + str(len(ratings)))
    return ratings


def netflix_print(movie_id, customer_ids, ratings, o_stream):
    global calculated_ratings

    o_stream.write(movie_id + '\n')
    for customer_id, rating in zip(customer_ids, ratings):
        o_stream.write(str(rating) + '\n')
        calculated_ratings.append((movie_id, customer_id, rating))


def print_rmse(o_stream):
    # read in answers
    answers = {}
    if isfile(CACHE_LOC + ANSWER_PICKLE):
        with open(CACHE_LOC + ANSWER_PICKLE, 'rb') as answer_file:
            answers = load(answer_file)
    else:
        answers = get(CACHE_URL + ANSWER_PICKLE).content
    print(type(answers))

    # format data for rmse calculation
    data = ([],[])
    for movie_id, customer_id, rating in calculated_ratings:
         data[0].append(rating)
         data[1].append(answers[movie_id][customer_id])

    # calculate, format and output rmse
    o_stream.write('RMSE: ' + '{:.2f}'.format(rmse(data)) + '\n')


def rmse (nums_1, nums_2) :
    return sqrt(mean(square(subtract(nums_1, nums_2))))


def netflix_solve(i_stream, o_stream):
    """
    i_stream a reader
    o_stream a writer
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
