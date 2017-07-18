"""Mixin to prevent access to a view based on a reCAPTCHA challenge"""
from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.views import View
from .recaptcha import check


class RecaptchaMixin(View):
    """Restrict access to a view based on a reCAPTCHA challenge.

    Notes
    -----
    When the view is called, the reCAPTCHA challenge is checked, which mean it
    can't be checked a second time (reCAPTCHA response tokens can only be
    checked once). If you want the user to keep access to the view, set the
    DURATION property on your class to be the duration (in seconds) of this
    authorization.
    With the default values, all views protected by RecaptchaMixin share the
    same "lock": if DURATION is set, accessing one will give access to the other
    as long as the session token remains valid. To prevent this, either change
    the RECAPTCHA_KEY class attribute to something unique for each independant
    views or set the RECAPTCHA_INDEPENDENT class attribute to True.

    Also note that cache mechanisms can happen, and cause the page to remain
    accessible for a while. If this is not desirable, use the @never_cache
    decorator from Django.
    """
    DURATION = None
    SESSION_DATE_KEY = 'RECAPTCHA_%s'
    RECAPTCHA_KEY = 'session'
    RECAPTCHA_INDEPENDENT = False

    def _session_key(self):
        """Return the session key for this view's session lock."""
        if self.__class__.RECAPTCHA_INDEPENDENT:
            local_key = self.__class__.__name__
        else:
            local_key = self.__class__.RECAPTCHA_KEY
        return self.__class__.SESSION_DATE_KEY % local_key

    def _check_session(self, request):
        """Check if the session contains access data.

        Parameters
        ----------
        request : Request
            The Django request


        Returns
        -------
        bool
            True if the session indicate that the user is allowed to see the
            view, False otherwise.


        Notes
        -----
        This method will check for the DURATION class attribute, and always
        return False if it is not set (or null).
        """
        if not self.__class__.DURATION:
            return False
        duration = self.__class__.DURATION
        key = self._session_key()
        checkup_date = request.session.get(key, None)
        if checkup_date is None:
            return False
        now = datetime.now().timestamp()
        expire = checkup_date + duration
        return expire >= now

    def _update_session(self, request):
        """Add the reCAPTCHA validation time into the session.

        Notes
        -----
        Only the timestamp is added (not the datetime object).
        """
        request.session[self._session_key()] = datetime.now().timestamp()

    def dispatch(self, request, *args, **kwargs):
        session_pass = self._check_session(request)
        if not session_pass:
            give_access = check(request)
            if give_access:
                self._update_session(request)
        else:
            give_access = True
        if not give_access:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
