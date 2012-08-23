import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except IOError:
    README = CHANGES = ''

install_requires=['setuptools' ]
pyramid_requires=['pyramid', 'zope.interfaces']
test_requires = []

__version__ = "0.1"

setup(name='composite.snowflake',
      version=__version__,
      description='Snowflake: generator 64-bit unique identifiers',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: MIT/X",
      ],
      url="http://github.com/avnik/composite.traverser/",
      author="Alexander V. Nikolaev",
      author_email="avn@daemon.hole.ru",
      license="MIT/X",
      packages=find_packages(),
      namespace_packages = ['composite', 'composite.snowflake'],
      include_package_data=True,
      zip_safe=False,
      install_requires = install_requires,
      tests_require= test_requires,
      extras_require = {
          'test': test_requires,
          'pyramid': pyramid_requires,
      },
)

