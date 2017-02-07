import unittest
from chartmogul import Customer, Config
from chartmogul.api.customer import Attributes, Stripe, Clearbit,\
                                    Company, Person, Name, Employment, Address
from datetime import datetime
import requests_mock

from pprint import pprint

docsListSample = {
    "entries": [
        {
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
            "attributes":{
                "tags": ["engage", "unit loss", "discountable"],
                "stripe":{
                    "uid": 7,
                    "coupon": True
                },
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
                            "subIndustry": "Application Software"
                        },
                        "metrics": {
                            "raised": 1502450000,
                            "employees": 1000,
                            "googleRank": 7,
                            "alexaGlobalRank": 2319,
                            "marketCap": None
                        },
                    },
                    "person": {
                        "name": {
                            "fullName": "Bob Kramer"
                        },
                        "employment": {
                            "name": "Example Company"
                        }
                    }
                },
                "custom": {
                    "CAC": 213,
                    "utmCampaign": "social media 1",
                    "convertedAt": "2015-09-08 00:00:00",
                    "pro": False,
                    "salesRep": "Gabi"
                }
            },
            "address": {
                "address_zip": "0185128",
                "city": "Nowhereville",
                "country": "US",
                "state": "Alaska"
            },
            "mrr": 3000.0,
            "arr": 36000.0,
            "billing-system-url": "https:\/\/dashboard.stripe.com\/customers\/cus_4Z2ZpyJFuQ0XMb",
            "chartmogul-url": "https:\/\/app.chartmogul.com\/#customers\/25647-Example_Company",
            "billing-system-type": "Stripe",
            "currency": "USD",
            "currency-sign": "$"
        }
    ],
    "has_more": True,
    "per_page": 50,
    "page": 1,
    "current_page": 1,
    "total_pages": 4
}

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
        stripe=Stripe(
          uid=7,
          coupon=True
        ),
        clearbit=Clearbit(
            company=Company(
                name="Example Company",
                legalName="Example Company Inc.",
                domain="examplecompany.com",
                url="http://examplecompany.com",
                category={
                    "sector": "Information Technology",
                    "industryGroup": "Software and Services",
                    "industry": "Software",
                    "subIndustry": "Application Software"
                },
                metrics={
                    "alexaGlobalRank": 2319,
                    "googleRank": 7,
                    "employees": 1000,
                    "marketCap": None,
                    "raised": 1502450000
                },
            ),
            person=Person(
                name=Name(
                    fullName="Bob Kramer"
                ),
                employment=Employment(
                    name="Example Company"
                )
            )
        ),
        custom={
            "CAC": 213,
            "utmCampaign": "social media 1",
            "convertedAt": "2015-09-08 00:00:00",
            "pro": False,
            "salesRep": "Gabi"
        }
    ),
    address=Address(
        address_zip="0185128",
        city="Nowhereville",
        country="US",
        state="Alaska"
    ),
    mrr=3000.0,
    arr=36000.0,
    billing_system_url="https:\/\/dashboard.stripe.com\/customers\/cus_4Z2ZpyJFuQ0XMb",
    chartmogul_url="https:\/\/app.chartmogul.com\/#customers\/25647-Example_Company",
    billing_system_type="Stripe",
    currency="USD",
    currency_sign="$"
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
        "custom": [
            {'key': 'CAC', 'type': 'Integer', 'value': 213},
            {"key": "utmCampaign", "value": "social media 1", "type": "String"},
            {"key": "convertedAt", "value": datetime(
                2015, 9, 8), "type": "Timestamp"},
            {"key": "pro", "value": False, "type": "Boolean"},
            {"key": "salesRep", "value": "Gabi", "type": "String"}]
    }
}

sentCreateExpected = {
    'attributes': {
        'custom': [
            {'key': 'CAC', 'type': 'Integer', 'value': 213},
            {"key": "utmCampaign", "value": "social media 1", "type": "String"},
            {"key": "convertedAt", "value": "2015-09-08T00:00:00", "type": "Timestamp"},
            {"key": "pro", "value": False, "type": "Boolean"},
            {"key": "salesRep", "value": "Gabi", "type": "String"}
        ],
        'tags': ['engage', 'unit loss', 'discountable']},
    'city': 'Nowhereville',
    'company': '',
    'country': 'US',
    'customer-since': '2015-06-09T13:16:00',
    'data_source_uuid': 'ds_610b7a84-c50f-11e6-8aab-97d6db98913a',
    'email': 'bob@examplecompany.com',
    'external_id': '34916129',
    'free_trial_started_at': '2015-01-09T10:00:00',
    'lead_created_at': '2015-01-01T10:00:00',
    'name': 'Example Company',
    'state': 'Alaska',
    'zip': '0185128'
}


class CustomerTestCase(unittest.TestCase):
    """
    Tests complex nested structure & assymetric create/retrieve schema.
    """

    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            'GET',
            "https://api.chartmogul.com/v1/customers",
            request_headers={'Authorization': 'Basic dG9rZW46c2VjcmV0'},
            status_code=200,
            json=docsListSample
        )

        config = Config("token", "secret")
        customers = Customer.all(config).get()

        expected = Customer._many(
            entries=[deserializedCustomer],
            has_more=True,
            per_page=50,
            page=1,
            current_page=1,
            total_pages=4
        )

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        # Complete comparing too complicated, would need to:
        #  1) sort all dictionaries,
        #  2) use special class/library for timezones (Python has no default)
        # self.assertEqual(str(customers), str(expected))
        # => check only first level fields are OK
        self.assertEqual(sorted(dir(customers)), sorted(dir(expected)))

    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            'POST',
            "https://api.chartmogul.com/v1/customers",
            status_code=200,
            json=docsListSample["entries"][0]
        )

        config = Config("token", "secret")
        Customer.create(config, data=createCustomer).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), sentCreateExpected)

    @requests_mock.mock()
    def test_search(self, mock_requests):
        mock_requests.register_uri(
            'GET',
            "https://api.chartmogul.com/v1/customers/search?email=tralala@someemail.com",
            status_code=200,
            json=docsListSample
        )

        config = Config("token", "secret")
        result = Customer.search(config, email='tralala@someemail.com').get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {
                         'email': ['tralala@someemail.com']})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertTrue(isinstance(result, Customer._many))
        self.assertTrue(isinstance(result.entries[0], Customer))

    @requests_mock.mock()
    def test_merge(self, mock_requests):
        mock_requests.register_uri(
            'POST',
            "https://api.chartmogul.com/v1/customers/merges",
            status_code=204
        )

        jsonRequest = {
            "from": {"customer_uuid": "cus_de305d54-75b4-431b-adb2-eb6b9e546012"},
            "into": {"customer_uuid": "cus_ab223d54-75b4-431b-adb2-eb6b9e234571"}
        }

        config = Config("token", "secret")
        result = Customer.merge(config, data=jsonRequest).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), jsonRequest)
        self.assertEqual(result, None)
