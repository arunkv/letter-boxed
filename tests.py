#    Copyright 2024 Arun K Viswanathan
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0

import unittest

import lb
from lb import is_word_valid, recursive_solve, trim_dictionary


class DotDict(dict):
    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        del self[item]



class TestLetterBoxedSolver(unittest.TestCase):
    def setUp(self):
        self.args = DotDict()
        self.args.top = 'abcd'
        self.args.left = 'efgh'
        self.args.bottom = 'ijkl'
        self.args.right = 'mnop'
        self.args.min = 2
        self.args.max = 2
        self.dictionary = ['ab', 'cd', 'ef', 'gh', 'ij', 'kl', 'mn', 'op']

    def test_is_word_valid(self):
        self.assertFalse(is_word_valid('ab', self.args))
        self.assertFalse(is_word_valid('zz', self.args))
        self.assertTrue(is_word_valid('ae', self.args))

    def test_trim_dictionary(self):
        trimmed = trim_dictionary(self.dictionary, self.args)
        self.assertEqual(trimmed, [])

    def test_recursive_solve(self):
        all_letters = set(self.args.top + self.args.left + self.args.bottom + self.args.right)
        search_words = trim_dictionary(self.dictionary, self.args)
        all_solutions = recursive_solve(self.args, all_letters, search_words, search_words, [])
        self.assertEqual(len(all_solutions), 0)


if __name__ == '__main__':
    unittest.main()
