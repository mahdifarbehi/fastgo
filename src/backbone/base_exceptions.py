from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found"
        )


class DuplicateException(HTTPException):
    def __init__(self, detail="Object already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class IntegrityException(HTTPException):
    def __init__(self, detail="Integrity error"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ValueErrorException(HTTPException):
    def __init__(self, detail="Invalid value"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail="Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail="Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class FailedUploadException(HTTPException):
    def __init__(self, detail="Failed to upload file"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail="Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
