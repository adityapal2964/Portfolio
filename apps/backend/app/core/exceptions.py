class NotFoundError(Exception):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message)


class InvalidStateError(Exception):
    def __init__(self, message: str = "Invalid state") -> None:
        super().__init__(message)
