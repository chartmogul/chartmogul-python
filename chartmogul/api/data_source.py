from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource, DataObject
from collections import namedtuple


class ProcessingStatus(DataObject):
    class _Schema(Schema):
        processed = fields.Integer(allow_none=True)
        pending = fields.Integer(allow_none=True)
        failed = fields.Integer(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return ProcessingStatus(**data)


class AutoChurnSubscriptionSetting(DataObject):
    class _Schema(Schema):
        enabled = fields.Boolean()
        interval = fields.Integer(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return AutoChurnSubscriptionSetting(**data)


class DataSource(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#data-sources
    """

    _path = "/data_sources{/uuid}"
    _root_key = "data_sources"
    _bool_query_params = [
        'with_processing_status',
        'with_auto_churn_subscription_setting',
        'with_invoice_handling_setting'
    ]
    _many = namedtuple("DataSources", [_root_key])

    class _Schema(Schema):
        uuid = fields.String()
        name = fields.String()
        created_at = fields.DateTime()
        status = fields.Str()
        system = fields.Str()
        processing_status = fields.Nested(ProcessingStatus._Schema, many=False, allow_none=True)
        auto_churn_subscription_setting = fields.Nested(AutoChurnSubscriptionSetting._Schema, many=False, allow_none=True)
        invoice_handling_setting = fields.Raw(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return DataSource(**data)

    _schema = _Schema(unknown=EXCLUDE)
