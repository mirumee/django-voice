from setuptools import setup, find_packages
import os

version = 'svn'

LONG_DESCRIPTION = """
============
Django Voice
============

This application lets you solicit feedback and suggestions from
your users, who can then vote and comment on other suggestions.
"""

setup(
    name='django-voice',
    version=version,
    description="django-voice",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='django,feedback,discussion',
    author='Huwshimi',
    author_email='huw@huwshimi.com',
    url='http://code.google.com/p/django-voice/',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)

