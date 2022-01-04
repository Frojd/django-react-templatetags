#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re
import sys

from setuptools import find_packages, setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()


with open("README.md") as f:
    readme = f.read()

# Convert markdown to rst
try:
    from pypandoc import convert_file

    long_description = convert_file("README.md", "rst")
except:
    long_description = ""

version = ""
with io.open("django_react_templatetags/__init__.py", "r", encoding="utf8") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

setup(
    name="django_react_templatetags",
    version=version,
    description=(
        "This django library allows you to add React components into your django templates."
    ),  # NOQA
    long_description=long_description,
    author="Fröjd",
    author_email="martin@marteinn.se",
    url="https://github.com/frojd/django-react-templatetags",
    packages=find_packages(exclude=("tests*", "example_django_react_templatetags")),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
    ],
    extras_require={
        "ssr": ["requests"],
        "hypernova": ["hypernova"],
    },
    tests_require=[
        "Django>=3.2",
        "requests",
    ],
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Topic :: Utilities",
        "Programming Language :: JavaScript",
    ],
)
