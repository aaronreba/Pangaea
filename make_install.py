#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("common", ["common.pyx"]),
               Extension("actor", ["actor.pyx"])]

setup(
  name = 'Common for Pangaea',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)


setup(
  name = 'Actor for Pangaea',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
