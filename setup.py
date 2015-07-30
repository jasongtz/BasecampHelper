#from distutils.core import setup
from setuptools import setup

setup(
    # Application name:
    name="BasecampHelper",

    # Version number (initial):
    version="0.1",

    # Application author details:
    author="Jason",

    # Packages
    packages=['basecamphelper'],

    # Include additional files into the package
    include_package_data=True,

    # Details
    #url="http://pypi.python.org/pypi/MyApplication_v010/",

    #
    license="MIT",
   # description="",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "requests",
        "requests[security]"
    ],

)