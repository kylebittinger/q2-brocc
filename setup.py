# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages
import versioneer

setup(
    name="q2-brocc",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    author="Kyle Bittinger",
    author_email="kylebittinger@gmail.com",
    description="QIIME2 plugin for the BROCC taxonomic classifier",
    license='BSD-3-Clause',
    url="https://github.com/kylebittinger/q2-brocc",
    install_requires=[
        'brocc',
    ],
    entry_points={
        'qiime2.plugins':
        ['q2-brocc=q2_brocc.plugin_setup:plugin']
    },
    package_data={
        'q2_brocc': ['citations.bib'],
        'q2_brocc.tests': ['data/*'],
    },
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
