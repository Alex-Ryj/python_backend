import unittest
from com.amazon.amazon_api import ProductAPI


class Test(unittest.TestCase):

    def setUp(self):
        self.amz = ProductAPI(region='IT')
        pass

    def tearDown(self):
        pass

    def test_get_items_search(self):

        response = self.amz.call({'Operation': 'ItemSearch',
                                 'SearchIndex': 'All',
                                 'Keywords': 'drone',
                                 'ResponseGroup': 'Images,ItemAttributes,Offers'
                                 })
        print(response)
        self.assertTrue('ItemSearchResponse' in str(response))

    def test_get_items_asins(self):
        response = self.amz.call(Operation='ItemLookup',
                                 Condition='All',
                                 IdType='ASIN',
                                 ItemId='B00NIUHAG6',
                                 ResponseGroup='Images,ItemAttributes,Offers'
                                 )
        print(response)
        self.assertTrue('ItemSearchResponse' in str(response))



