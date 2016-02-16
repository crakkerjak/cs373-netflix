#!/usr/bin/env python3
from random import randint

EID = 'cat3263'
TARGET_DIR = 'netflix-tests/'
DATA_FILE = 'data/probe.txt'
INPUT_FILE = TARGET_DIR + 'RunNetflix.in'
OUTPUT_FILE = TARGET_DIR + 'RunNetflix.out'
TESTS_PER_CUSTOMER = 15

def main():
    with open(DATA_FILE, 'r') as data_file, \
         open(INPUT_FILE, 'w') as test_in, \
         open(OUTPUT_FILE, 'w') as test_out:
        test_count = 0
        line = iter(data_file)
        movie_id = next(line)[:-1]
        customer_ids = []
        while test_count < 2000:
            try:
                entry = next(line)
                if entry[-1] == ':':
                    movie_id = entry[:-1]

            except StopIteration:
                break

if __name__ == "__main__":
    main()
