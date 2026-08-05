"""Exceptions for the MunApp API."""


class MunAppError(Exception):
    """Base exception."""


class MunAppAuthenticationError(MunAppError):
    """Authentication failed."""


class MunAppApiError(MunAppError):
    """API request failed."""
