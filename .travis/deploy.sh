#!/usr/bin/env sh

pushd $1
python setup.py sdist bdist_wheel --python-tag py3
twine upload -s dist/* --repository-url https://test.pypi.org/legacy/ -u bizhang -p $PYPI_PASSWORD
popd