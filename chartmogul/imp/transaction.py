from ..api.transaction import Transaction as TransactionNew
from warnings import warn


class Transaction(TransactionNew):
    @classmethod
    def create(cls, *args, **kwargs):
        warn("chartmogul.imp namespace is deprecated, use chartmogul.Transaction.create!")
        return super(Transaction, cls).create(*args, **kwargs)
