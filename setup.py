#!/usr/bin/python
from setuptools import setup
#import os


#here = os.path.abspath(os.path.dirname(__file__))
#try:
#    with open(os.path.join(here, 'README.md')) as f:
#        README = f.read()
#    with open(os.path.join(here, 'CHANGES.txt')) as f:
#        CHANGES = f.read()
#except IOError:
#    README = CHANGES = ''


setup(
    name='agora',
    version='0.0.1',
    author='beg0',
    author_email='beg0@free.fr',
    packages=['agora'],
    url='https://github.com/beg0/agora',
    license='MIT',
    description='Another Generator Of Rest Api.',
    long_description="AGORA is a library to generate client-side accessors for HTTP REST API.",
    install_requires=[
        'setuptools',
        'six',
        'pyraml-parser>=0.1.7',
        'requests',
        'flex',
    ],
    #zip_safe=True,
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],
)
