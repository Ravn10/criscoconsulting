from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in tritorc_manufacturing/__init__.py
from tritorc_manufacturing import __version__ as version

setup(
	name="cirscoconsulting",
	version=version,
	description="customisation",
	author="Firsterp",
	author_email="support@firsterp.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
