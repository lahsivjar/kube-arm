"""
Installer for jarvis-control

TODO create other setup files
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from os import path

setup(
    name='jarvis',
    version='0.0.1',
    description='Jarvis Control is a CLI to run commands against a Jarvis Kube',

    long_description='Jarvis Control is a CLI to run commands against a Jarvis Kube',

    url='https://github.com/lahsivjar/jarvis-kube',

    author='Bharath',
    author_email='bharathb777@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='developer tools',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'jarvis=jarvis.jarvis:main',
        ],
    },
)