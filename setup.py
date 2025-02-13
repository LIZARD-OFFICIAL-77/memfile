from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
with codecs.open(os.path.join(here, "LICENSE"), encoding="utf-8") as fh:
    license = "\n" + fh.read()

VERSION = '{{VERSION_PLACEHOLDER}}'
DESCRIPTION = 'memfiles - normal files that store contents in RAM.'

# Setting up
setup(
    name="memfile",
    version=VERSION,
    author="LIZARD-OFFICIAL-77",
    author_email="<lizard.official.77@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=(),
    keywords=[
        'linux',
        'fs',
        'filesystems',
        'memory',
        'temporary',
        'sharedmemory'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
    license=license,
    project_urls={
        'Source Code': 'https://github.com/LIZARD-OFFICIAL-77/memfile',  # GitHub link
        'Bug Tracker': 'https://github.com/LIZARD-OFFICIAL-77/memfile/issues',  # Link to issue tracker
    },
    include_package_data=True,
    url = "https://github.com/LIZARD-OFFICIAL-77/memfile"
)