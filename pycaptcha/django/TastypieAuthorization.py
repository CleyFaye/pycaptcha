"""Django's tastypie authorization based on reCAPTCHA"""
from logging import getLogger
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from .recaptcha import check
logg = getLogger(__name__)


class TastypieAuthorization(Authorization):
    """Authorize some specific actions only if a reCAPTCHA challenge is provided
    in the request.

    Notes
    -----
    This class expect to find the user token in the 'response' field (from
    either GET or POST).
    It also assume that the shared secret is set correctly in the project
    configuration (in RECAPTCHA_SHARED_SECRET).
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
        if not check(request):
            logg.info('A robot tried to access a resource (reCAPTCHA fail): %s',
                      request.get_full_path())
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
