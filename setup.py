#!/usr/bin/env python
from __future__ import absolute_import
import os
import re
import sys

from codecs import open
from setuptools import setup

github_url = 'https://github.com/chartmogul/chartmogul-python'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requires = [
    'requests>=2.10.0',
    'uritemplate>=3.0.0',
    'promise>=1.0.1',
    'marshmallow>=3.10.0',
    'future>=0.16.0',
]
test_requirements = [
    # This is needed to circumvent a vcrpy dependency problem And can be
    # deleted once it is solved.
    'yarl; python_version>"3.5"',
    'yarl<1.4; python_version=="3.5"',

    'mock>=1.0.1',
    'requests-mock>=1.3.0',
    'vcrpy>=1.11.1',
    'PyYAML>=5.1.2',
    'httpretty>=0.9.6',
    'wrapt>=1.11.2'
]

with open('chartmogul/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='chartmogul',
    version=version,
    description='Python library for ChartMogul API.',
    long_description='`See documentation on GitHub <' + github_url + '>`_',
    author='Petr Kopac (ChartMogul Ltd.)',
    author_email='petr@chartmogul.com',
    url='https://chartmogul.com',
    download_url = github_url + '/tarball/v' + version,
    packages=['chartmogul', 'chartmogul.api', 'chartmogul.imp'],
    package_data={'': ['LICENSE', 'NOTICE'], 'chartmogul': ['*.pem']},
    package_dir={'chartmogul': 'chartmogul', 'chartmogul.api': 'chartmogul/api', 'chartmogul.imp': 'chartmogul/imp'},
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    tests_require=test_requirements,
    test_suite="test",
    extras_require={},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
