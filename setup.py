"""In progress project in UW's HCDE program.
"""

DOCLINES = __doc__.split("\n")

import sys

from setuptools import setup, find_packages
from codecs import open
from os import path
import os

os.environ["MPLCONFIGDIR"] = "."

# if sys.version_info[:2] < (2, 7):
#     raise RuntimeError("Python version 2.7 or greater required.")

setup(
  name='private_quotes',
  version='0.1.2',
  description=DOCLINES[0],
  packages=find_packages(),
  entry_points= {},
  author='Andrew Beers',
  author_email='albeers@uw.edu',
  url='https://github.com',  # use the URL to the github repo
  download_url='https://github.com/',
  keywords=[''],
  install_requires=[''],
  classifiers=[],
)
