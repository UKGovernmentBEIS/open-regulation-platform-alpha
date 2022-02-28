import setuptools
import os

#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="orp_alpha_python_tools",
    version="0.0.1",
    author="Alastair McKinley",
    author_email="a.mckinley@analyticsengines.com",
    description="Python utilities for ORP Alpha",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    package_data={'': ['xmltools/test/akn2html.sef.json']},
    include_package_data=True,
    python_requires='>=3.7',
    install_requires= [
        "lxml==4.6.3",
        "pytest==6.2.4"
    ]
)