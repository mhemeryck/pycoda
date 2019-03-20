from __future__ import unicode_literals

import os
import sys

from setuptools import setup
from setuptools.command.install import install

import pycoda

install_requires = ("factory-boy",)


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")

        if tag != pycoda.__version__:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, pycoda.__version__
            )
            sys.exit(info)


def readme():
    """print long description"""
    with open("README.md") as f:
        return f.read()


setup(
    name="codapy",
    version=pycoda.__version__,
    description="Coded statement of Account (CODA) python API",
    long_description=readme(),
    long_description_content_type="text/markdown",
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
    cmdclass={"verify": VerifyVersionCommand},
)
