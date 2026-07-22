from fastapi import HTTPException, status

class RouteAIException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class EntityNotFoundException(RouteAIException):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(detail=f"{entity_name} with id '{entity_id}' not found.", status_code=status.HTTP_404_NOT_FOUND)

class AuthenticationFailedException(RouteAIException):
    def __init__(self, detail: str = "Invalid authentication credentials."):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)
