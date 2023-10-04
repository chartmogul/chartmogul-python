from future.utils import raise_from
from requests import HTTPError


class ConfigurationError(Exception):
    pass


class APIError(Exception):
    pass


class ArgumentMissingError(Exception):
    pass


class DeprecatedArgumentError(Exception):
    pass


def annotateHTTPError(err):
    if isinstance(err, HTTPError):
        raise_from(APIError(err.response.content), err)
    else:
        raise err
