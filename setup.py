from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in item_price/__init__.py
from item_price import __version__ as version

setup(
	name="item_price",
	version=version,
	description="Item Price Set From Item Master",
	author="Invento Software Limited",
	author_email="munim@invento.com.bd",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
