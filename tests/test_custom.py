# The MIT License (MIT)
# Copyright (c) 2020 by Brockmann Consult GmbH and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest

from nc2zarr.custom import load_custom_func

my_custom_var = 14


def my_custom_func(*args, **kwargs):
    return 14


class LoadCustomFunctionTest(unittest.TestCase):

    def test_ok(self):
        func = load_custom_func("tests.test_custom:my_custom_func")
        self.assertEqual(14, func())

    def test_invalid(self):
        with self.assertRaises(ValueError) as cm:
            load_custom_func("tests.test_custom.my_custom_func")
        self.assertEqual('func_ref "tests.test_custom.my_custom_func" is invalid',
                         f"{cm.exception}")

    def test_module_not_found(self):
        with self.assertRaises(ValueError) as cm:
            load_custom_func("test.test_custom:my_custom_func")
        self.assertEqual('module for function "test.test_custom:my_custom_func" not found',
                         f"{cm.exception}")

    def test_function_not_found(self):
        with self.assertRaises(ValueError) as cm:
            load_custom_func("tests.test_custom:my_custom_fun")
        self.assertEqual('function "tests.test_custom:my_custom_fun" not found',
                         f"{cm.exception}")

    def test_not_a_function(self):
        with self.assertRaises(ValueError) as cm:
            load_custom_func("tests.test_custom:my_custom_var")
        self.assertEqual('"tests.test_custom:my_custom_var" is not callable',
                         f"{cm.exception}")
