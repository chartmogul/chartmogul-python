from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource, DataObject, _add_method
from collections import namedtuple

metrics = ["customers", "customer-churn-rate", "arr", "asp", "mrr", "arpa", "mrr-churn-rate", "ltv"]


class Summary(DataObject):
    """
    Optional information about a series of metrics.
    """

    class _Schema(Schema):
        current = fields.Number()
        previous = fields.Number()
        percentage_change = fields.Number(data_key="percentage-change")
        # All metrics percentage change
        for metric in metrics:
            pc = metric + "-percentage-change"
            current_pc = "current-" + metric
            previous_pc = "previous-" + metric
            locals()[pc.replace("-", "_")] = fields.Number(data_key=pc)
            locals()[current_pc.replace("-", "_")] = fields.Number(data_key=current_pc)
            locals()[previous_pc.replace("-", "_")] = fields.Number(data_key=previous_pc)

        @post_load
        def make(self, data, **kwargs):
            return Summary(**data)

    _schema = _Schema(unknown=EXCLUDE)


class Metrics(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#introduction-metrics-api
    """

    _path = "/metrics/all"
    _root_key = "entries"
    _many_cls = namedtuple("Metrics", [_root_key, "summary"])
    _many_cls.__new__.__defaults__ = (None,) * len(_many_cls._fields)

    class _Schema(Schema):
        """
        Fields are optional, so a subset present is good enough
        """

        date = fields.Date()
        customer_churn_rate = fields.Number(data_key="customer-churn-rate")
        mrr_churn_rate = fields.Number(data_key="mrr-churn-rate")
        ltv = fields.Number()
        customers = fields.Number()
        asp = fields.Number()
        arpa = fields.Number()
        arr = fields.Number()
        mrr = fields.Number()
        # MRR only
        mrr_new_business = fields.Number(data_key="mrr-new-business")
        mrr_expansion = fields.Number(data_key="mrr-expansion")
        mrr_contraction = fields.Number(data_key="mrr-contraction")
        mrr_churn = fields.Number(data_key="mrr-churn")
        mrr_reactivation = fields.Number(data_key="mrr-reactivation")
        percentage_change = fields.Number(data_key="percentage-change")
        for metric in metrics:
            pc = metric + "-percentage-change"
            locals()[pc.replace("-", "_")] = fields.Number(data_key=pc)

        @post_load
        def make(self, data, **kwargs):
            return Metrics(**data)

    _schema = _Schema(unknown=EXCLUDE)

    @classmethod
    def _many(cls, entries, **kwargs):
        if "summary" in kwargs:
            kwargs["summary"] = Summary._schema.load(kwargs["summary"])
        return cls._many_cls(entries, **kwargs)


_add_method(Metrics, "mrr", "get", path="/metrics/mrr")
_add_method(Metrics, "arr", "get", path="/metrics/arr")
_add_method(Metrics, "arpa", "get", path="/metrics/arpa")
_add_method(Metrics, "asp", "get", path="/metrics/asp")
_add_method(Metrics, "customer_count", "get", path="/metrics/customer-count")
_add_method(Metrics, "customer_churn_rate", "get", path="/metrics/customer-churn-rate")
_add_method(Metrics, "mrr_churn_rate", "get", path="/metrics/mrr-churn-rate")
_add_method(Metrics, "ltv", "get", path="/metrics/ltv")
