from marshmallow import Schema, fields, post_load
from ..resource import Resource, DataObject, _add_method
from .customer import Customer
from collections import namedtuple


class CustomAttributes(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#custom-attributes
    """
    _path = "/customers{/uuid}/attributes/custom"

    class _Schema(Schema):
        custom = fields.Dict()

        @post_load
        def make(self, data, **kwargs):
            return CustomAttributes(**data)

    _customers = namedtuple('Customers', ['entries'])
    _schema = _Schema()

    @classmethod
    def _load(cls, response):
        """
        Workaround: when using email, the return value is actually
        a list of customers, but without paging.
        """
        response.raise_for_status()
        if response.status_code == 204:
            return None
        jsonObj = response.json()
        if 'entries' in jsonObj:
            customers = Customer._schema.load(jsonObj['entries'], many=True)
            return cls._customers(customers)
        else:
            return cls._schema.load(jsonObj)
