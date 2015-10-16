# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='El-Mapper',
    version=version,
    description="The El Mapper project",
    long_description="",
    classifiers=[
        'Framework :: Django :: 1.8',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
    ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='mapper django',
    author=u'Romain Commandé',
    author_email='commande.romain@gmail.com',
    url='http://www.rcomman.de',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django==1.8.5',
    ],
    extras_require={
        'develop': [
            'ipython',
            'ipdb',
        ]
    },
    entry_points=""" # -*- Entry points: -*- """,
)
