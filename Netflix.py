#!/usr/bin/env python3

# -------------------------------
# netflix/Netflix.py
# Copyrights (C) are for the weak
# Chris A. Timaeus
# -------------------------------
from os.path import isfile
from urllib.request import urlopen
from pickle import load, \
                   loads
from numpy import mean, \
                  sqrt, \
                  square, \
                  subtract

CACHE_LOC = '/u/downing/public_html/netflix-caches/'
CACHE_URL = 'http://www.cs.utexas.edu/users/downing/netflix-caches/'
ANSWER_PICKLE = 'cat3263-a.pickle'
MOVIE_PICKLE = 'cat3263-mov-2.pickle'
CUSTOMER_PICKLE = 'cat3263-cust-2.pickle'
TRAINING_SET_AVG = 3.604289964420661

calculated_ratings = []


def netflix_predict(movie_id, customer_ids, movie_data, cust_data):
    """Predicts ratings for one movie and a list of customer_ids

    Uses the customer_average, by year if a vailable, offset by the difference
    between the average rating across the entire training_set and the average
    rating for the movie.

    Args:
        movie_id: A movie id number in string format, including a colon at the
                  end.
        customer_ids: A list of customer_id's, again in string format.

    Returns:
        A list of floats, the predicted ratings rounded to 1/10th of a star
        predicted. For example:

        [3.0, 3.4, 4.0]
    """
    ratings = []
    for customer_id in customer_ids:
        # ---------------------------------------------------------------------
        # these 3 lines yield a 0.97 RMSE on probe.txt:
        # m_ofs = movie_data[movie_id]['avgr'] - TRAINING_SET_AVG
        # c_ofs = cust_data[customer_id]['avgr'] - TRAINING_SET_AVG
        # ratings.append(TRAINING_SET_AVG + m_ofs + c_ofs)
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # but this one gets 0.90 :)
        # ratings.append(cust_data[customer_id]['caby'][movie_data[movie_id]['year']])
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # and these get 0.83309598542714313751
        release_year = movie_data[movie_id]['year']
        if release_year != -1: # release year was NULL in training_set
            customer_average = cust_data[customer_id]['caby'][release_year]
        else:
            customer_average = cust_data[customer_id]['avgr']
        ratings.append(customer_average +
                       movie_data[movie_id]['avgr'] - TRAINING_SET_AVG)
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

    o_stream.write(str(movie_id) + ':\n')
    for customer_id, rating in zip(customer_ids, ratings):
        rating = '{:.1f}'.format(rating)
        o_stream.write(str(rating) + '\n')
        calculated_ratings.append((movie_id, customer_id, float(rating)))


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
        answers = loads(urlopen(CACHE_URL + ANSWER_PICKLE).read())

    # format data for rmse calculation
    data = ([],[])
    for movie_id, customer_id, rating in calculated_ratings:
         data[0].append(rating)
         data[1].append(answers[int(movie_id)][int(customer_id)])

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


def load_data():
    movie_data = {}
    cust_data = {}
    # load movie data cache
    if isfile(CACHE_LOC + MOVIE_PICKLE):
        with open(CACHE_LOC + MOVIE_PICKLE, 'rb') as movie_file:
            movie_data = load(movie_file)
    else:
        movie_data = loads(urlopen(CACHE_URL + MOVIE_PICKLE).read())
    # load customer data cache
    if isfile(CACHE_LOC + CUSTOMER_PICKLE):
        with open(CACHE_LOC + CUSTOMER_PICKLE, 'rb') as cust_file:
            cust_data = load(cust_file)
    else:
        cust_data = loads(urlopen(CACHE_URL + CUSTOMER_PICKLE).read())
    return(movie_data, cust_data)


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
    movie_data, cust_data = load_data()
    # parse input
    for line in i_stream:
        line = line.strip()
        if line[-1] == ':':
            if len(customer_ids) > 0:
                # see the future (or the past, actually)
                predictions = netflix_predict(movie_id, customer_ids,
                                              movie_data, cust_data)
                # print current movie's output
                netflix_print(movie_id, customer_ids, predictions, o_stream)
            movie_id = int(line[:-1])
            customer_ids = []
        else:
            customer_ids.append(int(line))
    # predict ratings for final movie
    predictions = netflix_predict(movie_id, customer_ids,
                                  movie_data, cust_data)
    # print final movie's output
    netflix_print(movie_id, customer_ids, predictions, o_stream)
    print_rmse(o_stream)
