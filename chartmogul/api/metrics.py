from marshmallow import Schema, fields, post_load
from ..resource import Resource, _add_method
from collections import namedtuple

class Metrics(Resource):
    """
    https://dev.chartmogul.com/docs/authentication
    """
    _path = "/metrics/all"
    _root_key = 'entries'
    _many = namedtuple('Metrics', [_root_key, 'summary'])
    _many.__new__.__defaults__ = (None,) * len(_many._fields)

    class _Schema(Schema):
        """
        Fields are optional, so a subset present is good enough
        """
        date = fields.Date()
        customer_churn_rate = fields.Number(load_from='customer-churn-rate')
        mrr_churn_rate = fields.Number(load_from='mrr-churn-rate')
        ltv = fields.Number()
        customers = fields.Number()
        asp = fields.Number()
        arpa = fields.Number()
        arr = fields.Number()
        mrr = fields.Number()

        @post_load
        def make(self, data):
            return Metrics(**data)

    _schema = _Schema(strict=True)

_add_method(Metrics, "mrr", "get", path='/metrics/mrr')
_add_method(Metrics, "arr", "get", path='/metrics/arr')
_add_method(Metrics, "arpa", "get", path='/metrics/arpa')
_add_method(Metrics, "asp", "get", path='/metrics/asp')
_add_method(Metrics, "customer_count", "get", path='/metrics/customer-count')
_add_method(Metrics, "customer_churn_rate", "get", path='/metrics/customer-churn-rate')
_add_method(Metrics, "mrr_churn_rate", "get", path='/metrics/mrr-churn-rate')
_add_method(Metrics, "ltv", "get", path='/metrics/ltv')
