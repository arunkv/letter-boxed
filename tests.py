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


class TestLetterBoxedSolver(unittest.TestCase):
    def setUp(self):
        self.top = 'abcd'
        self.left = 'efgh'
        self.bottom = 'ijkl'
        self.right = 'mnop'
        self.dictionary = ['ab', 'cd', 'ef', 'gh', 'ij', 'kl', 'mn', 'op']

    def test_is_word_valid(self):
        lb.MIN_WORD_LENGTH = 2
        self.assertFalse(is_word_valid('ab', self.left, self.bottom, self.right, self.top))
        self.assertFalse(is_word_valid('zz', self.left, self.bottom, self.right, self.top))
        self.assertTrue(is_word_valid('ae', self.left, self.bottom, self.right, self.top))

    def test_trim_dictionary(self):
        trimmed = trim_dictionary(self.top, self.left, self.bottom, self.right, self.dictionary)
        self.assertEqual(trimmed, [])

    def test_recursive_solve(self):
        all_letters = set(self.top + self.left + self.bottom + self.right)
        search_words = trim_dictionary(self.top, self.left, self.bottom, self.right, self.dictionary)
        recursive_solve(all_letters, search_words, search_words, [])
        self.assertEqual(len(lb.ALL_SOLUTIONS), 0)


if __name__ == '__main__':
    unittest.main()
