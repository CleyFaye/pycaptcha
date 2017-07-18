"""reCAPTCHA server-side check configured with Django"""
from django.conf import settings
from pycaptcha import recaptcha_check
try:
    from ipware.ip import get_ip
except ImportError:
    # SO:4581997:2059163
    def get_ip(request):
        """Return the remote IP from a Django request.

        Returns
        -------
        string
            The client remote IP.


        Notes
        -----
        This is far from perfect, and will miss many cases of proxy, reverse
        proxy, VPN, etc. Only use it for non-critical checks.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


def check(request, response_key='response'):
    """Check the reCAPTCHA from a request.

    Parameters
    ----------
    request : Request
        The Django request
    response_key : string (optional)
        The key to look for to retrieve the user response token. Defaults to
        'response'


    Returns
    -------
    bool
        Returns True if the reCAPTCHA challenge was completed, or False if it
        failed or if there was no challenge to check.


    Notes
    -----
    Like the other Django facilities, this expect to find the reCAPTCHA shared
    secret in the RECPATCHA_SHARED_SECRET setting.
    """
    response = (request.POST.get(response_key, None)
                or request.GET.get(response_key, None))
    remote_ip = get_ip(request)
    return recaptcha_check(settings.RECAPTCHA_SHARED_SECRET,
                           response,
                           remote_ip)
