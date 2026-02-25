from __future__ import annotations

from unittest.mock import Mock

import pytest

from yandex_direct import DirectApiError, DirectConfig, DirectTransportError, ReportRequest, V5_SERVICES, YandexDirectClient


@pytest.fixture
def client() -> YandexDirectClient:
    return YandexDirectClient(DirectConfig(access_token="t", client_login="l"), report_poll_interval_s=0)


def _response(status_code: int, text: str, headers: dict | None = None):
    response = Mock()
    response.status_code = status_code
    response.text = text
    response.headers = headers or {}
    if text and text[:1] in "[{":
        response.json.return_value = __import__("json").loads(text)
    else:
        response.json.return_value = {}
    return response


def test_service_proxy_dynamic_method(client: YandexDirectClient) -> None:
    client.transport.post_json = Mock(return_value=_response(200, '{"result": {"ok": true}}'))

    result = client.campaigns.get(FieldNames=["Id"], SelectionCriteria={})

    assert result == {"ok": True}
    assert client.transport.post_json.call_count == 1


def test_services_registry_contains_all_v5_services(client: YandexDirectClient) -> None:
    services = client.services()
    assert set(services.keys()) == set(V5_SERVICES)


def test_attribute_error_for_unknown_service(client: YandexDirectClient) -> None:
    with pytest.raises(AttributeError):
        _ = client.unknown_service


def test_api_error_payload_raises(client: YandexDirectClient) -> None:
    client.transport.post_json = Mock(return_value=_response(200, '{"error": {"error_code": 10, "error_string": "bad request"}}'))

    with pytest.raises(DirectApiError) as exc_info:
        client.call("ads", "get", {})

    assert exc_info.value.error_code == 10


def test_http_error_raises(client: YandexDirectClient) -> None:
    client.transport.post_json = Mock(return_value=_response(500, "oops", {"RequestId": "r1"}))

    with pytest.raises(DirectApiError) as exc_info:
        client.call("ads", "get", {})

    assert exc_info.value.status_code == 500
    assert exc_info.value.request_id == "r1"


def test_transport_error_bubbles(client: YandexDirectClient) -> None:
    client.transport.post_json = Mock(side_effect=DirectTransportError("boom"))

    with pytest.raises(DirectTransportError):
        client.call("ads", "get", {})


def test_report_ready_success_after_retry(client: YandexDirectClient) -> None:
    request = ReportRequest(report_definition={"ReportName": "r"})
    client.transport.post_json = Mock(
        side_effect=[
            _response(201, "", {"RequestId": "r1", "retryIn": "1"}),
            _response(200, "tsv-body", {"RequestId": "r2"}),
        ]
    )

    result = client.get_report_ready(request, attempts=2)

    assert result == "tsv-body"


def test_report_ready_timeout(client: YandexDirectClient) -> None:
    request = ReportRequest(report_definition={"ReportName": "r"})
    client.transport.post_json = Mock(return_value=_response(201, "", {"RequestId": "r1", "retryIn": "1"}))

    with pytest.raises(DirectApiError) as exc_info:
        client.get_report_ready(request, attempts=2)

    assert "not ready" in str(exc_info.value)
