# -*- coding: utf-8 -*-
from .api.config import Config
from .errors import APIError, ConfigurationError, ArgumentMissingError

from .api.activity import Activity
from .api.attributes import Attributes
from .api.custom_attrs import CustomAttributes
from .api.customer import Customer
from .api.data_source import DataSource
from .api.invoice import Invoice
from .api.metrics import Metrics
from .api.ping import Ping
from .api.plan import Plan
from .api.subscription import Subscription
from .api.tags import Tags
from .api.transaction import Transaction

# Deprecated
import imp


"""
ChartMogul API Python Client

Provides convenient Python bindings for ChartMogul's API.

:copyright: (c) 2017 by ChartMogul Ltd.
:license: MIT, see LICENSE for more details.
"""

__title__ = 'chartmogul'
__version__ = '1.1.7'
__build__ = 0x000000
__author__ = 'ChartMogul Ltd'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 ChartMogul Ltd'
