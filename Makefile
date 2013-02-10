build:
	pip install -e .
	pip install "file://`pwd`#egg=django-login-as[tests]"

test: build
	python runtests.py -x