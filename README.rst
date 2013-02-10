django-login-as
===============

A simple middleware which allows a superuser to login as another user and view the site on their behalf.


Install
-------

Install the package:

::

	pip install django-login-as


Add the middleware:

::

	MIDDLEWARE_CLASSES = (
		'loginas.LoginAsHookMiddleware',
	)

Register the application within INSTALLED_APPS:

::

	INSTALLED_APPS = (
		'loginas',
	)

Make sure the application loader is available for templates:

::

	TEMPLATE_LOADERS = (
		'django.template.loaders.app_directories.Loader',
	)


Usage
-----

Load any page with an html response type and you'll see a new toolbar at the top of the page. Enter a username to change who you're viewing the site as.
