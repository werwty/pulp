#!/usr/bin/env sh
set -e

pip install twine

pushd pulpcore
python setup.py sdist bdist_wheel --python-tag py3
twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u PYPI_USER -p PYPI_PASSWORD
popd

pushd plugin
python setup.py sdist bdist_wheel --python-tag py3
twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u PYPI_USER -p PYPI_PASSWORD
popd

pushd common
python setup.py sdist bdist_wheel --python-tag py3
twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u PYPI_USER -p PYPI_PASSWORD
popd
