import requests
from json import JSONDecodeError, dumps
from promise import Promise
from uritemplate import URITemplate
from .errors import *
from .api.config import Config
from datetime import datetime

"""
HTTP verb mapping. Based on nodejs library.
"""
MAPPINGS = {
    'all': 'get',
    'create': 'post',
    'destroy': 'delete',
    'cancel': 'patch',
    'merge': 'patch',
    'retrieve': 'get',
    'patch': 'patch',
    'update': 'put',
    'modify': 'patch',
    'add': 'post',
    'remove': 'delete'
}

PAGING = ['current_page', 'total_pages', 'has_more', 'per_page', 'page']

class DataObject:
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
        Pretty-prints any object as <ClassName{property='string',number=4,date=datetime.datetime(2003, 8, 4, 21, 41, 43)}>
        """
        return "<" + self.__class__.__name__ + "{" + \
                ", ".join([attr + "=" + repr(getattr(self, attr)) for attr in sorted(dir(self))
                          if not attr.startswith('_') and not callable(getattr(self, attr))]) + \
               "}>"

def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code
    Handles datetime.
    """

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")

class Resource(DataObject):
    _path = ''

    @classmethod
    def _load(cls, response):
        response.raise_for_status()
        if response.status_code == 204:
            return None

        try:
            return cls._schema.load(response.json()).data
        #TODO: schema errors? what class?
        # except ValueError: ! is parent class of JSONDecodeError
        except JSONDecodeError:
            return response.content

    @classmethod
    def _load_many(cls, response):
        """
        Python doesn't allow arbitrary fields on arrays and having special classes
        for array & cursor attributes is not necessary => namedtuple.
        (immutable, therefore all set on creation by generator)
        """
        response.raise_for_status()
        jsonObj = response.json()
        return cls._many(cls._schema.load(jsonObj[cls._root_key], many=True).data,
                         **{key: jsonObj[key] for key in PAGING if key in jsonObj})

    @classmethod
    def _request(cls, config, method, http_verb, path, data=None, **kwargs):
        if http_verb == 'get':
            params = kwargs
            data = None
        else:
            params = None
            if data is not None:
                data=dumps(data, default=json_serial)

        if method == 'all':
            postprocess = cls._load_many
        else:
            postprocess = cls._load

        return Promise(lambda resolve, _:
            resolve(getattr(requests, http_verb)(config.uri + path,
                data=data,
                params=params,
                auth=config.auth)
            )
        ).then(postprocess
        ).catch(annotateHTTPError)

    @classmethod
    def _expandPath(cls, path, kwargs):
        t = URITemplate(path)
        return t.expand(kwargs)

    @classmethod
    def _method(cls, method, path=None):
        @classmethod
        def fc(cls, config, **kwargs):
            if config is None or type(config) != Config:
                raise ConfigurationError("First argument should be instance of chartmogul.Config class!")

            pathTemp = path # due to Python closure
            if pathTemp is None:
                pathTemp = cls._path

            # This enforces user to pass argument, otherwise we could call wrong URL.
            if method in ['destroy','cancel', 'retrieve', 'update'] and 'uuid' not in kwargs:
                raise APIError("Please pass 'uuid' parameter")
            if method in ['create','modify'] and 'data' not in kwargs:
                raise APIError("Please pass 'data' parameter")

            pathTemp = Resource._expandPath(pathTemp, kwargs)
            # UUID is always path parameter only.
            if 'uuid' in kwargs:
                del kwargs['uuid']

            return cls._request(config, method, MAPPINGS[method], pathTemp, **kwargs)
        return fc

def _add_method(cls, method):
    """
    Dynamically define all possible actions.
    """
    fc = Resource._method(method)
    fc.__doc__ = "Sends %s request to ChartMogul." % MAPPINGS[method]
    fc.__name__ = method
    setattr(cls, fc.__name__, fc)


for key in MAPPINGS.keys():
    _add_method(Resource, key)
