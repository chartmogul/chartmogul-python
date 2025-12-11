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


class InvoiceHandlingMethod(DataObject):
    class _Schema(Schema):
        create_subscription_when_invoice_is = fields.String()
        update_subscription_when_invoice_is = fields.String()
        prevent_subscription_for_invoice_voided = fields.Boolean()
        prevent_subscription_for_invoice_refunded = fields.Boolean()
        prevent_subscription_for_invoice_written_off = fields.Boolean()

        @post_load
        def make(self, data, **kwargs):
            return InvoiceHandlingMethod(**data)


class InvoiceHandlingSetting(DataObject):
    class _Schema(Schema):
        manual = fields.Nested(InvoiceHandlingMethod._Schema, many=False, unknown=EXCLUDE)
        automatic = fields.Nested(InvoiceHandlingMethod._Schema, many=False, unknown=EXCLUDE)

        @post_load
        def make(self, data, **kwargs):
            return InvoiceHandlingSetting(**data)


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
    _many = namedtuple(
        "DataSources",
        [_root_key] + _bool_query_params,
        defaults=[None, None, None]
    )

    @classmethod
    def _preProcessParams(cls, params):
        params = super()._preProcessParams(params)

        for query_param in cls._bool_query_params:
            if query_param in params and isinstance(params[query_param], bool):
                if params[query_param] is True:
                    params[query_param] = 'true'
                else:
                    del params[query_param]

        return params

    class _Schema(Schema):
        uuid = fields.String()
        name = fields.String()
        created_at = fields.DateTime()
        status = fields.Str()
        system = fields.Str()
        processing_status = fields.Nested(ProcessingStatus._Schema, many=False, allow_none=True)
        auto_churn_subscription_setting = fields.Nested(AutoChurnSubscriptionSetting._Schema, many=False, allow_none=True)
        invoice_handling_setting = fields.Nested(InvoiceHandlingSetting._Schema, many=False, allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return DataSource(**data)

    _schema = _Schema(unknown=EXCLUDE)
