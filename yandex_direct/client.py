from __future__ import annotations

import time
from dataclasses import dataclass, field

from .config import DirectConfig
from .exceptions import DirectApiError
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


@dataclass
class ServiceProxy:
    client: "YandexDirectClient"
    service: str

    def call(self, method: str, **params: dict) -> dict:
        return self.client.call(service=self.service, method=method, params=params)

    def __getattr__(self, method_name: str):
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
    transport: HttpTransport = field(init=False)

    def __post_init__(self) -> None:
        self.transport = HttpTransport(timeout_s=self.timeout_s, verify_ssl=self.verify_ssl)

    def call(self, service: str, method: str, params: dict | None = None) -> dict:
        body = {"method": method, "params": params or {}}
        service_name = service.lower()
        url = f"{self.config.api_url}/{service_name}"
        response = self.transport.post_json(url=url, payload=body, headers=self.config.headers())
        return self._parse_api_response(response.status_code, response.text, response.headers)

    def service(self, service_name: str) -> ServiceProxy:
        return ServiceProxy(client=self, service=service_name)

    def services(self) -> dict[str, ServiceProxy]:
        return {name: ServiceProxy(client=self, service=name) for name in V5_SERVICES}

    def __getattr__(self, service_name: str) -> ServiceProxy:
        normalized = service_name.lower()
        if normalized in V5_SERVICES:
            return self.service(normalized)
        raise AttributeError(service_name)

    def get_ads(self, selection_criteria: dict, field_names: list[str]) -> dict:
        return self.ads.get(SelectionCriteria=selection_criteria, FieldNames=field_names)

    def get_report(self, request: ReportRequest) -> str:
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
        last_error: DirectApiError | None = None
        for _ in range(attempts):
            try:
                return self.get_report(request)
            except DirectApiError as exc:
                if exc.status_code != 201:
                    raise
                last_error = exc
                time.sleep(self.report_poll_interval_s)

        raise DirectApiError(
            f"Report was not ready after {attempts} attempts",
            status_code=201,
            details=last_error.details if last_error else {},
            request_id=last_error.request_id if last_error else None,
        )

    def _parse_api_response(self, status_code: int, text: str, headers: dict[str, str]) -> dict:
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
