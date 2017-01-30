# -*- coding: utf-8 -*-
import logging

from .api.data_source import DataSource
from .api.plan import Plan
from .api.config import Config, ping
from .errors import APIError, ConfigurationError
from . import imp
from . import metrics
from . import enrichment
# from . import customer, data_source
# from .imp import invoice, subscription, transaction
# from .enrichment import custom_attribute
# from .metrics import customer

"""
ChartMogul API Python Client

Provides convenient Python bindings for ChartMogul's API.

:copyright: (c) 2017 by ChartMogul Ltd.
:license: MIT, see LICENSE for more details.
"""

__title__ = 'chartmogul'
__version__ = '0.0.1'
__build__ = 0x000000
__author__ = 'ChartMogul Ltd'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 ChartMogul Ltd'



# Set default logging handler to avoid "No handler found" warnings.

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
