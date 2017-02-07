from marshmallow import Schema, fields, post_load
from ..resource import Resource, DataObject


class Stripe(DataObject):
    class _Schema(Schema):
        uid = fields.Int()
        coupon = fields.Boolean()

        @post_load
        def make(self, data):
            return Stripe(**data)


class Name(DataObject):
    class _Schema(Schema):
        fullName = fields.String()

        @post_load
        def make(self, data):
            return Name(**data)


class Employment(DataObject):
    class _Schema(Schema):
        name = fields.String()

        @post_load
        def make(self, data):
            return Employment(**data)


class Person(DataObject):
    class _Schema(Schema):
        name = fields.Nested(Name._Schema)
        employment = fields.Nested(Employment._Schema)

        @post_load
        def make(self, data):
            return Person(**data)


class Company(DataObject):
    class _Schema(Schema):
        name = fields.String()
        legalName = fields.String()
        domain = fields.String()
        url = fields.String()
        category = fields.Dict()
        metrics = fields.Dict()

        @post_load
        def make(self, data):
            return Company(**data)


class Clearbit(DataObject):
    class _Schema(Schema):
        company = fields.Nested(Company._Schema)
        person = fields.Nested(Person._Schema)

        @post_load
        def make(self, data):
            return Clearbit(**data)


class Attributes(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#customer-attributes
    """
    _path = "/customers{/uuid}/attributes"

    class _Schema(Schema):
        tags = fields.List(fields.String())
        stripe = fields.Nested(Stripe._Schema)
        clearbit = fields.Nested(Clearbit._Schema)
        custom = fields.Dict()

        @post_load
        def make(self, data):
            return Attributes(**data)

    _schema = _Schema(strict=True)
