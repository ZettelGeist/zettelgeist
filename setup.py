# setup.py - placeholder for eventual setup script

from setuptools import setup
from zettelgeist import zversion

setup(
    name='zettelgeist',
    packages=['zettelgeist'],
    version=zversion.version(),
    description='ZettelGeist - a historiographically focused notetaking system',
    author='ZettelGeist Laboratories',
    author_email='gkt@cs.luc.edu',
    license='Apache License 2.0',
    url='https://github.com/zettelgeist/zettelgeist',
    keywords=['notetaking', 'YAML', 'Markdown', 'sqlite3', 'GitHub'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.0',
        'License :: OSI Approved :: Apache Software License'
    ],
    python_requires='>=3',
    install_requires=[
        'PyYAML',
        'tatsu'
    ],
    entry_points = {
        'console_scripts': [
            'zcreate = zettelgeist.zcreate:main',
            'zimport = zettelgeist.zimport:main',
            'zfilter = zettelgeist.zfilter:main',
            'zfind = zettelgeist.zfind:main',
            'zettel = zettelgeist.zettel:main'
            ]
    }
)
