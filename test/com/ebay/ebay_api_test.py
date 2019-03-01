import unittest
from properties import EBAY_APP_ID
from com.ebay.ebay_api import EbayFindingAPI
from com.data.utils import Container


class Test(unittest.TestCase):

    def setUp(self):
        self.ebay = EbayFindingAPI()
        pass

    def tearDown(self):
        pass

    def test_get_items_search(self):
        payload = Container()
        payload.headers = {
            'X-EBAY-SOA-OPERATION-NAME': 'findItemsByKeywords',
            'X-EBAY-SOA-SERVICE-VERSION': '1.0.0',
            'X-EBAY-SOA-REQUEST-DATA-FORMAT': 'XML',
            'X-EBAY-SOA-GLOBAL-ID': 'EBAY-US',
            'X-EBAY-SOA-SECURITY-APPNAME': EBAY_APP_ID,
            'Content-Type': 'text/xml;charset=utf-8',
        }
        payload.data = '''<findItemsByKeywordsRequest xmlns="https://www.ebay.com/marketplace/search/v1/services">
                                <keywords>harry potter phoenix</keywords>
                             </findItemsByKeywordsRequest>'''
        response = self.ebay.call({'OPERATION-NAME': 'findItemsByKeywords',
                                   'keywords': 'drone',
                                   'paginationInput.entriesPerPage': '5'}, payload
                                  )
        self.assertIn('Success', response, )
        print(response)

    def test_get_items_ids(self):
        pass

