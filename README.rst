django-view-as
==============

A simple middleware which allows a superuser to view the site on behalf of another user.


Install
-------

Install the package:

::

	pip install django-view-as


Add the middleware:

::

	MIDDLEWARE_CLASSES = (
		'viewas.ViewAsMiddleware',
	)

Register the application within INSTALLED_APPS:

::

	INSTALLED_APPS = (
		'django.contrib.auth',
		'django.contrib.sessions',
		'viewas',
	)

Make sure the application loader is available for templates:

::

	TEMPLATE_LOADERS = (
		'django.template.loaders.app_directories.Loader',
	)


Usage
-----

Load any page with an html response type and you'll see a new toolbar at the top of the page. Enter a username to change who you're viewing the site as.
