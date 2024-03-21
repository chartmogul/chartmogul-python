import unittest
from chartmogul import Customer, Contact, Config, CustomerNote, Opportunity
from chartmogul.api.customer import Attributes, Address
from datetime import datetime
from chartmogul import APIError
import requests_mock

from pprint import pprint

entry = {
    "id": 25647,
    "uuid": "cus_de305d54-75b4-431b-adb2-eb6b9e546012",
    "external_id": "34916129",
    "external_ids": ["34916129"],
    "data_source_uuid": "ds_610b7a84-c50f-11e6-8aab-97d6db98913a",
    "data_source_uuids": ["ds_610b7a84-c50f-11e6-8aab-97d6db98913a"],
    "name": "Example Company",
    "company": "",
    "email": "bob@examplecompany.com",
    "status": "Active",
    "lead_created_at": "2015-01-01T10:00:00-04:00",
    "free_trial_started_at": "2015-01-09T10:00:00-04:00",
    "customer-since": "2015-06-09T13:16:00-04:00",
    "city": "Nowhereville",
    "state": "Alaska",
    "country": "US",
    "zip": "0185128",
    "attributes": {
        "tags": ["engage", "unit loss", "discountable"],
        "stripe": {"uid": 7, "coupon": True},
        "clearbit": {
            "company": {
                "name": "Example Company",
                "legalName": "Example Company Inc.",
                "domain": "examplecompany.com",
                "url": "http://examplecompany.com",
                "category": {
                    "sector": "Information Technology",
                    "industryGroup": "Software and Services",
                    "industry": "Software",
                    "subIndustry": "Application Software",
                },
                "metrics": {
                    "raised": 1502450000,
                    "employees": 1000,
                    "googleRank": 7,
                    "alexaGlobalRank": 2319,
                    "marketCap": None,
                },
            },
            "person": {
                "name": {"fullName": "Bob Kramer"},
                "employment": {"name": "Example Company"},
            },
        },
        "custom": {
            "CAC": 213,
            "utmCampaign": "social media 1",
            "convertedAt": "2015-09-08 00:00:00",
            "pro": False,
            "salesRep": "Gabi",
        },
    },
    "address": {
        "address_zip": "0185128",
        "city": "Nowhereville",
        "country": "US",
        "state": "Alaska",
    },
    "mrr": 3000.0,
    "arr": 36000.0,
    "billing-system-url": "https:\/\/dashboard.stripe.com\/customers\/cus_4Z2ZpyJFuQ0XMb",
    "chartmogul-url": "https:\/\/app.chartmogul.com\/#customers\/25647-Example_Company",
    "billing-system-type": "Stripe",
    "currency": "USD",
    "currency-sign": "$",
    "website_url": "https://chartmogul.com",
}

allContacts = {"entries": [entry], "cursor": "cursor==", "has_more": True}

deserializedCustomer = Customer(
    id=25647,
    uuid="cus_de305d54-75b4-431b-adb2-eb6b9e546012",
    external_id="34916129",
    external_ids=["34916129"],
    data_source_uuid="ds_610b7a84-c50f-11e6-8aab-97d6db98913a",
    data_source_uuids=["ds_610b7a84-c50f-11e6-8aab-97d6db98913a"],
    name="Example Company",
    company="",
    email="bob@examplecompany.com",
    status="Active",
    lead_created_at=datetime(2015, 1, 1, 10, 0),
    free_trial_started_at=datetime(2015, 1, 9, 10, 0),
    customer_since=datetime(2015, 6, 9, 13, 16),
    city="Nowhereville",
    state="Alaska",
    country="US",
    zip="0185128",
    attributes=Attributes(
        tags=["engage", "unit loss", "discountable"],
        stripe={"uid": 7, "coupon": True},
        clearbit={
            "company": {
                "name": "Example Company",
                "legalName": "Example Company Inc.",
                "domain": "examplecompany.com",
                "url": "http://examplecompany.com",
                "category": {
                    "sector": "Information Technology",
                    "industryGroup": "Software and Services",
                    "industry": "Software",
                    "subIndustry": "Application Software",
                },
                "metrics": {
                    "alexaGlobalRank": 2319,
                    "googleRank": 7,
                    "employees": 1000,
                    "marketCap": None,
                    "raised": 1502450000,
                },
            },
            "person": {
                "name": {"fullName": "Bob Kramer"},
                "employment": {"name": "Example Company"},
            },
        },
        custom={
            "CAC": 213,
            "utmCampaign": "social media 1",
            "convertedAt": "2015-09-08 00:00:00",
            "pro": False,
            "salesRep": "Gabi",
        },
    ),
    address=Address(address_zip="0185128", city="Nowhereville", country="US", state="Alaska"),
    mrr=3000.0,
    arr=36000.0,
    billing_system_url="https:\/\/dashboard.stripe.com\/customers\/cus_4Z2ZpyJFuQ0XMb",
    chartmogul_url="https:\/\/app.chartmogul.com\/#customers\/25647-Example_Company",
    billing_system_type="Stripe",
    currency="USD",
    currency_sign="$",
    website_url="https://chartmogul.com",
)

createCustomer = {
    "external_id": "34916129",
    "data_source_uuid": "ds_610b7a84-c50f-11e6-8aab-97d6db98913a",
    "name": "Example Company",
    "company": "",
    "email": "bob@examplecompany.com",
    "lead_created_at": datetime(2015, 1, 1, 10, 0),
    "free_trial_started_at": datetime(2015, 1, 9, 10, 0),
    "customer-since": datetime(2015, 6, 9, 13, 16),
    "city": "Nowhereville",
    "state": "Alaska",
    "country": "US",
    "zip": "0185128",
    "attributes": {
        "tags": ["engage", "unit loss", "discountable"],
        "stripe": {"uid": 7, "coupon": True},
        "clearbit": {
            "company": {
                "name": "Example Company",
                "legalName": "Example Company Inc.",
                "domain": "examplecompany.com",
                "url": "http://examplecompany.com",
                "category": {
                    "sector": "Information Technology",
                    "industryGroup": "Software and Services",
                    "industry": "Software",
                    "subIndustry": "Application Software",
                },
                "metrics": {
                    "raised": 1502450000,
                    "employees": 1000,
                    "googleRank": 7,
                    "alexaGlobalRank": 2319,
                    "marketCap": None,
                },
            },
            "person": {
                "name": {"fullName": "Bob Kramer"},
                "employment": {"name": "Example Company"},
            },
        },
        "custom": [
            {"key": "CAC", "type": "Integer", "value": 213},
            {"key": "utmCampaign", "value": "social media 1", "type": "String"},
            {"key": "convertedAt", "value": datetime(2015, 9, 8), "type": "Timestamp"},
            {"key": "pro", "value": False, "type": "Boolean"},
            {"key": "salesRep", "value": "Gabi", "type": "String"},
        ],
    },
    "website_url": "https://chartmogul.com"
}

sentCreateExpected = {
    "attributes": {
        "stripe": {"uid": 7, "coupon": True},
        "clearbit": {
            "company": {
                "name": "Example Company",
                "legalName": "Example Company Inc.",
                "domain": "examplecompany.com",
                "url": "http://examplecompany.com",
                "category": {
                    "sector": "Information Technology",
                    "industryGroup": "Software and Services",
                    "industry": "Software",
                    "subIndustry": "Application Software",
                },
                "metrics": {
                    "raised": 1502450000,
                    "employees": 1000,
                    "googleRank": 7,
                    "alexaGlobalRank": 2319,
                    "marketCap": None,
                },
            },
            "person": {
                "name": {"fullName": "Bob Kramer"},
                "employment": {"name": "Example Company"},
            },
        },
        "custom": [
            {"key": "CAC", "type": "Integer", "value": 213},
            {"key": "utmCampaign", "value": "social media 1", "type": "String"},
            {"key": "convertedAt", "value": "2015-09-08T00:00:00", "type": "Timestamp"},
            {"key": "pro", "value": False, "type": "Boolean"},
            {"key": "salesRep", "value": "Gabi", "type": "String"},
        ],
        "tags": ["engage", "unit loss", "discountable"],
    },
    "city": "Nowhereville",
    "company": "",
    "country": "US",
    "customer-since": "2015-06-09T13:16:00",
    "data_source_uuid": "ds_610b7a84-c50f-11e6-8aab-97d6db98913a",
    "email": "bob@examplecompany.com",
    "external_id": "34916129",
    "free_trial_started_at": "2015-01-09T10:00:00",
    "lead_created_at": "2015-01-01T10:00:00",
    "name": "Example Company",
    "state": "Alaska",
    "zip": "0185128",
    "website_url": "https://chartmogul.com",
}

contact = {
    "uuid": "con_00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "data_source_uuid": "ds_00000000-0000-0000-0000-000000000000",
    "customer_external_id": "external_001",
    "first_name": "First name",
    "last_name": "Last name",
    "position": 9,
    "title": "Title",
    "email": "test@example.com",
    "phone": "+1234567890",
    "linked_in": "https://linkedin.com/not_found",
    "twitter": "https://twitter.com/not_found",
    "notes": "Heading\nBody\nFooter",
    "custom": {"MyStringAttribute": "Test", "MyIntegerAttribute": 123},
}

createContact = {
    "uuid": "con_00000000-0000-0000-0000-000000000000",
    "data_source_uuid": "ds_00000000-0000-0000-0000-000000000000",
    "first_name": "First name",
    "last_name": "Last name",
    "position": 9,
    "title": "Title",
    "email": "test@example.com",
    "phone": "+1234567890",
    "linked_in": "https://linkedin.com/not_found",
    "twitter": "https://twitter.com/not_found",
    "notes": "Heading\nBody\nFooter",
    "custom": [
        {"key": "MyStringAttribute", "value": "Test"},
        {"key": "MyIntegerAttribute", "value": 123},
    ],
}

note = {
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "type": "note",
    "text": "This is a note",
    "call_duration": 0,
    "author_email": "john@example.com",
    "created_at": "2015-06-09T13:16:00-04:00",
    "updated_at": "2015-06-09T13:16:00-04:00"
}

createNote = {
    "type": "note",
    "text": "This is a note",
    "author_email": "john@xample.com"
}

noteEntry = {
    "uuid": "cus_00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "type": "note",
    "text": "This is a note",
    "call_duration": 0,
    "author_email": "john@example.com",
    "created_at": "2015-06-09T13:16:00-04:00",
    "updated_at": "2015-06-09T13:16:00-04:00"
}

allNotes = {"entries": [noteEntry], "cursor": "cursor==", "has_more": True}

opportunity = {
    "uuid": "00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "owner": "test1@example.org",
    "pipeline": "New business 1",
    "pipeline_stage": "Discovery",
    "estimated_close_date": "2023-12-22",
    "currency": "USD",
    "amount_in_cents": 100,
    "type": "recurring",
    "forecast_category": "pipeline",
    "win_likelihood": 3,
    "custom": {"from_campaign": True},
    "created_at": "2024-03-13T07:33:28.356Z",
    "updated_at": "2024-03-13T07:33:28.356Z"
}

createOpportunity = {
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "owner": "test1@example.org",
    "pipeline": "New business 1",
    "pipeline_stage": "Discovery",
    "estimated_close_date": "2023-12-22",
    "currency": "USD",
    "amount_in_cents": 100,
    "type": "recurring",
    "forecast_category": "pipeline",
    "win_likelihood": 3,
    "custom": {"key": "from_campaign", "value": True},
}

opportunityEntry = {
    "uuid": "00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "owner": "test1@example.org",
    "pipeline": "New business 1",
    "pipeline_stage": "Discovery",
    "estimated_close_date": "2023-12-22",
    "currency": "USD",
    "amount_in_cents": 100,
    "type": "recurring",
    "forecast_category": "pipeline",
    "win_likelihood": 3,
    "custom": {"from_campaign": True},
    "created_at": "2024-03-13T07:33:28.356Z",
    "updated_at": "2024-03-13T07:33:28.356Z"
}

allOpportunities = {"entries": [opportunityEntry], "cursor": "cursor==", "has_more": True}


class CustomerTestCase(unittest.TestCase):
    """
    Tests complex nested structure & assymetric create/retrieve schema.
    """

    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/customers",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=allContacts,
        )

        config = Config("token")
        customers = Customer.all(config).get()

        expected = Customer._many(entries=[deserializedCustomer], has_more=True, cursor="cursor==")

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        # Complete comparing too complicated, would need to:
        #  1) sort all dictionaries,
        #  2) use special class/library for timezones (Python has no default)
        # self.assertEqual(str(customers), str(expected))
        # => check only first level fields are OK
        self.assertEqual(sorted(dir(customers)), sorted(dir(expected)))
        self.assertEqual(
            sorted(customers.entries[0].attributes.stripe),
            sorted(expected.entries[0].attributes.stripe),
        )
        self.assertEqual(
            sorted(customers.entries[0].attributes.clearbit),
            sorted(expected.entries[0].attributes.clearbit),
        )
        self.assertTrue(isinstance(customers.entries[0], Customer))

    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/customers",
            status_code=200,
            json=entry,
        )

        config = Config("token")
        Customer.create(config, data=createCustomer).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), sentCreateExpected)

    @requests_mock.mock()
    def test_search(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/customers/search?email=tralala@someemail.com",
            status_code=200,
            json=allContacts,
        )

        config = Config("token")
        result = Customer.search(config, email="tralala@someemail.com").get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {"email": ["tralala@someemail.com"]})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertTrue(isinstance(result, Customer._many))
        self.assertTrue(isinstance(result.entries[0], Customer))
        self.assertTrue(result.has_more)
        self.assertEqual(result.cursor, "cursor==")

    @requests_mock.mock()
    def test_merge(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/customers/merges", status_code=204
        )

        jsonRequest = {
            "from": {"customer_uuid": "cus_de305d54-75b4-431b-adb2-eb6b9e546012"},
            "into": {"customer_uuid": "cus_ab223d54-75b4-431b-adb2-eb6b9e234571"},
        }

        config = Config("token")
        result = Customer.merge(config, data=jsonRequest).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), jsonRequest)
        self.assertEqual(result, None)

    @requests_mock.mock()
    def test_connectSubscriptions(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/customers/cus_5915ee5a-babd-406b-b8ce-d207133fb4cb/connect_subscriptions",
            status_code=202,
        )

        jsonRequest = {
            "subscriptions": [
                {
                    "data_source_uuid": "ds_ade45e52-47a4-231a-1ed2-eb6b9e541213",
                    "external_id": "d1c0c885-add0-48db-8fa9-0bdf5017d6b0",
                },
                {
                    "data_source_uuid": "ds_ade45e52-47a4-231a-1ed2-eb6b9e541213",
                    "external_id": "9db5f4a1-1695-44c0-8bd4-de7ce4d0f1d4",
                },
            ]
        }
        config = Config("token")
        result = Customer.connectSubscriptions(
            config, uuid="cus_5915ee5a-babd-406b-b8ce-d207133fb4cb", data=jsonRequest
        ).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), jsonRequest)
        self.assertEqual(result, None)

    @requests_mock.mock()
    def test_modify_uuid_missing(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/customers/",
            status_code=400,
            json={
                "code": 400,
                "message": "Please pass 'uuid' parameter",
            },
        )

        jsonRequest = {"country": "US"}
        config = Config("token")

        with self.assertRaises(APIError) as context:
            result = Customer.modify(config, uuid="", data=jsonRequest).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue("Please pass \\'uuid\\' parameter" in str(context.exception))

    @requests_mock.mock()
    def test_modify(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/customers/cus_5915ee5a-babd-406b-b8ce-d207133fb4cb",
            status_code=200,
        )

        jsonRequest = {"country": "US"}
        config = Config("token")

        result = Customer.modify(
            config, uuid="cus_5915ee5a-babd-406b-b8ce-d207133fb4cb", data=jsonRequest
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), jsonRequest)

    @requests_mock.mock()
    def test_contacts(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/customers/cus_00000000-0000-0000-0000-000000000000/contacts",
            status_code=200,
            json=allContacts,
        )

        config = Config("token")
        contacts = Customer.contacts(config, uuid="cus_00000000-0000-0000-0000-000000000000").get()
        expected = Contact._many(**allContacts)

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(sorted(dir(contacts)), sorted(dir(expected)))
        self.assertTrue(isinstance(contacts.entries[0], Contact))
        self.assertEqual(contacts.cursor, "cursor==")
        self.assertTrue(contacts.has_more)

    @requests_mock.mock()
    def test_createContact(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/customers/cus_00000000-0000-0000-0000-000000000000/contacts",
            status_code=200,
            json=contact,
        )

        config = Config("token")
        expected = Customer.createContact(
            config, uuid="cus_00000000-0000-0000-0000-000000000000", data=createContact
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), createContact)
        self.assertTrue(isinstance(expected, Contact))

    @requests_mock.mock()
    def test_notes(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/customer_notes?customer_uuid=cus_00000000-0000-0000-0000-000000000000&cursor=ym9vewfo&per_page=1",
            status_code=200,
            json=allNotes,
        )

        config = Config("token")
        notes = Customer.notes(
            config,
            uuid="cus_00000000-0000-0000-0000-000000000000",
            cursor="ym9vewfo",
            per_page=1,
            ).get()
        expected = Customer._many(**allNotes)

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {'customer_uuid': ['cus_00000000-0000-0000-0000-000000000000'], 'cursor': ['ym9vewfo'], 'per_page': ['1']})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(sorted(dir(notes)), sorted(dir(expected)))
        self.assertTrue(isinstance(notes.entries[0], CustomerNote))
        self.assertEqual(notes.cursor, "cursor==")
        self.assertTrue(notes.has_more)

    @requests_mock.mock()
    def test_createNote(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/customer_notes",
            status_code=200,
            json=note,
        )

        config = Config("token")
        expected = Customer.createNote(
            config, uuid="cus_00000000-0000-0000-0000-000000000000", data=createNote
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), createNote)
        self.assertTrue(isinstance(expected, CustomerNote))

    @requests_mock.mock()
    def test_opportunities(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/opportunities?customer_uuid=cus_00000000-0000-0000-0000-000000000000&cursor=ym9vewfo&per_page=1",
            status_code=200,
            json=allOpportunities,
        )

        config = Config("token")
        opportunities = Customer.opportunities(
            config,
            uuid="cus_00000000-0000-0000-0000-000000000000",
            cursor="ym9vewfo",
            per_page=1).get()
        expected = Customer._many(**allOpportunities)

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {'customer_uuid': ['cus_00000000-0000-0000-0000-000000000000'], 'cursor': ['ym9vewfo'], 'per_page': ['1']})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(sorted(dir(opportunities)), sorted(dir(expected)))
        self.assertTrue(isinstance(opportunities.entries[0], Opportunity))
        self.assertEqual(opportunities.cursor, "cursor==")
        self.assertTrue(opportunities.has_more)

    @requests_mock.mock()
    def test_createOpportunity(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/opportunities",
            status_code=200,
            json=opportunity,
        )

        config = Config("token")
        expected = Customer.createOpportunity(
            config, uuid="cus_00000000-0000-0000-0000-000000000000", data=createOpportunity
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), createOpportunity)
        self.assertTrue(isinstance(expected, Opportunity))
