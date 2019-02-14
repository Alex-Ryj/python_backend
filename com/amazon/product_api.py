import urllib
from urllib.parse import quote
import hmac
import time
import logging
from base64 import b64encode
from hashlib import sha256
from properties import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG, AWS_PORDUCT_API_SERVICE, AWS_PRODUCT_API_VERSION

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


class ProductAPI(object):
    def __init__(self, region='US', timeout=10, max_rate=0.9):
        self.max_rate = max_rate
        self.region = region
        self.timeout = timeout
        # put this in a list so it can be shared between instances
        self._last_request_time = None

    @staticmethod
    def _canonical_query_string(params):
        # params should be in a URL query string with keys in alphabetical order
        return "&".join("%s=%s" % (
            key, quote(str(params[key]))) for key in sorted(params))

    def _api_url(self, **kwargs):
        params = {
            'AWSAccessKeyId': AWS_ACCESS_KEY_ID,
            'AssociateTag': AWS_ASSOCIATE_TAG,
            'Service': AWS_PORDUCT_API_SERVICE,
            'Timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'Version': AWS_PRODUCT_API_VERSION,
        }
        params.update(kwargs)
        service_domain = ENDPOINT[self.region]
        quoted_strings = self._canonical_query_string(params)
        # Generate the string to be signed
        data = 'GET\n' + service_domain + '\n' + REQUEST_URI +'\n' + quoted_strings
        # Generate the signature required by the Product Advertising API
        digest = hmac.new(AWS_SECRET_ACCESS_KEY.encode(), data.encode(), sha256).digest()
        # base64 encode and urlencode
        signature = urllib.parse.quote(b64encode(digest))
        return ("https://" + service_domain + REQUEST_URI + "?" +
                quoted_strings + "&Signature=%s" % signature)

    def _call_api(self, api_url):
            try:
                api_request = urllib.request.Request(api_url)
                return urllib.request.urlopen(api_request, timeout=self.timeout)
            except Exception as e:
                log.error(e)

    def call(self, **kwargs):
        api_url = self._api_url(**kwargs)
        if self.max_rate and self._last_request_time:
            wait_time = 1 / self.max_rate - (time.time() - self._last_request_time)
            if wait_time > 0:
                time.sleep(wait_time)
        self._last_request_time = time.time()
        response = self._call_api(api_url)
        response_text = response.read()
        return response_text


__all__ = ["ProductAPI"]
