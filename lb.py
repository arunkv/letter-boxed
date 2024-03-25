#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Letter Boxed Solver

#    Copyright 2024 Arun K Viswanathan
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0

import argparse
import logging
import os
import time

import nltk

logging.basicConfig(filename='lb.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

MIN_WORD_LENGTH = 4
MAX_WORD_LENGTH = float('inf')
SEARCH_DEPTH = 4
all_solutions = []


def parse_arguments():
    parser = argparse.ArgumentParser(description='Letter Boxed Solver')
    parser.add_argument('-t', '--top', type=str, required=True,
                        help='Letters on the top side of the box')
    parser.add_argument('-l', '--left', type=str, required=True,
                        help='Letters on the left side of the box')
    parser.add_argument('-b', '--bottom', type=str, required=True,
                        help='Letters on the bottom side of the box')
    parser.add_argument('-r', '--right', type=str, required=True,
                        help='Letters on the right side of the box')
    parser.add_argument('-m', '--min', type=int,
                        help='Minimum word length in solution (default: 4)')
    parser.add_argument('-x', '--max', type=int,
                        help='Maximum word length in solution (default: no limit)')
    parser.add_argument('-d', '--depth', type=int,
                        help='Search depth (default: 4)')
    parser.add_argument('-D', '--dict', type=str,
                        help='Dictionary file (default: /usr/share/dict/words)')
    return parser.parse_args()


def get_dictionary(dictionary):
    try:
        if os.path.isfile(dictionary):
            logging.info("Using custom dictionary: %s", dictionary)
            with open(dictionary) as f:
                return [line.strip() for line in f]
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        try:
            nltk_words = nltk.corpus.words.words()
        except LookupError:
            nltk.download('words')
            logging.info("Downloading NLTK corpus")
            nltk_words = nltk.corpus.words.words()
            logging.info("NLTK corpus downloaded with %s words", len(nltk_words))
        return nltk_words


def trim_dictionary(top, left, bottom, right, dictionary):
    # Initialize the trimmed dictionary
    trimmed_dictionary = []

    # For each word in the dictionary
    for word in dictionary:
        word = word.lower()

        valid = is_word_valid(word, left, bottom, right, top)

        if valid:
            trimmed_dictionary.append(word)

    # Return the trimmed dictionary
    logging.info("Dictionary trimmed to %s words", len(trimmed_dictionary))
    return trimmed_dictionary


# Test if a word is valid given the letters on the sides of the box
def is_word_valid(word, left, bottom, right, top):
    # Check if the word meets the minimum length
    if len(word) < MIN_WORD_LENGTH or len(word) > MAX_WORD_LENGTH:
        return False

    # Check if the word contains only the letters in the box without consecutive letters from the same side
    prev_set_name = None
    for letter in word:
        if letter in top:
            set_name = 't'
        elif letter in left:
            set_name = 'l'
        elif letter in bottom:
            set_name = 'b'
        elif letter in right:
            set_name = 'r'
        else:
            return False
        if set_name == prev_set_name:
            return False
        prev_set_name = set_name

    return True


# Solve the puzzle using the given letters and dictionary
def solve(top, left, bottom, right, dictionary):
    start_time = time.time()
    all_letters = set(top + left + bottom + right)
    search_words = trim_dictionary(top, left, bottom, right, dictionary)
    recursive_solve(all_letters, search_words, search_words, [])
    end_time = time.time()
    if len(all_solutions) == 0:
        print("No solutions found")
    else:
        for i, solution in enumerate(all_solutions, 1):
            print("{}. {}".format(i, solution))
    print("Solution search took {:.3f} seconds".format(end_time - start_time))
    logging.info("Solution search took %s seconds", end_time - start_time)


# Recursive function to solve the puzzle using a search space and a prefix solution
def recursive_solve(all_letters, all_search_words, search_words, solution=None, depth=0):
    solution = solution or []
    if depth != SEARCH_DEPTH:
        for word in search_words:
            potential_solution = solution + [word]
            used_letters = set(list(''.join(potential_solution)))
            if all_letters == used_letters:
                logging.info("Found solution: %s", potential_solution)
                all_solutions.append(potential_solution)
            else:
                last_letter = word[-1]
                next_search_words = [x for x in all_search_words if x[0] == last_letter]
                recursive_solve(all_letters, all_search_words, next_search_words, potential_solution, depth + 1)


if __name__ == '__main__':
    args = parse_arguments()
    top_letters = list(args.top.lower())
    left_letters = list(args.left.lower())
    bottom_letters = list(args.bottom.lower())
    right_letters = list(args.right.lower())
    logging.info("Puzzle letters: top=%s, left=%s, bottom=%s, right=%s",
                 top_letters, left_letters, bottom_letters, right_letters)

    if args.min:
        MIN_WORD_LENGTH = args.min
    if args.max:
        MAX_WORD_LENGTH = args.max
    if args.depth:
        SEARCH_DEPTH = args.depth
    selected_dict = args.dict or 'nltk'
    logging.info("Search parameters: min=%s, max=%s, depth=%s, dict=%s",
                 MIN_WORD_LENGTH, MAX_WORD_LENGTH, SEARCH_DEPTH, selected_dict)

    solve(top_letters, left_letters, bottom_letters, right_letters, get_dictionary(selected_dict))
