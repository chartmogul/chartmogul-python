VERSION = "v1"
API_BASE = "https://api.chartmogul.com"


class Config:
    uri = API_BASE + "/" + VERSION

    def __init__(self, account_token, secret_key, request_timeout=None, max_retries=20, backoff_factor=2):
        self.auth = (account_token, secret_key)
        self.request_timeout = request_timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
