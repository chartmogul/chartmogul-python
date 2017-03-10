from ..api.invoice import Invoice as InvoiceNew
from warnings import warn


class Invoice(InvoiceNew):
    @classmethod
    def create(cls, *args, **kwargs):
        warn("chartmogul.imp namespace is deprecated, use chartmogul.Invoice.create!")
        return super(Invoice, cls).create(*args, **kwargs)

    @classmethod
    def all(cls, *args, **kwargs):
        warn("chartmogul.imp namespace is deprecated, use chartmogul.Invoice.all!")
        return super(Invoice, cls).all(*args, **kwargs)
