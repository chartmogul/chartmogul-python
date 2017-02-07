import unittest
from chartmogul import CustomAttributes, Config, APIError, Customer
from datetime import datetime
import requests_mock
from pprint import pprint

# First case data
dictData = {
    'custom': [
        {'type': 'String', 'key': 'channel',
            'value': 'Facebook'},
        {'type': 'Integer',
            'key': 'age', 'value': 8},
        {'type': 'Timestamp',
            'key': 'convertedAt', 'value': datetime(2015, 9, 8, 0, 0, 0)}
    ]
}

jsonData = {
    'custom': [
        {'type': 'String', 'key': 'channel',
            'value': 'Facebook'},
        {'type': 'Integer',
            'key': 'age', 'value': 8},
        {'type': 'Timestamp',
            'key': 'convertedAt', 'value': '2015-09-08 00:00:00'}
    ]
}

simpleJSONResult = {
    'custom': {
        'CAC': 213,
        'utmCampaign': 'social media 1',
        'convertedAt': '2015-09-08 00:00:00',
        'pro': False,
        'salesRep': 'Gabi',
        'channel': 'Facebook',
        'age': 8
    }
}

# Second case data

jsonRequest2 = {
    "email": "adam@smith.com",
    "custom": [
             {"type": "String", "key": "channel", "value": "Facebook"}
    ]
}

jsonResponse2 = {
    "entries": [
        {
            "id": 25647,
            "uuid": "cus_de305d54-75b4-431b-adb2-eb6b9e546012",
            "external_id": "40574176",
            "email": "adam@smith.com",
            "name": "Smith Company",
            "customer-since": "2015-06-09T13:16:00-04:00",
            "status": "Active",
            "attributes": {
                "tags": ["important", "Prio1"],
                "stripe": {
                    "coupon": True
                },
                "clearbit": {
                    "name": "Acme"
                },
                "custom": {
                    "channel": "Facebook"
                }
            }
        },
        {
            "id": 13456,
            "uuid": "cus_fb305d54-75b4-431b-2334-eb6b9e540016",
            "external_id": "58473129",
            "email": "adam@smith.com",
            "name": "Adam",
            "customer-since": "2015-06-10T13:16:00-04:00",
            "status": "Active",
            "attributes": {
                "tags": ["important", "Prio1"],
                "stripe": {
                    "coupon": False
                },
                "clearbit": {
                    "name": "Umbrella Corp."
                },
                "custom": {
                    "channel": "Facebook"
                }
            }
        }
    ]
}

expected2Str = ("Customers(entries=[<Customer{attributes=<Attributes{"
                "clearbit=<Clearbit{}>, custom={'channel': 'Facebook'"
                "}, stripe=<Stripe{coupon=True}>, tags=['important', "
                "'Prio1']}>, customer_since=datetime.datetime(2015, 6, 9, 13, "
                "16, tzinfo=tzoffset(None, -14400)), email='adam@smith.com', "
                "external_id='40574176', id=25647, name='Smith Company', "
                "status='Active', uuid='cus_de305d54-75b4-431b-adb2-"
                "eb6b9e546012'}>, <Customer{attributes=<Attributes{"
                "clearbit=<Clearbit{}>, custom={'channel': 'Facebook'"
                "}, stripe=<Stripe{coupon=False}>, tags=['important', "
                "'Prio1']}>, customer_since=datetime.datetime(2015, 6, 10, 13, "
                "16, tzinfo=tzoffset(None, -14400)), email='adam@smith.com', "
                "external_id='58473129', id=13456, name='Adam', "
                "status='Active', uuid='cus_fb305d54-75b4-431b-2334-"
                "eb6b9e540016'}>])")

class CustomAttributesTestCase(unittest.TestCase):
    """
    Tests asymmetric custom attributes' schema.
    """

    @requests_mock.mock()
    def test_add(self, mock_requests):
        mock_requests.register_uri(
            'POST',
            'https://api.chartmogul.com/v1/customers/CUSTOMER_UUID/attributes/custom',
            status_code=200,
            json=simpleJSONResult
        )

        expected = CustomAttributes(**simpleJSONResult)

        config = Config('token', 'secret')
        result = CustomAttributes.add(config,
                                      uuid='CUSTOMER_UUID',
                                      data=jsonData).get()

        self.assertEqual(mock_requests.call_count, 1, 'expected call')
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), jsonData)
        self.assertTrue(isinstance(result, CustomAttributes))
        self.assertEqual(result.custom['CAC'], expected.custom['CAC'])
        self.assertEqual(result.custom['utmCampaign'], expected.custom['utmCampaign'])
        self.assertEqual(result.custom['convertedAt'], expected.custom['convertedAt'])
        self.assertEqual(result.custom['pro'], expected.custom['pro'])
        self.assertEqual(result.custom['salesRep'], expected.custom['salesRep'])

    @requests_mock.mock()
    def test_add_to_email(self, mock_requests):
        mock_requests.register_uri(
            'POST',
            'https://api.chartmogul.com/v1/customers/CUSTOMER_UUID/attributes/custom',
            status_code=200,
            json=jsonResponse2
        )

        config = Config('token', 'secret')
        result = CustomAttributes.add(config,
                                      uuid='CUSTOMER_UUID',
                                      data=jsonRequest2).get()

        self.assertEqual(mock_requests.call_count, 1, 'expected call')
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), jsonRequest2)
        self.assertEqual(str(result), expected2Str)
