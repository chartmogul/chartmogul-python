from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource
from chartmogul import ArgumentMissingError


class JsonImport(Resource):
    """
    https://dev.chartmogul.com/reference/bulk-import/
    """

    _path = "/data_sources{/data_source_uuid}/json_imports{/id}"

    class _Schema(Schema):
        id = fields.String()
        data_source_uuid = fields.String(allow_none=True)
        status = fields.String(allow_none=True)
        external_id = fields.String(allow_none=True)
        status_details = fields.Raw(allow_none=True)
        created_at = fields.DateTime(allow_none=True)
        updated_at = fields.DateTime(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return JsonImport(**data)

    _schema = _Schema(unknown=EXCLUDE)

    @classmethod
    def _validate_arguments(cls, method, kwargs):
        if method in ["create", "retrieve"] and "data_source_uuid" not in kwargs:
            raise ArgumentMissingError("Please pass 'data_source_uuid' parameter")
        if method in ["create"] and "data" not in kwargs:
            raise ArgumentMissingError("Please pass 'data' parameter")
        if method in ["retrieve"] and "id" not in kwargs:
            raise ArgumentMissingError("Please pass 'id' parameter")


JsonImport.create = JsonImport._method(
    "create", "post", "/data_sources{/data_source_uuid}/json_imports")
JsonImport.retrieve = JsonImport._method(
    "retrieve", "get", "/data_sources{/data_source_uuid}/json_imports{/id}")
