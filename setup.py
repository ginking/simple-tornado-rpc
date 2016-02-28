from setuptools import setup, find_packages
import sys, os

version = '0.1.0'
README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read() + '\n\n'

setup(name='torpc',
    version=version,
    description=" Simple JSON RPC using the Tornado framework",
    long_description=long_description,
    classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0'
    ],
    keywords='simple tornado rpc',
    author='Li Xianbin',
    author_email='sparklxb@163.com',
    url='https://github.com/sparklxb/simple-tornado-rpc',
    license='MIT',
    install_requires=[
      # -*- Extra requirements: -*-
    ]
)