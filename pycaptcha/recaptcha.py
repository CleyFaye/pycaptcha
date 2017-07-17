"""Perform a reCAPTCHA verification server-side"""
import requests

DEFAULT_RECAPTCHA_CHECK_URL = 'https://www.google.com/recaptcha/api/siteverify'

response_info = {}


def check(secret, response, remote_ip=None, custom_check_url=None):
    """Check if a given user token come from a successful reCAPTCHA challenge.

    Parameters
    ----------
    secret : string
        The shared secret between the site and reCAPTCHA
    response : string
        The token provided by the user after completion of the challenge
    remote_ip : string (optional)
        The IP address of the client
    custom_check_url : string (optional)
        The URL to use to perform the check. Default to Google reCAPTCHA service


    Returns
    -------
    boolean, details
        The status of the challenge. True indicate success, False indicate
        failure.
    """
    check_url = custom_check_url or DEFAULT_RECAPTCHA_CHECK_URL
    check_data = {
        'secret': secret,
        'response': response}
    if remote_ip:
        check_data['remoteip'] = remote_ip
    reply = requests.post(check_url, check_data).json()
    global response_info
    response_info[response] = reply
    return reply['success']


def get_details(response):
    """Return the details of a response check.

    Parameters
    ----------
    response : string
        The response code from the user.


    Returns
    -------
    dict
        A JSON object with the following fields:

        - success
        - challenge_ts
        - hostname
        - error-codes

        Check with the reCAPTCHA API for more details.


    Notes
    -----
    This function can only be called after check().
    Calling this function will remove the entry from the internal cache, so it
    can't be called again with the same response without calling check() again.

    This is not thread safe, and there are possible race conditions if multiple
    threads calls check() and get_details().
    """
    global response_info
    result = response_info[response]
    del response_info[response]
    return result
