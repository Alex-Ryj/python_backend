import unittest
from com.amazon.product_api import ProductAPI


class Test(unittest.TestCase):

    def setUp(self):
        self.amz = ProductAPI(region='UK')
        pass

    def tearDown(self):
        pass

    def test_query_string_sort(self):
        params = {'b': '2+b', 'a': '1&m', 'c': '3=j'}
        result = ProductAPI._canonical_query_string(params)
        self.assertEqual('a=1%26m&b=2%2Bb&c=3%3Dj', result)

    def test_get_items(self):

        response = self.amz.call(Operation='ItemSearch',
                            SearchIndex='All',
                            Keywords='drone',
                            ResponseGroup='Images,ItemAttributes,Offers'
                            )
        print(response)
        self.assertTrue('ItemSearchResponse' in str(response))
