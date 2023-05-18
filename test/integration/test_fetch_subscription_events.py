import unittest
from chartmogul import Config, SubscriptionEvent

config = Config(api_key = '85315c0a8b2b281ccb2352790ab373fd')

class FetchSubscriptionEventsTestCase(unittest.TestCase):
    def test_subscription_events(self):
        result = SubscriptionEvent.all(config).get()
        print(result)