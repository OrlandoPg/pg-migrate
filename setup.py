#!/usr/bin/env python2.7

from distutils.core import setup

setup(name='PG Migrate', version='0.1',
    description='DB Migration Assistant for PostgreSQL',
    author='David Rogers', author_email='david@orlandopy.org',
    url='https://github.com/OrlandoPg/pg-migrate/',
    packages=['migrations'],
    requires=['decorator'], provides=['pg-migrate'],
    scripts=['bin/migrations'],
)
