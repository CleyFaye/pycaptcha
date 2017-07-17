"""Django's tastypie authorization based on reCAPTCHA"""
from logging import getLogger
from django.conf import settings
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from pycaptcha import recaptcha_check


logg = getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class TastypieAuthorization(Authorization):
    """Authorize some specific actions only if a reCAPTCHA challenge is provided
    in the request.

    Notes
    -----
    This class expect to find the user token in the 'response' field (from
    either GET or POST).
    It also assume that API key and shared secret are set correctly in the
    project configuration (respectively in RECAPTCHA_API_KEY and
    RECAPTCHA_SHARED_SECRET). It actually only use the secret at this point.
    """
    def check_permissions(self, request):
        """Check if the reCAPTCHA was successful.

        Parameters
        ----------
        request : Request
            The request object, containing the POST and GET data


        Notes
        -----
        This function raise an exception if something's wrong with the reCAPTCHA
        and return normally if everything's right.
        """
        response = (request.POST.get('response', None)
                    or request.GET.get('response', None))
        if not response:
            logg.debug('response field not set')
            raise Unauthorized
        secret = settings.RECAPTCHA_SHARED_SECRET
        remote_ip = get_client_ip(request)
        success = recaptcha_check(secret,
                                  response,
                                  remote_ip)
        if not success:
            raise Unauthorized

    def read_list(self, object_list, bundle):
        self.check_permissions(bundle.request)
        return object_list

    def read_detail(self, object_list, bundle):
        self.check_permissions(bundle.request)
        return True

    def create_list(self, object_list, bundle):
        self.check_permissions(bundle.request)
        return object_list

    def create_detail(self, object_list, bundle):
        self.check_permissions(bundle.request)
        return True

    def update_list(self, object_list, bundle):
        self.check_permissions(bundle.request)
        return object_list

    def update_detail(self, object_list, bundle):
        self.check_permissions(bundle.request)
        return True

    def delete_list(self, object_list, bundle):
        self.check_permissions(bundle.request)
        return object_list

    def delete_detail(self, object_list, bundle):
        self.check_permissions(bundle.request)
        return True
