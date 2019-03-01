import logging
import requests
from com.data.abstract_calls import AbstractApiCall
from properties import EBAY_APP_ID, EBAY_GLOBAL_ID, EBAY_SITE_ID


ENDPOINT = {
    'Finding': 'https://svcs.ebay.com/services/search/FindingService/v1?',
    'Shopping': 'http://open.api.ebay.com/shopping?',
    'SOAP': 'https://api.ebay.com/wsapi'
}

log = logging.getLogger(__name__)


class EbayFindingAPI(AbstractApiCall):

    def __init__(self, timeout=10, max_rate=0.9):
        super().__init__(timeout, max_rate)

    def _api_url(self, extra_params):
        params = {
            'SECURITY-APPNAME': EBAY_APP_ID,
            'SERVICE-VERSION': '1.0.0',
            'GLOBAL-ID': EBAY_GLOBAL_ID,
            'siteid': EBAY_SITE_ID,
            'RESPONSE-DATA-FORMAT': 'JSON',
        }
        params.update(extra_params)
        service_domain = ENDPOINT['Finding']
        quoted_strings = self._canonical_query_string(params)
        return service_domain + quoted_strings

    def _call_api(self, api_url, payload):
        try:
            # with requests.get(api_url, timeout=self.timeout) as resp:
            with requests.post(api_url, timeout=self.timeout, headers=payload.headers, data=payload.data) as resp:
                return resp
        except Exception as e:
            log.error(e)


__all__ = ["EbayFindingAPI"]
