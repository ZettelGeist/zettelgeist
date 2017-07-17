#
# setpath.sh: A script you can source to set the PATH and PYTHONPATH to find the ZettelGeist tools.
#
# Usage:
# $ source setpath.sh
#

# TODO: Make this is a bit smarter later.

export PYTHONPATH=$(pwd):$PYTHONPATH
export PATH=$(pwd)/bin:$PATH
env | grep PATH
