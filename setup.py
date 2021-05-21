import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="jsonify-opening-hours",
    version="0.4.0",
    description="Parses opening hours from various human-readable strings into a standard JSON format",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MoralCode/jsonify-opening-hours",
    author="Adrian Edwards",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=["pyparsing",],
)
