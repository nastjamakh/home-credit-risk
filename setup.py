from setuptools import setup

PACKAGE_NAME = "home-credit"
VERSION = "0.2.0"

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    py_modules=["home-credit"],
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        hc=src/entrypoint:cli
    """,
)
