#!/usr/bin/env python3
import os
from setuptools import setup


def read(fname,
         ):
    """Utility function to read the README file.

    Notes
    -----
    This is used for the long_description.
    """
    return open(os.path.join(os.path.dirname(__file__),
                             fname),
                'r').read()


setup(name="pycaptcha",
      version="0.2.0",
      author="Gabriel Paul 'Cley Faye' Risterucci",
      author_email="gabriel.risterucci@gmail.com",
      description=("Perform server-side verification of a reCAPTCHA challenge."
                   ),
      license="MIT",
      keywords="recaptcha server-side django",
      url="https://repos.cleyfaye.net/trac/pycaptcha",
      packages=['pycaptcha',
                'pycaptcha.django',
                ],
      install_requires=['requests>=2'],
      long_description=read('README.md'),
      python_requires='>=3',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Framework :: Django",
          "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
          "License :: OSI Approved :: MIT License",
      ],
      )
