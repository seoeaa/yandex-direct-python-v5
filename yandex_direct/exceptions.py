from __future__ import annotations


class DirectError(RuntimeError):
    """Base class for all Yandex Direct Python client errors."""


class DirectTransportError(DirectError):
    """Raised when HTTP transport failed before an API payload was parsed."""


class DirectApiError(DirectError):
    """Raised when Yandex Direct API reports an error."""

    def __init__(
        self,
        message: str,
        *,
        error_code: int | None = None,
        details: dict | None = None,
        request_id: str | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
        self.request_id = request_id
        self.status_code = status_code
