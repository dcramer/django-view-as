import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import smart_unicode


assert 'django.contrib.auth' in settings.INSTALLED_APPS
assert 'django.contrib.sessions' in settings.INSTALLED_APPS
assert 'viewas' in settings.INSTALLED_APPS


_HTML_TYPES = ('text/html', 'application/xhtml+xml')


def replace_insensitive(string, target, replacement):
    """
    Similar to string.replace() but is case insensitive
    Code borrowed from: http://forums.devshed.com/python-programming-11/case-insensitive-string-replace-490921.html
    """
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    if index >= 0:
        return string[:index] + replacement + string[index + len(target):]
    # no results so return the original string
    return string


class BaseMiddleware(object):
    def can_run(self, request):
        if not hasattr(request, 'user'):
            return False
        user = getattr(request, 'actual_user', request.user)
        return user.is_superuser


class ViewAsHookMiddleware(BaseMiddleware):
    """
    Authenticates a superuser as another user assuming a session variable is present.
    """
    logger = logging.getLogger('viewas')

    def get_user(self, username):
        try:
            return User.objects.get(username__iexact=username)
        except ObjectDoesNotExist:
            # try to look up by email
            if '@' in username:
                try:
                    return User.objects.get(email__iexact=username)
                except (MultipleObjectsReturned, ObjectDoesNotExist):
                    return None
        return None

    def login_as(self, request, username):
        if request.user.username.lower() == username.lower():
            return

        if username == '':
            if 'login_as' in request.session:
                del request.session['login_as']
            return

        self.logger.info(
            'User %r forced a login as %r', request.user.username, username,
            extra={'request': request})

        user = self.get_user(username)
        if user:
            request.user = user
            request.session['login_as'] = request.user.username
        else:
            messages.warning(request, "Did not find a user matching '%s'" % (username,))
            if 'login_as' in request.session:
                del request.session['login_as']

    def process_request(self, request):
        if not self.can_run(request):
            return

        request.actual_user = request.user

        if 'login_as' in request.POST:
            self.login_as(request, request.POST['login_as'])
            return HttpResponseRedirect(request.get_full_path())

        elif 'login_as' in request.session:
            self.login_as(request, request.session['login_as'])


class ViewAsRenderMiddleware(BaseMiddleware):
    tag = u'</body>'

    def process_response(self, request, response):
        if not self.can_run(request):
            return response

        if ('gzip' not in response.get('Content-Encoding', '') and
                response.get('Content-Type', '').split(';')[0] in _HTML_TYPES):
            response.content = replace_insensitive(
                smart_unicode(response.content),
                self.tag,
                smart_unicode(self.render(request) + self.tag))
            if response.get('Content-Length', None):
                response['Content-Length'] = len(response.content)
        return response

    def render(self, request):
        return render_to_string('viewas/header.html', {
            'request': request,
        })


class ViewAsMiddleware(ViewAsHookMiddleware, ViewAsRenderMiddleware):
    pass
