#!/usr/bin/env python3
from pickle import load
from random import randint, \
                   sample
from shutil import copy


EID = 'cat3263'
TARGET_DIR = 'netflix-tests/'
DATA_FILE = 'data/probe.txt'
ANS_PICKLE = 'data/' + EID + '-a.pickle'
INPUT_FILE = 'RunNetflix.in'
OUTPUT_FILE = 'RunNetflix.out'
MAX_TESTS = 2000


def gen_tests():
    with open(DATA_FILE, 'r') as data_file, \
         open(INPUT_FILE, 'w') as test_in, \
         open(OUTPUT_FILE, 'w') as test_out:
        with open(ANS_PICKLE, 'rb') as pickled_answers:
            answers = load(pickled_answers)
        line_count = 0
        line = iter(data_file)
        movie_id = next(line)[:-1]
        customer_ids = []
        while line_count < MAX_TESTS:
            try:
                entry = next(line).strip()
                if entry[-1] == ':':
                    line_count += maybe_add(movie_id, customer_ids, answers,
                                            test_in, test_out)
                    movie_id = entry
                    customer_ids = []
                else:
                    customer_ids.append(entry)
            except StopIteration:
                break
        print(line_count)


def maybe_add(movie_id, customer_ids, answers, test_in, test_out):
    TOTAL_CUSTOMERS = 16938 # grep ':' probe.txt | wc -l
    RATINGS_PER_MOVIE = 5
    CUSTOMERS_NEEDED = MAX_TESTS // RATINGS_PER_MOVIE
    lines_added = 0
    if randint(1, 16938) < CUSTOMERS_NEEDED:
        customer_ids = sample(customer_ids,
                              min(RATINGS_PER_MOVIE - 1, len(customer_ids)))
        write_tests(movie_id, customer_ids, test_in)
        write_answers(movie_id, customer_ids, answers, test_out)
        lines_added += len(customer_ids) + 1
    return lines_added


def write_tests(movie_id, customer_ids, test_in):
    print(movie_id, file=test_in)
    for customer_id in customer_ids:
        print(customer_id, file=test_in)


def write_answers(movie_id, customer_ids, answers, test_out):
    print(movie_id, file=test_out)
    for customer_id in customer_ids:
        print(str(answers[movie_id[:-1]][customer_id]), file=test_out)


def copy_files():
    if TARGET_DIR != '':
      for file_name in [INPUT_FILE, OUTPUT_FILE]:
        copy(file_name, TARGET_DIR + '/' + EID + '-' + file_name)


if __name__ == "__main__":
    gen_tests()
    copy_files()
