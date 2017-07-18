"""Perform a reCAPTCHA verification server-side"""
import requests
try:
    from dateutil.parser import parse as parse_date
except ImportError:
    from datetime import datetime

    def parse_date(datestr):
        """Parse a date from ISO format yyyy-MM-dd'T'HH:mm:ssZZ"""
        return datetime.strptime('%Y-%m-%dT%H:%M:%S%z')

DEFAULT_RECAPTCHA_CHECK_URL = 'https://www.google.com/recaptcha/api/siteverify'


def check_detailed(secret,
                   response,
                   remote_ip=None,
                   check_url=DEFAULT_RECAPTCHA_CHECK_URL):
    """Check if a given user token come from a successful reCAPTCHA challenge.

    Parameters
    ----------
    secret : string
        The shared secret between the site and reCAPTCHA
    response : string
        The token provided by the user after completion of the challenge
    remote_ip : string (optional)
        The IP address of the client
    check_url : string (optional)
        The URL to use to perform the check. Default to Google reCAPTCHA service


    Returns
    -------
    dict
        The status of the challenge. It contains at least the following
        properties:

        - success (bool)
        - timestamp (datetime): timestamp of the challenge
        - hostname (str): hostname where the reCAPTCHA was solved
        - error (list(str)): a list of errors (see reCAPTCHA API for details)
    """
    check_data = {
        'secret': secret,
        'response': response}
    if remote_ip:
        check_data['remoteip'] = remote_ip
    reply = requests.post(check_url, check_data).json()
    result = {
        'success': reply['success'],
        'timestamp': parse_date(reply['challenge_ts']),
        'hostname': reply['hostname'],
    }
    if 'error-codes' in reply:
        result['error'] = reply['error-codes']
    return result


def check(secret,
          response,
          remote_ip=None,
          check_url=DEFAULT_RECAPTCHA_CHECK_URL):
    """Check if a given user token come from a successful reCAPTCHA challenge.

    Parameters
    ----------
    secret : string
        The shared secret between the site and reCAPTCHA
    response : string
        The token provided by the user after completion of the challenge
    remote_ip : string (optional)
        The IP address of the client
    check_url : string (optional)
        The URL to use to perform the check. Default to Google reCAPTCHA service


    Returns
    -------
    bool
        The status of the challenge. True indicate success, False indicate
        failure.


    Notes
    -----
    This is a convenience function that calls check_detailed().
    """
    return check_detailed(secret,
                          response,
                          remote_ip,
                          check_url)['success']
