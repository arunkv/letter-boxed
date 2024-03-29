#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Letter Boxed Solver

This module provides a solver for the New York Times Letter Boxed puzzle.
It uses the NLTK word list as the default dictionary and outputs all possible solutions.

Functions:
    parse_arguments(): Parses command line arguments.
    spinner(stop_event): Displays a spinner with elapsed time in the console.
    start_spinner(): Starts the spinner.
    stop_spinner(stop_event, spinner_thread): Stops the spinner.
    get_dictionary(dictionary): Returns a list of words from the specified dictionary.
    trim_dictionary(dictionary, args): Trims dictionary based on the letters on sides of the box.
    is_word_valid(word, args): Checks if a word is valid given the letters on the sides of the box.
    print_solutions(all_solutions): Prints the solutions.
    solve(args): Solves the puzzle using the given letters and dictionary.
    recursive_solve(args, all_letters, all_search_words, search_words, all_solutions,
                    solution, depth):
        Recursive function to solve the puzzle using a search space and a prefix solution.

Copyright 2024 Arun K Viswanathan
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""

import argparse
import logging
import os
import threading
import time

import nltk

import constants

logging.basicConfig(filename='lb.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_arguments():
    """
    Parse the command line arguments for the Letter Boxed Solver.

    Returns:
        parsed_args (argparse.Namespace): The parsed command line arguments.
    """
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


def spinner(stop_event):
    """
    Generates a spinner animation while the stop_event is not set.

    Parameters:
        stop_event (threading.Event): Event object that indicates whether the spinner should stop.

    Returns:
        None
    """
    start_time = time.time()
    while not stop_event.is_set():
        for frame in r'-\|/':
            elapsed_time = time.time() - start_time
            print('\r', frame, f' {elapsed_time:.2f}s', sep='', end='', flush=True)
            time.sleep(0.1)


def start_spinner():
    """
    Generate a spinner thread that runs concurrently with the main thread.

    Returns:
        stop_event (threading.Event): An event object to control the spinner thread.
        spinner_thread (threading.Thread): The thread running the spinner function.
    """
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(stop_event,))
    spinner_thread.start()
    return stop_event, spinner_thread


def stop_spinner(stop_event, spinner_thread):
    """
    Stop the spinner thread by setting the stop event and waiting for the thread to join.
    """
    stop_event.set()
    spinner_thread.join()
    print()  # Print a newline to clear the spinner


def get_dictionary(dictionary):
    """
    A function that retrieves a list of words from a custom dictionary file or the NLTK corpus.

    Parameters:
    - dictionary (str): The path to the custom dictionary file.

    Returns:
    - list: A list of words extracted from the custom dictionary file or the NLTK corpus.
    """
    try:
        if os.path.isfile(dictionary):
            logging.info("Using custom dictionary: %s", dictionary)
            with open(dictionary, 'r', encoding='utf-8') as word_file:
                return [line.strip() for line in word_file]
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


def trim_dictionary(dictionary, args):
    """
    Generates a new list of words from the given dictionary that meet the criteria specified by
    the arguments.

    Parameters:
        dictionary (list): A list of words to be filtered.
        args (argparse.Namespace):  The arguments passed to the function. It should have the
        following attributes:
            - min (int): The minimum length of the word.
            - max (int): The maximum length of the word.
            - top (set): The set of letters allowed on the top side of the box.
            - left (set): The set of letters allowed on the left side of the box.
            - bottom (set): The set of letters allowed on the bottom side of the box.
            - right (set): The set of letters allowed on the right side of the box.

    Returns:
        list: A new list of words that meet the specified criteria.

    Raises:
        None
    """
    trimmed_dictionary = [word for word in dictionary if is_word_valid(word, args)]
    logging.info("Dictionary trimmed to %s words", len(trimmed_dictionary))
    return trimmed_dictionary


def is_word_valid(word, args):
    """
    Check if a given word is valid based on the specified constraints.

    Parameters:
        word (str): The word to be checked.
        args (argparse.Namespace): The arguments passed to the function. It should have the
        following attributes:
            - min (int): The minimum length of the word.
            - max (int): The maximum length of the word.
            - top (set): The set of letters allowed on the top side of the box.
            - left (set): The set of letters allowed on the left side of the box.
            - bottom (set): The set of letters allowed on the bottom side of the box.
            - right (set): The set of letters allowed on the right side of the box.

    Returns:
        bool: True if the word is valid, False otherwise.
    """

    # Check if the word meets the minimum length
    if len(word) < args.min or len(word) > args.max:
        return False

    # Check if word contains only letters in the box without consecutive letters from same side
    sides = {'t': args.top, 'l': args.left, 'b': args.bottom, 'r': args.right}
    prev_set_name = None
    for letter in word:
        set_name = next((name for name, side in sides.items() if letter in side), None)
        if set_name is None or set_name == prev_set_name:
            return False
        prev_set_name = set_name

    return True


def print_solutions(all_solutions):
    """
    A function to print the solutions in a list, with special handling for empty list cases.
    """
    if len(all_solutions) == 0:
        print("No solutions found")
    else:
        for i, solution in enumerate(all_solutions, 1):
            print(f"{i}. {solution}")


# Solve the puzzle using the given letters and dictionary
def solve(args):
    """
    Solve the letter boxed puzzle using the given letters and dictionary.

    Parameters:
        args (argparse.Namespace): The arguments passed to the function. It should have the
        following attributes:
            - min (int): The minimum length of the word.
            - max (int): The maximum length of the word.
            - top (set): The set of letters allowed on the top side of the box.
            - left (set): The set of letters allowed on the left side of the box.
            - bottom (set): The set of letters allowed on the bottom side of the box.
            - right (set): The set of letters allowed on the right side of the box.
    :return: None
    """
    dictionary = get_dictionary(args.dict)
    args.all_search_words = args.search_words = trim_dictionary(dictionary, args)
    args.all_letters = set(args.top + args.left + args.bottom + args.right)
    stop_event, spinner_thread = start_spinner()
    all_solutions = recursive_solve(args, [], [])
    stop_spinner(stop_event, spinner_thread)
    print_solutions(all_solutions)


def recursive_solve(args, all_solutions, solution=None, depth=0):
    """
    A recursive function to solve a given problem using backtracking.

    Args:
        args: The arguments for the recursive solve function.
        all_solutions: A list to store all the found solutions.
        solution: The current solution being built (default is None).
        depth: The current depth of recursion (default is 0).

    Returns:
        list: A list of all the found solutions.
    """
    solution = solution or []
    if depth != args.depth:
        for word in args.search_words:
            potential_solution = solution + [word]
            used_letters = set(list(''.join(potential_solution)))
            if args.all_letters == used_letters:
                logging.info("Found solution: %s", potential_solution)
                all_solutions.append(potential_solution)
            else:
                last_letter = word[-1]
                args.search_words = [x for x in args.all_search_words
                                     if x[0] == last_letter and x != word]
                all_solutions = recursive_solve(args, all_solutions, potential_solution, depth + 1)
    return all_solutions


if __name__ == '__main__':
    solve(parse_arguments())
