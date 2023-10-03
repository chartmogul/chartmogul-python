from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource
from .customer import Customer
from collections import namedtuple


class Tags(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#customer-attributes
    """

    _path = "/customers{/uuid}/attributes/tags"

    class _Schema(Schema):
        tags = fields.List(fields.String())

        @post_load
        def make(self, data, **kwargs):
            return Tags(**data)

    _customers = namedtuple("Customers", ["entries"])
    _schema = _Schema(unknown=EXCLUDE)

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
        if "entries" in jsonObj:
            customers = Customer._schema.load(jsonObj["entries"], many=True)
            return cls._customers(customers)
        else:
            return cls._schema.load(jsonObj)
