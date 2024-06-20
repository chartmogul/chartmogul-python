#!/usr/bin/env python
from __future__ import absolute_import
import os
import re
import sys

from codecs import open
from setuptools import setup

github_url = "https://github.com/chartmogul/chartmogul-python"

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

requires = [
    "requests>=2.31.0",
    "uritemplate>=4.1.1",
    "promise>=2.3.0",
    "marshmallow>=3.19.0",
    "future>=0.18.3",
    "urllib3==1.26.19",
]
test_requirements = [
    "mock>=5.1.0",
    "requests-mock>=1.11.0",
    "vcrpy>=4.4.0",
    "PyYAML>=6.0.1",
    "httpretty>=1.1.4",
    "wrapt>=1.15.0",
]

with open("chartmogul/version.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

setup(
    name="chartmogul",
    version=version,
    description="Python library for ChartMogul API.",
    long_description="`See documentation on GitHub <" + github_url + ">`_",
    author="Petr Kopac (ChartMogul Ltd.)",
    author_email="petr@chartmogul.com",
    url="https://chartmogul.com",
    download_url=github_url + "/tarball/v" + version,
    packages=[
        "chartmogul",
        "chartmogul.api",
        "chartmogul.api.customers",
    ],
    package_data={"": ["LICENSE", "NOTICE"], "chartmogul": ["*.pem"]},
    package_dir={
        "chartmogul": "chartmogul",
        "chartmogul.api": "chartmogul/api",
        "chartmogul.api.customers": "chartmogul/api/customers",
    },
    include_package_data=True,
    install_requires=requires,
    license="MIT",
    zip_safe=False,
    tests_require=test_requirements,
    test_suite="test",
    extras_require={},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
