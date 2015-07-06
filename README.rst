django-view-as
==============

A simple middleware which allows a superuser to view the site on behalf of another user.

This idea originated within Disqus, and has served quite well in helping debug user problems.


Install
-------

Install the package:

::

	pip install django-view-as


Add the middleware:

::

	MIDDLEWARE_CLASSES = (
		'viewas.middleware.ViewAsMiddleware',
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

Load any page with an html response type, hit the tilda key (~), and you'll see a new toolbar at the bottom of the page. Enter a username to change who you're viewing the site as.


Configure the menu toggle key
-----------------------------

The following configuration option could be set in your settings.py to change the default keystroke to toggle the "View as" menu. Its value is the javascript key number that will be matched in the `keydown` event handler.

::
	
	VIEWAS_TOGGLE_KEY = 119  # F8


If you need more complex behavior (such as not binding based on the superuser attribute), check out the source the middleware is designed to be extensibile.

