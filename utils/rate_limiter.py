import time
import re

class RateLimiter:
    _instance = None

    def __new__(cls, min_interval=1.0):
        if cls._instance is None:
            cls._instance = super(RateLimiter, cls).__new__(cls)
            cls._instance.min_interval = min_interval
            cls._instance.next_allowed_time = time.time()
        return cls._instance

    def wait_for_slot(self):
        now = time.time()
        if now < self.next_allowed_time:
            sleep_time = self.next_allowed_time - now
            time.sleep(sleep_time)

    def update_after_response(self, response):
        now = time.time()

        if response.status_code == 429:
            try:
                api_response = response.json()
                error_msg = api_response.get("error", "")
                ms_match = re.search(r'(\d+)', error_msg)
                if ms_match:
                    wait_ms = int(ms_match.group(1))
                    self.next_allowed_time = now + wait_ms / 1000.0
                    return
            except Exception:
                pass

            retry_after = response.headers.get("retry-after")
            if retry_after:
                self.next_allowed_time = now + float(retry_after)
                return

            self.next_allowed_time = now + 2.0
        else:
            self.next_allowed_time = now + self.min_interval

# Instância global única
rate_limiter = RateLimiter()