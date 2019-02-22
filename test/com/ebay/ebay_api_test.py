import unittest
import time
from com.ebay.ebay_api import EbayFindingAPI


class Test(unittest.TestCase):

    def setUp(self):
        self.ebay = EbayFindingAPI()
        pass

    def tearDown(self):
        pass

    def test_get_items_search(self):
        # response = self.ebay.call({'OPERATION-NAME': 'ItemSearch',
        #                           'SearchIndex': 'All',
        #                           'Keywords': 'drone',
        #                           'paginationInput.entriesPerPage': '5'}
        #                           )
        response = self.ebay.call(Keywords='drone'
                                  )
        print(response)

    def test_get_items_ids(self):
        pass
