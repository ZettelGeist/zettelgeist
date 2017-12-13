# setup.py - placeholder for eventual setup script

from setuptools import setup

setup(
    name='zettelgeist',
    packages=['zettelgeist'],
    version='0.9',
    description='ZettelGeist - a historiographically focused notetaking system',
    author='ZettelGeist Laboratories',
    author_email='gkt@cs.luc.edu',
    license='Apache License 2.0',
    url='https://github.com/zettelgeist/zettelgeist',
    download_url='https://github.com/zettelgeist/zegttelgeist/archive/0.9.tar.gz',
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
    scripts=['bin/zcreate',
             'bin/zimport',
             'bin/zfind',
             'bin/zettel']
)
