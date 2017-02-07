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

requires = []
test_requirements = ['mock>=1.0.1', 'requests-mock>=1.3.0']

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
    packages=['chartmogul'],
    package_data={'': ['LICENSE', 'NOTICE'], 'chartmogul': ['*.pem']},
    package_dir={'chartmogul': 'chartmogul'},
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries'
    ),
    tests_require=test_requirements,
    test_suite="test",
    extras_require={},
)
