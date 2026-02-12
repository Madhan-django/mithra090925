# exceptions.py
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call the default exception handler first
    response = exception_handler(exc, context)

    # Customize the error message for AuthenticationFailed
    if isinstance(exc, AuthenticationFailed):
        response.data = {'error': 'Authentication credentials are missing or invalid.'}

    return response
