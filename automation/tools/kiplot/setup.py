# -*- coding: utf-8 -*-

import io
import os

from setuptools import setup, find_packages

# Package meta-data.
NAME = 'kiplot'
DESCRIPTION = 'Plotting driver for KiCad'
URL = 'https://github.com/johnbeard/kiplot'
EMAIL = 'john.j.beard@gmail.com'
AUTHOR = 'John Beard'
REQUIRES_PYTHON = '>=2.7.0'


# What packages are required for this module to be executed?
REQUIRED = [
    'pyyaml',
    # 'pcbnew'
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


about = {}
with open(os.path.join(here, 'src', NAME, '__version__.py')) as f:
    exec(f.read(), about)


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    entry_points={
         'console_scripts': ['kiplot=kiplot.__main__:main'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
