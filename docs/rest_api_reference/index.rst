REST API Reference
==================

All REST API endpoints are protected with basic authentication. The password for the "admin"
user can be set using two methods.

    ``pulp-manager reset-admin-password``

The above command prompts the user to enter a new password for "admin" user.

    ``pulp-manager reset-admin-password --random``

The above command generates a random password for "admin" user and prints it to the screen.

.. swaggerv2doc:: http://127.0.0.1:3000/docs/v3/schema/?format=openapi
