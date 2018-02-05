#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='neocities',
      version='0.1.0',
      description='Python API for NeoCities.org',
      classifiers=[
          'Topic :: Internet'
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
          ],
      license='LGPLv3',
      package_dir={'neocities': 'neocities'},
      install_requires=['requests',
                        'click',
                        'tabulate'],
      packages=find_packages('.'),
      entry_points="""\
[console_scripts]
neocities = neocities.neocli:main
      """,
      )
