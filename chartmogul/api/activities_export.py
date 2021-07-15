from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource
from collections import namedtuple


class ActivitiesExport(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#list-customer-subscriptions
    """
    _path = "/activities_export"

    class _Schema(Schema):
        # Create
        start_date = fields.DateTime()
        end_date = fields.DateTime()
        type = fields.String()

        # Retrieve
        id = fields.String()
        status = fields.String()
        file_url = fields.String(allow_none=True)
        params = fields.Dict(allow_none=True)
        expires_at = fields.DateTime(allow_none=True)
        created_at = fields.DateTime()

        @post_load
        def make(self, data, **kwargs):
            return ActivitiesExport(**data)

    _schema = _Schema(unknown=EXCLUDE)

    @classmethod
    def _validate_arguments(cls, method, kwargs):
        # This enforces user to pass correct argument
        if method in ['retrieve'] and 'id' not in kwargs:
            raise ArgumentMissingError("Please pass 'id' parameter to retrieve your export request status")
        if method in ['create'] and 'data' not in kwargs:
            raise ArgumentMissingError("Please pass 'data' parameter")

ActivitiesExport.create = ActivitiesExport._method('create', 'post', '/activities_export')
ActivitiesExport.retrieve = ActivitiesExport._method('retrieve', 'get', '/activities_export/{id}')
