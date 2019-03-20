from __future__ import unicode_literals

from setuptools import setup

import pycoda

install_requires = ("factory-boy",)


setup(
    name="codapy",
    version=pycoda.__version__,
    description="Coded statement of Account (CODA) python API",
    url="https://github.com/mhemeryck/pycoda",
    install_requires=install_requires,
    author="Martijn Hemeryck",
    author_email="martijn.hemeryck@gmail.com",
    license="MIT",
    packages=["pycoda"],
    zip_safe=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business :: Financial :: Accounting",
    ],
)
