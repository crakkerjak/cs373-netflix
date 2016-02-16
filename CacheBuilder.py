#!/usr/bin/env python3

# imports
from array import array
from operator import itemgetter
from shutil import rmtree
from os import mkdir, \
               scandir
from datetime import datetime, \
                     timedelta
import sys
import threading
import pickle

# 'constants'
DATA_PATH = './data/'
EID = 'cat3263'


def all_avg_movie_ratings():
    """
    return an array of the average rating for all movies
    movie_id is the array index
    """
    print('Calculating average rating for each movie...')
    avg_ratings = array('f',[0])
    for movie_id in range(1, 17771):
        ratings = fetch_ratings_for_movie(movie_id)
        avg_ratings.append(avg_movie_rating(ratings))
    return avg_ratings


def avg_movie_rating(ratings):
    """
    return the average rating from a movie rating dict
    """
    s = 0.0
    for c in ratings:
        s += ratings[c][0]
    return s / len(ratings)


def all_movie_rating_trends():
    ratings_over_time = {}
    for entry in scandir(DATA_PATH + '/training_set'):
        print(entry.name)
        with open(entry.path) as f:
            m, *ratings = f.readlines()
            r = []
            for l in ratings:
                _, rating, date = l.strip().split(',')
                r.append((int(rating), date))
            ratings_over_time[int(m.strip()[:-1])] = movie_ratings_trend(r)
    return ratings_over_time


def movie_ratings_trend(ratings):
    x_intercept = datetime.strptime('2005-12-31', '%Y-%m-%d')
    ratings.sort(key=itemgetter(1))
    sample_size = max(len(ratings) // 10, 1)
    oldest = ratings[0:sample_size]
    newest = ratings[len(ratings) - sample_size:len(ratings)]
    x1 = average_date(oldest)
    y1 = sum(r[0] for r in oldest) / sample_size
    x2 = average_date(newest)
    y2 = sum(r[0] for r in newest) / sample_size
    if x1 == x2:
        slope = 0
    else:
        slope = (y2 - y1) / (x2 - x1).days
        y_intercept = y2 + slope * (x_intercept - x2).days
    return (slope, y_intercept)


def average_date(ratings):
    if len(ratings) == 1:
        return datetime.strptime(ratings[0][1], '%Y-%m-%d')
    dates = [datetime.strptime(r[1], '%Y-%m-%d') for r in ratings]
    deltas = [dates[i] - dates[0] for i in range(1, len(dates))]
    avg_delta = sum(deltas, timedelta(0)) / len(deltas)
    return dates[0] + avg_delta


def fetch_ratings_for_movie(movie_id):
    """
    read and return all ratings for a given movie as {customer_id:(r,d)}
    """
    with open(DATA_PATH + 'training_set/mv_' + str(movie_id).zfill(7)
              + '.txt','r') as mv:
        ratings = {}
        for l in mv.readlines()[1:]:
            c, r, d = l.strip().split(',')
            ratings[int(c)] = (int(r), d)
            return ratings


def convert_training_set():
    """
    converts training_set files into an analog version organized by customer_id
    """
    # fair warning - guard against my.self
    print('Converting movie data to customer data...')
    print('This will take a long time and will start by removing any'
          + 'customer_data directory in the DATA_PATH.')
    really = input('Continue? [yn]: ')
    if really != 'y':
        print('Canceled.')
        return

    rmtree(DATA_PATH + 'customer_data/')
    mkdir(DATA_PATH + 'customer_data/')

    threads = [threading.Thread(target=convert_range, args=(1, 1000,))]
    for start in range (1000, 18000, 1000):
        threads.append(threading.Thread(target=convert_range,
                       args=(start, start + 1000)))
    threads.append(threading.Thread(target=convert_range, args=(17000, 17771)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def convert_range(start, stop):
    """
    start, stop two ints
    used by convert_training_set to divide up full range for threading
    """
    for movie_id in range(start, stop):
        this_movies_ratings = fetch_ratings_for_movie(movie_id)
        print('--Processing movie_id: ' + str(movie_id) + ', length: '
              + str(len(this_movies_ratings)))
        for c in this_movies_ratings.keys():
            with open(DATA_PATH + 'customer_data/c_' + str(c).zfill(7)
                      + '.txt','a') as f:
                r, d = this_movies_ratings[c]
                print(str(movie_id) + ',' + str(r) + ',' + d, file=f)


def all_avg_customer_ratings():
    """
    ratings a dict: {customer_id:{movie_id:(rating, date))}
    return average rating by each customer: {customer_id:avg_rating}
    """
    avg_ratings = {}
    for entry in scandir(DATA_PATH + '/customer_data'):
        c = int(entry.name[2:9])
        avg_ratings[c] = avg_customer_rating(c)
    return avg_ratings


def avg_customer_rating(customer_id):
    """
    ratings a dict: {movie_id:(rating, date)}
    return the average rating from a customer rating dict
    """
    s = 0.0
    ratings = fetch_ratings_for_customer(customer_id)
    for m, r in ratings.items():
        s += ratings[m][0]
    return s / len(ratings)


def fetch_ratings_for_customer(customer_id):
    """
    read and return all ratings for a given customer as {movie_id:(r,d)}
    """
    with open(DATA_PATH + 'customer_data/c_' + str(customer_id).zfill(7)
              + '.txt','r') as cf:
        ratings = {}
        for l in cf.readlines():
            m, r, d = l.strip().split(',')
            ratings[int(m)] = (int(r), d)
    return ratings

def movie_age_preferences():
    '''
    stores a line in point-slope form based on a the oldest and newest movies
    a customer has reviewed
    dict format: {customer_id:(slope, calc'd rating at x_intercept)}
    '''
    age_preferences = {}
    x_intercept = 2005
    ma = load_pickle('ma')
    for entry in scandir(DATA_PATH + '/customer_data'):
        c = int(entry.name[2:9])
        ratings = fetch_ratings_for_customer(c)
        ra = []
        for m in ratings.keys():
            if not ma[m] == -1 :
                ra.append((ma[m],ratings[m][0]))
        ra = sorted(ra, reverse=True)
        sample_size = max(len(ra) // 10, 1)
        oldest = ra[0:sample_size]
        newest = ra[len(ra) - sample_size:len(ra)]
        x1 = sum(r[0] for r in oldest) / sample_size
        y1 = sum(r[1] for r in oldest) / sample_size
        x2 = sum(r[0] for r in newest) / sample_size
        y2 = sum(r[1] for r in newest) / sample_size
        if x1 == x2:
            slope = 0
        else:
            slope = (y2 - y1) / (x1 - x2)
        y_intercept = x2 * slope + y2
        age_preferences[c] = (slope, y_intercept)
    return age_preferences


def sort_all_customer_files():
    '''
    sorts all customer files in customer_data directory
    '''
    for entry in scandir(DATA_PATH + '/customer_data'):
        c = int(entry.name[2:9])
        sort_customer_file(c)


def sort_customer_file(customer_id):
    '''
    customer_id an int
    sorts ratings in a customer file by date
    '''
    ratings = fetch_ratings_for_customer(customer_id)
    # sort by date
    ratings = sorted(ratings.items(), key=lambda r: r[1][1])
    with open(DATA_PATH + 'customer_data/c_' + str(customer_id).zfill(7)
              + '.txt','w') as cf:
        for m, r in ratings:
            print(str(m) + ',' + str(r[0]) + ',' + r[1], file=cf)


def all_rating_dates():
    dates = {}
    for entry in scandir(DATA_PATH + '/customer_data'):
        print(entry.name)
        c = int(entry.name[2:9])
        with open(entry.path,'r') as cf:
            for l in cf.readlines():
                m, _, d = l.strip().split(',')
                dates[c] = {int(m):d}
    return dates


def all_movie_ages():
    '''
    returns movie ages (in 2005) in an array, index with movie_id
    movies with no age in movie_titles.txt have a value of -1
    '''
    with open(DATA_PATH + 'movie_titles.txt', 'r') as f:
        ages = array('i',[0])
        for l in f.readlines():
            age = l.split(',')[1]
            if age.isdigit():
                ages.append(2005 - int(age))
            else:
                ages.append(-1)
        return ages


def coalesce_movie_data():
    ma = load_pickle('ma')
    avgmr = load_pickle('avgmr')
    amrt = load_pickle('amrt')

    movie_data = {}
    for m in range(1, 17771):
        movie_data[m] = {'age':ma[m],
                         'avg_rating':avgmr[m],
                         'trend':amrt[m]}
    return movie_data


def coalesce_customer_data():
    avgcr = load_pickle('avgcr')
    cmap = load_pickle('cmap')
    ard = load_pickle('ard')

    customer_data = {}
    for c in avgcr.keys():
        customer_data[c] = {'avg_rating':avgcr[c],
                            'trend':cmap[c],
                            'rating_dates':ard[c]}
    return customer_data


def answers():
    """
    returns a dict of actual ratings for reviews in probe.txt
    format: {movie_id:{customer_id:rating)}}
    """
    answers = {}
    with open(DATA_PATH + 'probe.txt') as probe:
        lines = probe.readlines()
        # parse each line in probe.txt
        ratings = {}
        for l in lines:
            l = l.strip()
            if l[-1] == ':': # line is a movie_id
                movie_id = l[:-1]
                ratings = fetch_ratings_for_movie(movie_id)
                answers[movie_id] = {}
            else: # line is customer_id, add rating to dict
                c = int(l)
                answers[movie_id][c] = ratings[c][0]
    return answers


def write_pickle(obj, name):
    '''
    obj an object
    name a string
    writes an object to a pickle file
    '''
    with open(DATA_PATH + EID + '-' + name + '.pickle','wb') as f:
        pickle.dump(obj, f)


def load_pickle(name):
    '''
    name a string
    reads an object from a pickle file
    '''
    with open(DATA_PATH + EID + '-' + name + '.pickle','rb') as f:
        obj = pickle.load(f)
    return obj


def validate_args(args):
    '''
    args list of strings
    validates command line arguments - not implemented
    '''
    return args


if __name__ == '__main__':
    args = validate_args(sys.argv)
    if len(args) > 1:
        if '-m2c' in args:
            convert_training_set()
        elif '-scf' in args:
            sort_all_customer_files()
        elif '-ma' in args:
            write_pickle(all_movie_ages(), 'ma')
        elif '-avgmr' in args:
            write_pickle(all_avg_movie_ratings(), 'avgmr')
        elif '-amrt' in args:
            write_pickle(all_movie_rating_trends(), 'amrt')
        elif '-avgcr' in args:
            write_pickle(all_avg_customer_ratings(), 'avgcr')
        elif '-cmap' in args:
            write_pickle(movie_age_preferences(), 'cmap')
        elif '-ard' in args:
            write_pickle(all_rating_dates(), 'ard')
        elif '-co' in args:
            write_pickle(coalesce_movie_data(), 'mov')
            write_pickle(coalesce_customer_data(), 'cust')
        elif '-a' in args:
            write_pickle(answers(), 'a')
        elif '-test' in args:
            amrt = load_pickle('amrt')
            print(type(amrt))
            print(sorted(amrt.keys()))
        print('Done.')
    else:
        print('usage: python3 CacheBuilder.py <-m2c,-scf,-ma,-avgmr,-amrot,'
              + '-avgcr,-cmap,-ard,-co,-a>')
