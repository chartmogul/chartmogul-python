import unittest
import vcr
from chartmogul import Config, SubscriptionEvent

config = Config(api_key="-")


class FetchSubscriptionEventsTestCase(unittest.TestCase):
    """
    Tests errors & user mistakes.
    """

    @vcr.use_cassette("fixtures/fetch_subscription_events.yaml", filter_headers=["authorization"])
    def test_subscription_events(self):
        result = SubscriptionEvent.all(config).get()
