from abc import ABCMeta, abstractmethod
from threading import Lock
import requests
from urllib.parse import quote
import time
import logging

log = logging.getLogger(__name__)
lock = Lock()


class AbstractGetCall(object, metaclass=ABCMeta):
    def __init__(self, timeout=10, max_rate=0.9):
        self.timeout = timeout
        self.max_rate = max_rate
        self._last_request_time = None

    @staticmethod
    def _canonical_query_string(params):
        # params can be sorted in alphabetical order
        return "&".join("%s=%s" % (
            key, quote(str(params[key]))) for key in sorted(params))

    @abstractmethod
    def _api_url(self, kwargs):
        pass

    def _call_api(self, api_url):
            try:
                with requests.get(api_url, timeout=self.timeout) as resp:
                    return resp
            except Exception as e:
                log.error(e)

    def call(self, **kwargs):
        api_url = self._api_url(**kwargs)
        self.needs_to_wait()
        response = self._call_api(api_url)
        return response.text

    def needs_to_wait(self):
        result = False
        with lock:
            if self.max_rate and self._last_request_time:
                wait_time = 1 / self.max_rate - (time.time() - self._last_request_time)
                if wait_time > 0:
                    time.sleep(wait_time)
                    result = True
            self._last_request_time = time.time()
        return result
