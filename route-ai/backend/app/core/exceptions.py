"""Custom exception hierarchy for RouteAI enterprise platform."""

from fastapi import HTTPException, status


class RouteAIException(HTTPException):
    """Base exception class for all custom RouteAI platform exceptions."""

    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: dict | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class EntityNotFoundException(RouteAIException):
    """Raised when a requested database entity or resource is not found (404 Not Found)."""

    def __init__(self, entity_name: str, entity_id: str | int) -> None:
        super().__init__(
            detail=f"{entity_name} with ID '{entity_id}' was not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class DuplicateRecordException(RouteAIException):
    """Raised when an active duplicate record already exists (409 Conflict)."""

    def __init__(self, detail: str) -> None:
        super().__init__(
            detail=detail,
            status_code=status.HTTP_409_CONFLICT,
        )


class AuthenticationFailedException(RouteAIException):
    """Raised when authentication fails or token is invalid/expired (401 Unauthorized)."""

    def __init__(self, detail: str = "Invalid authentication credentials or token expired.") -> None:
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )


class PermissionDeniedException(RouteAIException):
    """Raised when an authenticated user lacks required RBAC role permissions (403 Forbidden)."""

    def __init__(self, detail: str = "Permission denied. Required role authorization is missing.") -> None:
        super().__init__(
            detail=detail,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class IllegalStateTransitionException(RouteAIException):
    """Raised when a state machine transition is illegal according to business logic (400 Bad Request)."""

    def __init__(self, current_status: str, target_status: str, allowed_targets: set[str]) -> None:
        targets_str = ", ".join(sorted(allowed_targets)) if allowed_targets else "None (Terminal State)"
        super().__init__(
            detail=f"Illegal status transition from '{current_status}' to '{target_status}'. Allowed transitions: {targets_str}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class DatabaseException(RouteAIException):
    """Raised when an unhandled database exception occurs (500 Internal Server Error)."""

    def __init__(self, detail: str = "A database execution error occurred. Please contact system support.") -> None:
        super().__init__(
            detail=detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
