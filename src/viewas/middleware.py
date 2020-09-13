import logging
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import smart_text
from django.contrib.auth.models import AnonymousUser


assert 'django.contrib.auth' in settings.INSTALLED_APPS
assert 'django.contrib.sessions' in settings.INSTALLED_APPS
assert 'viewas' in settings.INSTALLED_APPS

if hasattr(settings, 'AUTH_USER_MODEL'):
    from django.contrib.auth import get_user_model

    User = get_user_model()
else:
    from django.contrib.auth.models import User

# tilda (192) as default key
VIEWAS_TOGGLE_KEY = getattr(settings, 'VIEWAS_TOGGLE_KEY', 192)

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
        selector = User.USERNAME_FIELD + '__iexact'
        query = {selector: username}
        try:
            return User.objects.get(**query)
        except ObjectDoesNotExist:
            # try to look up by email
            if '@' in username:
                try:
                    return User.objects.get(email__iexact=username)
                except (MultipleObjectsReturned, ObjectDoesNotExist):
                    return None
        return None

    def login_as(self, request, username):
        if request.user.get_username().lower() == username.lower():
            return

        if username == '':
            if 'login_as' in request.session:
                del request.session['login_as']
            return

        self.logger.info(
            'User %r forced a login as %r at %s',
            request.user.get_username(), username, request.get_full_path(),
            extra={'request': request})

        user = self.get_user(username)
        if user:
            request.user = user
            request.session['login_as'] = request.user.get_username()
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
                smart_text(response.content),
                self.tag,
                smart_text(self.render(request) + self.tag))
            if response.get('Content-Length', None):
                response['Content-Length'] = len(response.content)
        return response

    def render(self, request):
        if not isinstance(request.user, AnonymousUser):
            request.user.username = request.user.get_username()
        if hasattr(request, 'actual_user'):
            request.actual_user.username = request.actual_user.get_username()
        return render_to_string('viewas/header.html', {
            'VIEWAS_TOGGLE_KEY': VIEWAS_TOGGLE_KEY,
            'request': request,
        })


class ViewAsMiddleware(ViewAsHookMiddleware, ViewAsRenderMiddleware):
    pass
