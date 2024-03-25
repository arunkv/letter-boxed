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

import constants

logging.basicConfig(filename='lb.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


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
    parsed_args = parser.parse_args()
    parsed_args.top = list(str(parsed_args.top).lower())
    parsed_args.left = list(str(parsed_args.left).lower())
    parsed_args.bottom = list(str(parsed_args.bottom).lower())
    parsed_args.right = list(str(parsed_args.right).lower())
    logging.info("Puzzle letters: top=%s, left=%s, bottom=%s, right=%s",
                 parsed_args.top, parsed_args.left, parsed_args.bottom, parsed_args.right)

    parsed_args.min = parsed_args.min or constants.MIN_WORD_LENGTH
    parsed_args.max = parsed_args.max or constants.MAX_WORD_LENGTH
    parsed_args.depth = parsed_args.depth or constants.SEARCH_DEPTH
    parsed_args.dict = parsed_args.dict or 'nltk'
    logging.info("Search parameters: min=%s, max=%s, depth=%s, dict=%s",
                 parsed_args.min, parsed_args.max, parsed_args.depth, parsed_args.dict)
    return parsed_args


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


# Prune invalid words from the dictionary based on the letters on the sides of the box
def trim_dictionary(dictionary, args):
    trimmed_dictionary = [word for word in dictionary if is_word_valid(word, args)]
    logging.info("Dictionary trimmed to %s words", len(trimmed_dictionary))
    return trimmed_dictionary


# Test if a word is valid given the letters on the sides of the box
def is_word_valid(word, args):
    # Check if the word meets the minimum length
    if len(word) < args.min or len(word) > args.max:
        return False

    # Check if the word contains only the letters in the box without consecutive letters from the same side
    sides = {'t': args.top, 'l': args.left, 'b': args.bottom, 'r': args.right}
    prev_set_name = None
    for letter in word:
        set_name = next((name for name, side in sides.items() if letter in side), None)
        if set_name is None or set_name == prev_set_name:
            return False
        prev_set_name = set_name

    return True


# Solve the puzzle using the given letters and dictionary
def solve(args):
    dictionary = get_dictionary(args.dict)
    start_time = time.time()
    search_words = trim_dictionary(dictionary, args)
    all_letters = set(args.top + args.left + args.bottom + args.right)
    all_solutions = recursive_solve(args, all_letters, search_words, search_words, [], [])
    end_time = time.time()
    if len(all_solutions) == 0:
        print("No solutions found")
    else:
        for i, solution in enumerate(all_solutions, 1):
            print("{}. {}".format(i, solution))
    print("Solution search took {:.3f} seconds".format(end_time - start_time))
    logging.info("Solution search took %s seconds", end_time - start_time)


# Recursive function to solve the puzzle using a search space and a prefix solution
def recursive_solve(args, all_letters, all_search_words, search_words, all_solutions, solution=None, depth=0):
    solution = solution or []
    if depth != args.depth:
        for word in search_words:
            potential_solution = solution + [word]
            used_letters = set(list(''.join(potential_solution)))
            if all_letters == used_letters:
                logging.info("Found solution: %s", potential_solution)
                all_solutions.append(potential_solution)
            else:
                last_letter = word[-1]
                next_search_words = [x for x in all_search_words if x[0] == last_letter and x != word]
                all_solutions = recursive_solve(args, all_letters, all_search_words, next_search_words,
                                                all_solutions, potential_solution, depth + 1)
    return all_solutions


if __name__ == '__main__':
    solve(parse_arguments())
