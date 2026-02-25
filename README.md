# yandex-direct-python

Python-клиент для API Yandex Direct v5.

## Что реализовано

- универсальный вызов любого метода: `client.call(service, method, params)`;
- динамические прокси для **всех v5 сервисов** (`client.ads.get(...)`, `client.campaigns.add(...)` и т.д.);
- реестр всех сервисов через `client.services()`;
- Reports API: `get_report(...)` + polling `get_report_ready(...)`;
- типизированные ошибки (`DirectApiError`, `DirectTransportError`) с `request_id`, `status_code`, `error_code`.

## Установка

```bash
pip install -e .
```

## Примеры

```python
from yandex_direct import DirectConfig, YandexDirectClient, ReportRequest

config = DirectConfig(access_token="<token>", client_login="my-login", locale="ru")
client = YandexDirectClient(config)

# Вызов через динамический сервис
campaigns = client.campaigns.get(
    SelectionCriteria={"Ids": [123]},
    FieldNames=["Id", "Name", "State"],
)

# Универсальный вызов
ads = client.call(
    service="ads",
    method="get",
    params={"SelectionCriteria": {"CampaignIds": [123]}, "FieldNames": ["Id", "Status"]},
)

# Reports
request = ReportRequest(
    report_definition={
        "ReportName": "demo",
        "ReportType": "CAMPAIGN_PERFORMANCE_REPORT",
        "DateRangeType": "LAST_7_DAYS",
        "FieldNames": ["CampaignId", "CampaignName", "Impressions", "Clicks", "Cost"],
        "Format": "TSV",
    }
)
report_tsv = client.get_report_ready(request)
```
