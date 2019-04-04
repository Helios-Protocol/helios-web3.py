#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    find_packages,
    setup,
)


setup(
    name='helios_web3',
    version='5.0.1',
    description="""Helios version of Web3.py""",
    long_description_markdown_filename='README.rst',
    author='Tommy Mckinnon',
    author_email='tommy@heliosprotocol.io',
    url='https://github.com/Helios-Protocol/helios_web3.py',
    include_package_data=True,
    install_requires=[
        "web3>=4.0.0,<6.0.0",
        "eth-abi>=2.0.0b6,<3.0.0",
        "eth-account>=0.2.1,<0.4.0",
        "eth-hash[pycryptodome]>=0.2.0,<1.0.0",
        "eth-typing>=2.0.0,<3.0.0",
        "eth-utils>=1.3.0,<2.0.0",
        "ethpm>=0.1.4a12,<1.0.0",
        "hexbytes>=0.1.0,<1.0.0",
        "lru-dict>=1.1.6,<2.0.0",
        "requests>=2.16.0,<3.0.0",
        "pypiwin32>=223;platform_system=='Windows'",
    ],
    setup_requires=['setuptools-markdown'],
    python_requires='>=3.6,<4',
    license="MIT",
    zip_safe=False,
    keywords='ethereum, helios protocol',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)