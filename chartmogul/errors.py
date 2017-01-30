from requests import HTTPError

class ConfigurationError(Exception):
    pass

class APIError(Exception):
    pass

def annotateHTTPError(err):
    if isinstance(err, HTTPError):
        raise APIError(err.response.content) from err
    else:
        raise err
