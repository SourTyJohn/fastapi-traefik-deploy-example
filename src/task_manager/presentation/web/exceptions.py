from fastapi import status


class ApiError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST


class AuthenticationError(ApiError):
    status_code = status.HTTP_401_UNAUTHORIZED
