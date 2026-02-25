from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass

from .exceptions import DirectTransportError


@dataclass
class HttpResponse:
    status_code: int
    text: str
    headers: dict[str, str]

    def json(self) -> dict:
        return json.loads(self.text)


class HttpTransport:
    """Minimal HTTP JSON transport implemented on top of Python stdlib."""

    def __init__(self, timeout_s: int = 60, verify_ssl: bool = True) -> None:
        self.timeout_s = timeout_s
        self.verify_ssl = verify_ssl

    def post_json(self, url: str, payload: dict, headers: dict[str, str]) -> HttpResponse:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url=url, data=body, headers=headers, method="POST")

        context = None
        if not self.verify_ssl:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        try:
            with urllib.request.urlopen(request, timeout=self.timeout_s, context=context) as response:
                return HttpResponse(
                    status_code=response.getcode(),
                    text=response.read().decode("utf-8"),
                    headers=dict(response.headers.items()),
                )
        except urllib.error.HTTPError as exc:
            return HttpResponse(
                status_code=exc.code,
                text=exc.read().decode("utf-8") if exc.fp else "",
                headers=dict(exc.headers.items()) if exc.headers else {},
            )
        except Exception as exc:  # noqa: BLE001
            raise DirectTransportError(str(exc)) from exc
