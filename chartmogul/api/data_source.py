from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource
from collections import namedtuple


class DataSource(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#data-sources
    """

    _path = "/data_sources{/uuid}"
    _root_key = "data_sources"
    _many = namedtuple("DataSources", [_root_key])

    class _Schema(Schema):
        uuid = fields.String()
        name = fields.String()
        created_at = fields.DateTime()
        status = fields.Str()
        system = fields.Str()

        @post_load
        def make(self, data, **kwargs):
            return DataSource(**data)

    _schema = _Schema(unknown=EXCLUDE)
