#!/usr/bin/env sh

pip install twine

pushd $1
python setup.py sdist bdist_wheel --python-tag py3
twine upload dist/* --repository-url https://test.pypi.org/legacy/ -u bizhang -p $PYPI_PASSWORD

exit $?
