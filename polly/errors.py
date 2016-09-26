class Error(Exception):
    """General error with message"""
    def __init__(self, message):
        self.message = message


class NotFoundError(Error):
    """Exception raised for inexistent objects"""
    def __init__(self, message):
        super().__init__(message)


class EmptyError(Error):
    """Exception raised for invalid empty values"""
    def __init__(self, message):
        super().__init__(message)


class InvalidValueError(Error):
    """Exception raised for invalid values"""
    def __init__(self, message):
        super().__init__(message)
