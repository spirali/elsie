cd `dirname $0`/..
isort --profile black elsie tests
black elsie tests
flake8 elsie tests --ignore=E203,W503
