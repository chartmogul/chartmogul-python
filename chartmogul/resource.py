from datetime import date, datetime
from json import dumps

from promise import Promise
from uritemplate import URITemplate

from .api.config import Config
from .errors import (
    ArgumentMissingError,
    ConfigurationError,
    annotateHTTPError,
    DeprecatedArgumentError,
)
from .retry_request import requests_retry_session

from .version import __version__

"""
HTTP verb mapping. Based on nodejs library.
"""
MAPPINGS = {
    "add": "post",
    "all": "get",
    "cancel": "patch",
    "create": "post",
    "destroy": "delete",
    "merge": "patch",
    "modify": "patch",
    "patch": "patch",
    "remove": "delete",
    "retrieve": "get",
    "update": "put",
    "destroy_with_params": "delete",
    "modify_with_params": "patch",
}

LIST_PARAMS = ["has_more", "summary", "customer_uuid", "data_source_uuid", "cursor"]
ESCAPED_QUERY_KEYS = {"start_date": "start-date", "end_date": "end-date"}


class DataObject(object):
    def __init__(self, **kwargs):
        """
        Any arguments are translated into class attributes.
        """
        self._set_attrs(**kwargs)

    def _set_attrs(self, **kwargs):
        """
        Dynamically creates attributes of the class, so it's not necessary
        to repeat their list besides the serialization schema.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        """
        Pretty-prints any object as
        <ClassName{property='string',number=4,date=datetime.datetime(2003, 8, 4, 21, 41, 43)}>
        """
        return (
            "<"
            + self.__class__.__name__
            + "{"
            + ", ".join(
                [
                    attr + "=" + repr(getattr(self, attr))
                    for attr in sorted(dir(self))
                    if not attr.startswith("_") and not callable(getattr(self, attr))
                ]
            )
            + "}>"
        )


def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code
    Handles date & datetime.
    """

    if isinstance(obj, date) or isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")


class Resource(DataObject):
    _path = ""

    @classmethod
    def _load(cls, response):
        """
        Python doesn't allow arbitrary fields on arrays and having special classes
        for array & cursor attributes is not necessary => namedtuple.
        (immutable, therefore all set on creation by generator)
        """
        response.raise_for_status()
        if response.status_code == 204 or response.status_code == 202:
            return None
        try:
            jsonObj = response.json()
        except ValueError:  # Couldn't parse JSON, probably just text message.
            return response.content
        return cls._loadJSON(jsonObj)

    @classmethod
    def _loadJSON(cls, jsonObj):
        # has load_many capability & is many entries result?
        if "_root_key" in dir(cls) is not None and cls._root_key in jsonObj:
            return cls._many(
                cls._schema.load(jsonObj[cls._root_key], many=True),
                **{key: jsonObj[key] for key in LIST_PARAMS if key in jsonObj},
            )
        else:
            return cls._schema.load(jsonObj)

    @classmethod
    def _preProcessParams(cls, params):
        for key, replacement in ESCAPED_QUERY_KEYS.items():
            if key in params:
                params[replacement] = params[key]
                del params[key]
        return params

    @classmethod
    def _request(cls, config, method, http_verb, path, data=None, **kwargs):
        if http_verb == "get":
            params = cls._preProcessParams(kwargs)
            data = None
        else:
            params = None
            if data is not None:
                data = dumps(data, default=json_serial)

        return (
            Promise(
                lambda resolve, _: resolve(
                    getattr(
                        requests_retry_session(config.max_retries, config.backoff_factor),
                        http_verb,
                    )(
                        config.uri + path,
                        data=data,
                        headers={
                            "content-type": "application/json",
                            "User-Agent": "chartmogul-python/" + __version__,
                        },
                        params=params,
                        auth=config.auth,
                        timeout=config.request_timeout,
                    )
                )
            )
            .then(cls._load)
            .catch(annotateHTTPError)
        )

    @classmethod
    def _expandPath(cls, path, kwargs):
        t = URITemplate(path)
        return t.expand(kwargs)

    @classmethod
    def _validate_arguments(cls, method, kwargs):
        # This enforces user to pass argument, otherwise we could call
        # wrong URL.
        if method in ["destroy", "cancel", "retrieve", "modify", "update"] and "uuid" not in kwargs:
            raise ArgumentMissingError("Please pass 'uuid' parameter")
        if method in ["create", "modify"] and "data" not in kwargs:
            raise ArgumentMissingError("Please pass 'data' parameter")
        if method == "all" and "page" in kwargs:
            raise DeprecatedArgumentError("The 'page' parameter is deprecated")
        if (
            method in ["destroy_all"]
            and "data_source_uuid" not in kwargs
            and "customer_uuid" not in kwargs
        ):
            raise ArgumentMissingError(
                "Please pass 'data_source_uuid' and 'customer_uuid' parameters"
            )
        if method in ["destroy_with_params", "modify_with_params"] and not (
            "id" in kwargs["data"]["subscription_event"]
            or (
                "external_id" in kwargs["data"]["subscription_event"]
                and "data_source_uuid" in kwargs["data"]["subscription_event"]
            )
        ):
            raise ArgumentMissingError(
                "Please pass 'id' parameter or 'data_source_uuid' and 'external_id'"
            )

    @classmethod
    def _method(callerClass, method, http_verb, path=None, useCallerClass=False, useUUIDFor=None):
        @classmethod
        def fc(calleeClass, config, **kwargs):
            if config is None or not isinstance(config, Config):
                raise ConfigurationError(
                    "First argument should be" " instance of chartmogul.Config class!"
                )

            cls = callerClass if useCallerClass else calleeClass

            pathTemp = path  # due to Python closure
            if pathTemp is None:
                pathTemp = cls._path

            cls._validate_arguments(method, kwargs)

            pathTemp = Resource._expandPath(pathTemp, kwargs)

            if useUUIDFor is not None and 'data' in kwargs.keys():
                kwargs["data"][useUUIDFor] = kwargs["uuid"]

            # UUID is always path parameter only.
            if "uuid" in kwargs:
                del kwargs["uuid"]

            return cls._request(config, method, http_verb, pathTemp, **kwargs)

        return fc


def _add_method(cls, method, http_verb, path=None):
    """
    Dynamically define all possible actions.
    """
    fc = Resource._method(method, http_verb, path)
    # Not supported by 2.7, but probably not needed.
    # fc.__doc__ = "Sends %s request to ChartMogul." % http_verb
    # fc.__name__ = method
    setattr(cls, method, fc)


for method, http_verb in MAPPINGS.items():
    _add_method(Resource, method, http_verb)
