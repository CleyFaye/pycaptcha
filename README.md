PyCAPTCHA
=========

This package provide support for server-side checking of reCAPTCHA's user tokens.
It is made to work with Django projects, but that's not a requirement.


As a standalone
---------------

The pycaptcha.check() function returns the status of the request.


With Django
-----------

There's no need to install a Django application in your project settings.

The pycaptcha.django.check() is a helper function that will look for the reCAPTCHA shared secret in Django settings (key: RECAPTCHA\_SHARED\_SECRET).

The pycaptcha.django.RecaptchaMixin is a View mixin that prevent access to a view except if a reCAPTCHA challenge is successful.

The pycaptcha.django.TastypieAuthorization is a class designed to work with tastypie, and prevent all access to a resource except for the requested authorization, if a reCAPTCHA challenge was successfully done.

For both the view mixin and the tastypie authorization class, the challenge values are looked into both the GET and the POST of the request under the following names: "response".
