import os

from setuptools import setup

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + "/requirements.txt"
install_requires = []  # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]

if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name="PSEData",
    version="0.1",
    description="Accessing and updating data from PSE",
    url="#",
    author="Joseph Bonilla",
    author_email="bonillajeb@gmail.com",
    license="MIT",
    packages=["pse_data", "pse_data/data"],
    zip_safe=False,
    install_requires=install_requires,
)
