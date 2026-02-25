from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, TypeVar

from .config import DirectConfig
from .exceptions import DirectApiError, DirectError, DirectTransportError
from .reports import ReportRequest
from .transport import HttpTransport

V5_SERVICES: tuple[str, ...] = (
    "adextensions",
    "adgroups",
    "adimages",
    "ads",
    "agencyclients",
    "audiencetargets",
    "bidmodifiers",
    "bids",
    "businesses",
    "campaigns",
    "changes",
    "clients",
    "dictionaries",
    "dynamictextadtargets",
    "feeds",
    "keywordbids",
    "keywords",
    "keywordsresearch",
    "leads",
    "negativekeywordsharedsets",
    "retargetinglists",
    "sitelinks",
    "smartadtargets",
    "strategies",
    "turbopages",
    "vcards",
)

# Error codes that should trigger a retry
RETRYABLE_ERROR_CODES = {50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70}
RETRYABLE_HTTP_CODES = {429, 500, 502, 503, 504}

T = TypeVar("T")


def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exponential_base: float = 2.0,
    retry_on_error_codes: set[int] | None = None,
    retry_on_http_codes: set[int] | None = None,
):
    """Decorator that adds retry logic with exponential backoff."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            error_codes = retry_on_error_codes or RETRYABLE_ERROR_CODES
            http_codes = retry_on_http_codes or RETRYABLE_HTTP_CODES
            last_exception: Exception | None = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except DirectApiError as exc:
                    last_exception = exc
                    # Check if error is retryable
                    if exc.error_code and exc.error_code in error_codes:
                        if attempt < max_attempts - 1:
                            delay = min(base_delay * (exponential_base ** attempt), max_delay)
                            _logger.warning(
                                f"Retryable API error {exc.error_code}, "
                                f"attempt {attempt + 1}/{max_attempts}, "
                                f"waiting {delay:.1f}s"
                            )
                            time.sleep(delay)
                            continue
                    raise
                except DirectTransportError as exc:
                    last_exception = exc
                    if attempt < max_attempts - 1:
                        delay = min(base_delay * (exponential_base ** attempt), max_delay)
                        _logger.warning(
                            f"Transport error, attempt {attempt + 1}/{max_attempts}, "
                            f"waiting {delay:.1f}s: {exc}"
                        )
                        time.sleep(delay)
                        continue
                    raise

            raise last_exception  # type: ignore

        return wrapper  # type: ignore
    return decorator


def _setup_logger(name: str) -> logging.Logger:
    """Setup a logger with consistent format."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


_logger = _setup_logger("yandex_direct")


@dataclass
class ServiceProxy:
    """Dynamic proxy for Yandex Direct API service."""

    client: "YandexDirectClient"
    service: str

    @with_retry(max_attempts=3, base_delay=1.0)
    def call(self, method: str, **params: dict) -> dict:
        """Call a method on the service with retry logic."""
        return self.client.call(service=self.service, method=method, params=params)

    def __getattr__(self, method_name: str):
        """Dynamic method resolution."""
        api_method = method_name.replace("_", "")

        def _caller(**params: dict) -> dict:
            return self.call(method=api_method, **params)

        return _caller


@dataclass
class YandexDirectClient:
    """Feature-complete transport-level client for Yandex Direct API v5."""

    config: DirectConfig
    timeout_s: int = 60
    verify_ssl: bool = True
    report_poll_interval_s: int = 5
    # Retry settings
    retry_enabled: bool = True
    retry_max_attempts: int = 3
    retry_base_delay: float = 1.0
    retry_max_delay: float = 30.0
    # Logging
    log_requests: bool = True
    log_responses: bool = True
    # Custom retry settings
    retry_on_error_codes: set[int] | None = field(default=None)
    retry_on_http_codes: set[int] | None = field(default=None)

    transport: HttpTransport = field(init=False)

    def __post_init__(self) -> None:
        self.transport = HttpTransport(timeout_s=self.timeout_s, verify_ssl=self.verify_ssl)

    @with_retry(max_attempts=3, base_delay=1.0)
    def call(self, service: str, method: str, params: dict | None = None) -> dict:
        """Make an API call with retry logic."""
        body = {"method": method, "params": params or {}}
        service_name = service.lower()
        url = f"{self.config.api_url}/{service_name}"

        if self.log_requests:
            _logger.debug(f"Request: {method} on {service} with params: {params}")

        try:
            response = self.transport.post_json(url=url, payload=body, headers=self.config.headers())
            result = self._parse_api_response(response.status_code, response.text, response.headers)

            if self.log_responses:
                _logger.debug(f"Response: {method} on {service} -> {result}")

            return result
        except DirectTransportError as exc:
            _logger.error(f"Transport error calling {service}.{method}: {exc}")
            raise

    def service(self, service_name: str) -> ServiceProxy:
        """Get a service proxy object."""
        return ServiceProxy(client=self, service=service_name)

    def services(self) -> dict[str, ServiceProxy]:
        """Get all available service proxies."""
        return {name: ServiceProxy(client=self, service=name) for name in V5_SERVICES}

    def __getattr__(self, service_name: str) -> ServiceProxy:
        """Dynamic service access."""
        normalized = service_name.lower()
        if normalized in V5_SERVICES:
            return self.service(normalized)
        raise AttributeError(service_name)

    def get_ads(self, selection_criteria: dict, field_names: list[str]) -> dict:
        """Get ads with retry logic."""
        return self.ads.get(SelectionCriteria=selection_criteria, FieldNames=field_names)

    def get_campaigns(self, selection_criteria: dict, field_names: list[str]) -> dict:
        """Get campaigns with retry logic."""
        return self.campaigns.get(SelectionCriteria=selection_criteria, FieldNames=field_names)

    def get_ad_groups(self, selection_criteria: dict, field_names: list[str]) -> dict:
        """Get ad groups with retry logic."""
        return self.adgroups.get(SelectionCriteria=selection_criteria, FieldNames=field_names)

    def get_report(self, request: ReportRequest) -> str:
        """Get a report, returns immediately or raises if not ready."""
        response = self.transport.post_json(
            url=self.config.reports_url,
            payload=request.payload(),
            headers={**self.config.headers(), **request.headers()},
        )

        if response.status_code == 201:
            raise DirectApiError(
                "Report is being generated",
                status_code=201,
                request_id=response.headers.get("RequestId"),
                details={"retry_in": response.headers.get("retryIn")},
            )
        if response.status_code >= 400:
            raise DirectApiError(
                f"Report request failed with status {response.status_code}",
                status_code=response.status_code,
                request_id=response.headers.get("RequestId"),
                details={"body": response.text},
            )

        return response.text

    def get_report_ready(self, request: ReportRequest, attempts: int = 12) -> str:
        """Poll for report until it's ready."""
        last_error: DirectApiError | None = None
        for attempt in range(attempts):
            try:
                if self.log_requests:
                    _logger.info(f"Fetching report (attempt {attempt + 1}/{attempts})")
                return self.get_report(request)
            except DirectApiError as exc:
                if exc.status_code != 201:
                    raise
                last_error = exc
                if self.log_requests:
                    _logger.info(f"Report not ready, waiting {self.report_poll_interval_s}s...")
                time.sleep(self.report_poll_interval_s)

        raise DirectApiError(
            f"Report was not ready after {attempts} attempts",
            status_code=201,
            details=last_error.details if last_error else {},
            request_id=last_error.request_id if last_error else None,
        )

    def _parse_api_response(self, status_code: int, text: str, headers: dict[str, str]) -> dict:
        """Parse API response and handle errors."""
        request_id = headers.get("RequestId")

        if status_code >= 400:
            raise DirectApiError(
                f"HTTP error {status_code}",
                status_code=status_code,
                request_id=request_id,
                details={"body": text},
            )

        data = {} if not text else __import__("json").loads(text)

        if "error" in data:
            error = data["error"]
            raise DirectApiError(
                error.get("error_string", "Yandex Direct API error"),
                error_code=error.get("error_code"),
                status_code=status_code,
                request_id=request_id,
                details=error,
            )

        return data.get("result", data)


def set_log_level(level: int) -> None:
    """Set the log level for the yandex_direct logger."""
    _logger.setLevel(level)


def enable_logging(requests: bool = True, responses: bool = True) -> None:
    """Enable or disable request/response logging."""
    global _logger
    _logger.setLevel(logging.DEBUG if (requests or responses) else logging.INFO)
