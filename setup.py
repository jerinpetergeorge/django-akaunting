from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the version from Version.txt
with open("VERSION.txt") as fp:
    __version__ = fp.read().strip()

# get the dependencies and installs
requirements_path = "requirements/install_requires.txt"
with open(path.join(here, requirements_path), encoding="utf-8") as fp:
    all_reqs = fp.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = [
    x.strip().replace("git+", "") for x in all_reqs if x.startswith("git+")
]

root_package = "akaunting"
_find_packages = [
    f"{root_package}.{item}" for item in find_packages(where=root_package)
]
packages = [root_package, *_find_packages]
setup(
    name="django-akaunting",
    version=__version__,
    description="A Django version of Akaunting",
    long_description="",
    license="BSD",
    packages=packages,
    include_package_data=True,
    author="Jerin Peter George",
    author_email="jerinpetergeorge@gmail.com",
    install_requires=install_requires,
    dependency_links=dependency_links,
)
