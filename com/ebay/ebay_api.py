from com.data.abstract_calls import AbstractGetCall
from properties import EBAY_APP_ID, EBAY_GLOBAL_ID, EBAY_SITE_ID

ENDPOINT = {
    'Finding': 'https://svcs.ebay.com/services/search/FindingService/v1?',
    'Shopping': 'http://open.api.ebay.com/shopping?',
    'SOAP': 'https://api.ebay.com/wsapi'
}


class EbayFindingAPI(AbstractGetCall):
    def __init__(self, timeout=10, max_rate=0.9):
        super().__init__(timeout, max_rate)

    def _api_url(self, **kwargs):
        params = {
            'SECURITY-APPNAME': EBAY_APP_ID,
            'SERVICE-VERSION': '1.0.0',
            'GLOBAL-ID': EBAY_GLOBAL_ID,
            'siteid': EBAY_SITE_ID,
            'RESPONSE-DATA-FORMAT': 'JSON',
        }
        params.update(kwargs)
        service_domain = ENDPOINT['Finding']
        quoted_strings = self._canonical_query_string(params)
        return service_domain + quoted_strings


__all__ = ["EbayFindingAPI"]
