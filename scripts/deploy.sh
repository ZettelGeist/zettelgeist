#
# Deploy to PyPI. Don't run this script.
#

rm -rf dist/*
python setup.py sdist bdist_wheel
twine upload --repository pypi dist/*

