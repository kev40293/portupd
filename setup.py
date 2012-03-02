#!/usr/bin/env python

import sys
from distutils.core import setup
from distutils.extension import Extension

setup(name='portupd', version='0.01',
      description='Portage tree auto sync daemon',
      author='Kevin Brandstatter',
      author_email='Kevin Brandstatter',
      packages=['portupdlib'], license="GPLv3",
      scripts=['portupd'],
      data_files=[('/etc', ['portup.conf']),
         ('/etc/init.d', ['scripts/portupd'])],
      requires=['portage', '_emerge']
      )

