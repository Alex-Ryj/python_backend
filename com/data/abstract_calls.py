from abc import ABCMeta, abstractmethod
from threading import Lock
from urllib.parse import quote
import time
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - (%(threadName)-9s) %(message)s', )
log = logging.getLogger(__name__)


class AbstractApiCall(object, metaclass=ABCMeta):
    def __init__(self, timeout=10, max_rate=0.9):
        self.timeout = timeout
        self.max_rate = max_rate
        self._last_request_time = None
        self.lock = Lock()

    @staticmethod
    def _canonical_query_string(params):
        # params can be sorted in alphabetical order
        return "&".join("%s=%s" % (
            key, quote(str(params[key]))) for key in sorted(params))

    @abstractmethod
    def _api_url(self, params):
        pass

    @abstractmethod
    def _call_api(self, api_url, payload=None):
        pass

    def call(self, params, payload=None):
        api_url = self._api_url(params)
        self.needs_to_wait()
        response = self._call_api(api_url, payload)
        return response.text

    def needs_to_wait(self):
        result = False
        with self.lock:
            log.debug('checking lock')
            if self.max_rate and self._last_request_time:
                wait_time = 1 / self.max_rate - (time.time() - self._last_request_time)
                if wait_time > 0:
                    time.sleep(wait_time)
                    log.debug('waiting...')
                    result = True
            self._last_request_time = time.time()
        return result
