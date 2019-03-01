from urllib.parse import quote
import hmac
import time
import requests
import logging
from base64 import b64encode
from hashlib import sha256
from com.data.abstract_calls import AbstractApiCall
from properties import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG, \
    AWS_PRODUCT_API_SERVICE, AWS_PRODUCT_API_VERSION

ENDPOINT = {
    'US': 'webservices.amazon.com',
    'CA': 'webservices.amazon.ca',
    'CN': 'webservices.amazon.cn',
    'DE': 'webservices.amazon.de',
    'ES': 'webservices.amazon.es',
    'FR': 'webservices.amazon.fr',
    'IN': 'webservices.amazon.in',
    'IT': 'webservices.amazon.it',
    'JP': 'webservices.amazon.co.jp',
    'UK': 'webservices.amazon.co.uk',
    'BR': 'webservices.amazon.com.br',
    'MX': 'webservices.amazon.com.mx',
}
REQUEST_URI = "/onca/xml"

log = logging.getLogger(__name__)


class ProductAPI(AbstractApiCall):
    def __init__(self, region='US', timeout=10, max_rate=0.9):
        self.region = region
        self._last_request_time = None
        super().__init__(timeout, max_rate)

    def _api_url(self, extra_params):
        params = {
            'AWSAccessKeyId': AWS_ACCESS_KEY_ID,
            'AssociateTag': AWS_ASSOCIATE_TAG,
            'Service': AWS_PRODUCT_API_SERVICE,
            'Timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'Version': AWS_PRODUCT_API_VERSION,
        }
        params.update(extra_params)
        service_domain = ENDPOINT[self.region]
        quoted_strings = self._canonical_query_string(params)
        # Generate the string to be signed
        data = 'GET\n' + service_domain + '\n' + REQUEST_URI + '\n' + quoted_strings
        # Generate the signature required by the Product Advertising API
        digest = hmac.new(AWS_SECRET_ACCESS_KEY.encode(), data.encode(), sha256).digest()
        # base64 encode and urlencode
        signature = quote(b64encode(digest))
        return ("https://" + service_domain + REQUEST_URI + "?" +
                quoted_strings + "&Signature=%s" % signature)

    def _call_api(self, api_url):
        try:
            with requests.get(api_url, timeout=self.timeout) as resp:
                return resp
        except Exception as e:
            log.error(e)
        pass


__all__ = ["ProductAPI"]
