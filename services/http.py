import time, logging, requests
APP_LOGGER = logging.getLogger("cosmetics")

class HttpClient:
    def __init__(self, timeout_s: int = 30, max_retries: int = 3, backoff_s: int = 2):
        self.s = requests.Session()
        self.timeout_s, self.max_retries, self.backoff_s = timeout_s, max_retries, backoff_s

    def post_json(self, url: str, payload: dict) -> dict:
        for i in range(1, self.max_retries + 1):
            try:
                r = self.s.post(url, json=payload, timeout=self.timeout_s); r.raise_for_status()
                return r.json()
            except Exception as e:
                APP_LOGGER.warning("POST %s failed (%s/%s): %s", url, i, self.max_retries, e)
                if i == self.max_retries: raise
                time.sleep(self.backoff_s)
