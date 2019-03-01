import time
import threading
import unittest
from com.data.abstract_calls import AbstractApiCall
from com.amazon.amazon_api import ProductAPI
from com.ebay.ebay_api import EbayFindingAPI


class Test(unittest.TestCase):

    def setUp(self):
        AbstractApiCall.__abstractmethods__ = set()
        self.agc = AbstractApiCall()
        pass

    def tearDown(self):
        pass

    def test_query_string_sort(self):
        params = {'b': '2+b', 'a': '1&m', 'c': '3=j'}
        result = AbstractApiCall._canonical_query_string(params)
        self.assertEqual('a=1%26m&b=2%2Bb&c=3%3Dj', result)

    def test_wait_between_requests(self):
        self.assertFalse(self.agc.needs_to_wait())
        self.assertTrue(self.agc.needs_to_wait())
        time.sleep(2)
        self.assertFalse(self.agc.needs_to_wait())

    def test_concurrent_wait(self):
        amz = ProductAPI()
        ebay = EbayFindingAPI()
        t = threading.Thread(target=lambda: amz.needs_to_wait(), name='amz-thread')
        t.start()
        t.join()
        self.assertFalse(ebay.needs_to_wait())
        time.sleep(2)
        t2 = threading.Thread(target=lambda: ebay.needs_to_wait(), name='ebay-thread')
        t2.start()
        t2.join()
        self.assertTrue(ebay.needs_to_wait())
