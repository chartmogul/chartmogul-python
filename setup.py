#!/usr/bin/env python

import os
import re
import sys

from codecs import open
from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requires = []
test_requirements = ['mock>=2.0.0', 'requests-mock>=1.3.0']

with open('chartmogul/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='chartmogul',
    version=version,
    description='Python library for ChartMogul API.',
    long_description=readme,
    author='Petr Kopac',
    author_email='petr@chartmogul.com',
    url='https://chartmogul.com',
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
        'Programming Language :: Python :: 2.6',
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
    extras_require={},
)
