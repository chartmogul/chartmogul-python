import requests
from json import dumps
from promise import Promise
from uritemplate import URITemplate
from .errors import APIError, ConfigurationError, ArgumentMissingError, annotateHTTPError
from .api.config import Config
from datetime import datetime, date
from builtins import str

"""
HTTP verb mapping. Based on nodejs library.
"""
MAPPINGS = {
    'add': 'post',
    'all': 'get',
    'cancel': 'patch',
    'create': 'post',
    'destroy': 'delete',
    'merge': 'patch',
    'modify': 'patch',
    'patch': 'patch',
    'remove': 'delete',
    'retrieve': 'get',
    'update': 'put'
}

LIST_PARAMS = ['current_page', 'total_pages',
               'has_more', 'per_page', 'page',
               'summary', 'customer_uuid']
ESCAPED_QUERY_KEYS = {
    'start_date': 'start-date',
    'end_date': 'end-date'
}


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
        return "<" + self.__class__.__name__ + "{" + \
            ", ".join([attr + "=" + repr(getattr(self, attr)) for attr in sorted(dir(self))
                       if not attr.startswith('_') and not callable(getattr(self, attr))]) + \
               "}>"


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
    _path = ''

    @classmethod
    def _load(cls, response):
        """
        Python doesn't allow arbitrary fields on arrays and having special classes
        for array & cursor attributes is not necessary => namedtuple.
        (immutable, therefore all set on creation by generator)
        """
        response.raise_for_status()
        if response.status_code == 204:
            return None
        try:
            jsonObj = response.json()
        except ValueError:  # Couldn't parse JSON, probably just text message.
            return response.content
        return cls._loadJSON(jsonObj)

    @classmethod
    def _loadJSON(cls, jsonObj):
        # has load_many capability & is many entries result?
        if '_root_key' in dir(cls) is not None and cls._root_key in jsonObj:
            return cls._many(cls._schema.load(jsonObj[cls._root_key], many=True).data,
                             **{key: jsonObj[key] for key in LIST_PARAMS if key in jsonObj})
        else:
            return cls._schema.load(jsonObj).data

    @classmethod
    def _preProcessParams(cls, params):
        for key, replacement in ESCAPED_QUERY_KEYS.items():
            if key in params:
                params[replacement] = params[key]
                del params[key]
        return params

    @classmethod
    def _request(cls, config, method, http_verb, path, data=None, **kwargs):
        if http_verb == 'get':
            params = cls._preProcessParams(kwargs)
            data = None
        else:
            params = None
            if data is not None:
                data = dumps(data, default=json_serial)

        return Promise(lambda resolve, _:
                       resolve(getattr(requests, http_verb)(
                           config.uri + path,
                           data=data,
                           headers={'content-type': 'application/json'},
                           params=params,
                           auth=config.auth,
                           timeout=config.request_timeout)
                       )).then(cls._load).catch(annotateHTTPError)

    @classmethod
    def _expandPath(cls, path, kwargs):
        t = URITemplate(path)
        return t.expand(kwargs)

    @classmethod
    def _method(cls, method, http_verb, path=None):
        @classmethod
        def fc(cls, config, **kwargs):
            if config is None or not isinstance(config, Config):
                raise ConfigurationError("First argument should be"
                                         " instance of chartmogul.Config class!")

            pathTemp = path  # due to Python closure
            if pathTemp is None:
                pathTemp = cls._path

            # This enforces user to pass argument, otherwise we could call
            # wrong URL.
            if method in ['destroy', 'cancel', 'retrieve', 'update'] and 'uuid' not in kwargs:
                raise ArgumentMissingError("Please pass 'uuid' parameter")
            if method in ['create', 'modify'] and 'data' not in kwargs:
                raise ArgumentMissingError("Please pass 'data' parameter")

            pathTemp = Resource._expandPath(pathTemp, kwargs)
            # UUID is always path parameter only.
            if 'uuid' in kwargs:
                del kwargs['uuid']

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
