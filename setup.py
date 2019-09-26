"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='grpc-utils',  # Required
    version='1.0.0',  # Required
    description='Utils for working with gRPC in Python',  # Required

    long_description=long_description,  # Optional

    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/AlekzanderDee/grpc-utils',  # Optional
    author='Alexander Dultsev',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    license='MIT',

    keywords='grpc development',  # Optional

    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'venv']),  # Required

    install_requires=[
        'grpcio>=1.22.0',
    ],  # Optional
)
