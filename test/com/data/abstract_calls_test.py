import time
import unittest
from com.data.abstract_calls import AbstractGetCall


class Test(unittest.TestCase):

    def setUp(self):
        AbstractGetCall.__abstractmethods__ = set()
        self.agc = AbstractGetCall()
        pass

    def tearDown(self):
        pass

    def test_query_string_sort(self):
        params = {'b': '2+b', 'a': '1&m', 'c': '3=j'}
        result = AbstractGetCall._canonical_query_string(params)
        self.assertEqual('a=1%26m&b=2%2Bb&c=3%3Dj', result)

    def test_wait_between_requests(self):
        self.assertFalse(self.agc.needs_to_wait())
        self.assertTrue(self.agc.needs_to_wait())
        time.sleep(2)
        self.assertFalse(self.agc.needs_to_wait())

