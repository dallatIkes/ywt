class YWTException(Exception):
    """Base class for all YWT business exceptions."""

    pass


class NotFoundError(YWTException):
    def __init__(self, resource: str, identifier: str):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} '{identifier}' not found")


class ConflictError(YWTException):
    def __init__(self, message: str):
        super().__init__(message)


class ForbiddenError(YWTException):
    def __init__(self, message: str = "Action not allowed"):
        super().__init__(message)


class UnauthorizedError(YWTException):
    def __init__(self, message: str = "Not authenticated"):
        super().__init__(message)
