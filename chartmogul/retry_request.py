import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

METHOD_WHITELIST = ["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
STATUS_FORCELIST = (429, 500, 502, 503, 504, 520, 524)


def requests_retry_session(
    retries=20,
    backoff_factor=2,
    session=None,
):
    session = session or requests.Session()
    adapter = _retry_adapter(retries, backoff_factor)
    session.mount("https://", adapter)
    return session


def _retry_adapter(retries, backoff_factor):
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        status=retries,
        allowed_methods=METHOD_WHITELIST,
        status_forcelist=STATUS_FORCELIST,
        backoff_factor=backoff_factor,
    )
    return HTTPAdapter(max_retries=retry)
