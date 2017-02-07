VERSION = "v1"
API_BASE = "https://api.chartmogul.com"


class Config:
    uri = API_BASE + "/" + VERSION

    def __init__(self, account_token, secret_key):
        self.auth = (account_token, secret_key)
