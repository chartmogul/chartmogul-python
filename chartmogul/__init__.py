# -*- coding: utf-8 -*-
from .api.config import Config
from .errors import (
    APIError,
    ConfigurationError,
    ArgumentMissingError,
    DeprecatedArgumentError,
)

from .api.customers.activity import CustomerActivity
from .api.attributes import Attributes
from .api.custom_attrs import CustomAttributes
from .api.customer import Customer
from .api.customer_note import CustomerNote
from .api.contact import Contact
from .api.data_source import DataSource
from .api.invoice import Invoice
from .api.metrics import Metrics
from .api.opportunity import Opportunity
from .api.ping import Ping
from .api.plan import Plan
from .api.plan_group import PlanGroup
from .api.subscription_event import SubscriptionEvent
from .api.customers.subscription import CustomerSubscription
from .api.customers.subscription import CustomerSubscription as Subscription
from .api.tags import Tags
from .api.transaction import Transaction
from .api.account import Account
from .api.activity import Activity
from .api.activities_export import ActivitiesExport

from .version import __version__


"""
ChartMogul API Python Client

Provides convenient Python bindings for ChartMogul's API.

:copyright: (c) 2023 by ChartMogul Ltd.
:license: MIT, see LICENSE for more details.
"""

__title__ = "chartmogul"
__build__ = 0x000000
__author__ = "ChartMogul Ltd"
__license__ = "MIT"
__copyright__ = "Copyright 2023 ChartMogul Ltd"
