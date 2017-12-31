# ZettelGeist

[![Build Status](https://www.travis-ci.org/ZettelGeist/zettelgeist.svg?branch=master)](https://www.travis-ci.org/ZettelGeist/zettelgeist)

# Overview

ZettelGeist is a plaintext notetaking system inspired by the Zettelkasten approach. As this README is intended to be minimal,
we encourage you to visit http://zettelgeist.com for additional details.

# Installation

Installation is done via PyPI.
```
pip install zettelgeist
```

Power users can install by checking out the repo and running `setup.py` to install.

We recommend that you use a virtualenv as we are still in beta.

# Features

- A zettel is a "note card"
- Zettels written using YAML
- Zettels indexed using sqlite with FTS extensions
- Zettel searched using a query language (ZQL = Zettel Query Language) similar to Gmail's search operators
- Search results are rendered as a folder of zettels
- Replacement can be done on a set of notes to change any YAML field
- command-line and text editor driven workflow

For details, please see the main web site. This is where we'll provide full user documentation and recipes to help you get started.
We are developer-users of this project and are presently working on our own book. ZettelGeist is being used to organize all of the 
research for our book. So if it doesn't work for us, it probably won't work for you!