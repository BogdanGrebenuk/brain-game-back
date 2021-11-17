class AppException(Exception):
    """Base class for application exceptions"""

    def __init__(self, message='', payload=None):
        if payload is None:
            payload = {}
            super().__init__(message)
        self.message = message
        self.payload = payload


class DomainException(AppException):
    """Base exception for domain-related exceptions"""
