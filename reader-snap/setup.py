
from setuptools import setup


setup(name='reader-snap',


      version='0.1dev1',
      description='A test snap to read configs from another snap',

      author='Muhammad Yahya & Felix Forster @ OLI Systems 2020',
      url='https://github.com/olisystems/intersnap-com-demo.git',
      packages=['reader_main.reader_pkg', 'reader_main'],
      install_requires=['click', 'toml', ],

      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Topic :: Utilities",
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Operating System :: POSIX :: Linux", ],

      entry_points={
          'console_scripts': [
              'reader-snap = reader_main.reader_main:init'
          ]
      },

      )
