from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sb_dn/__init__.py
from sb_dn import __version__ as version

setup(
	name="sb_dn",
	version=version,
	description="SB",
	author="Usama",
	author_email="usamanaveed9263@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
