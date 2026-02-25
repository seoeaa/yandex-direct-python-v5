# yandex-direct-python

Python-клиент для API Яндекс Директ v5.

## Возможности

### Базовые
- Универсальный вызов любого метода: `client.call(service, method, params)`
- Динамические прокси для **всех v5 сервисов** (`client.ads.get(...)`, `client.campaigns.add(...)` и т.д.)
- Реестр всех сервисов через `client.services()`
- Reports API: `get_report(...)` + polling `get_report_ready(...)`
- Типизированные ошибки (`DirectApiError`, `DirectTransportError`) с `request_id`, `status_code`, `error_code`

### Для продакшена
- **Retry логика** с экспоненциальной задержкой при ошибках сети (HTTP 429, 500-504) и API (коды 50-70)
- **Логирование** - включите через `enable_logging()`
- **Валидация** - используйте `RequestValidator` для проверки параметров

### Типизация (для автодополнения в IDE)
- Типизированные классы запросов: `GetAdsRequest`, `AddAdsRequest`, `GetCampaignsRequest` и др.
- Критерии фильтрации: `AdsSelectionCriteria`, `CampaignsSelectionCriteria`, `AdGroupsSelectionCriteria`
- Константы полей: `AdFields`, `CampaignFields`, `AdGroupFields`, `KeywordFields`

## Установка

```bash
pip install -e .
```

## Быстрый старт

```python
from yandex_direct import DirectConfig, YandexDirectClient

config = DirectConfig(access_token="<token>", client_login="my-login", locale="ru")
client = YandexDirectClient(config)

# Вызов через динамический сервис
campaigns = client.campaigns.get(
    SelectionCriteria={"Ids": [123]},
    FieldNames=["Id", "Name", "State"],
)
```

## Примеры с типизацией

### Получение кампаний

```python
from yandex_direct import (
    YandexDirectClient,
    DirectConfig,
    GetCampaignsRequest,
    CampaignsSelectionCriteria,
    CampaignFields,
)

client = YandexDirectClient(DirectConfig(access_token="<token>", client_login="my-login"))

# С типизацией (с автодополнением)
criteria = CampaignsSelectionCriteria(ids=[123, 456])
request = GetCampaignsRequest(
    criteria=criteria,
    field_names=[CampaignFields.ID, CampaignFields.NAME, CampaignFields.STATUS]
)
result = client.campaigns.get(**request.to_dict())
```

### Получение объявлений

```python
from yandex_direct import (
    GetAdsRequest,
    AdsSelectionCriteria,
    AdFields,
)

criteria = AdsSelectionCriteria(campaign_ids=[123])
request = GetAdsRequest(criteria=criteria, field_names=[AdFields.ID, AdFields.STATUS])
result = client.ads.get(**request.to_dict())
```

### Добавление объявлений

```python
from yandex_direct import (
    AddAdsRequest,
    AdAddItem,
    TextAdAdd,
)

ad = AdAddItem(
    ad_group_id=123,
    text_ad=TextAdAdd(
        title="Купить widget",
        title2="Скидка 50%",
        text="Лучший widget в городе",
        href="https://example.com"
    )
)
result = client.ads.add(AddAdsRequest(ads=[ad]).to_dict())
```

### Отчеты

```python
from yandex_direct import ReportRequest

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

## Retry и логирование

```python
from yandex_direct import YandexDirectClient, DirectConfig, enable_logging, set_log_level
import logging

# Включить логирование
enable_logging(requests=True, responses=True)
set_log_level(logging.DEBUG)

# Настроить retry
client = YandexDirectClient(
    DirectConfig(access_token="<token>", client_login="my-login"),
    retry_max_attempts=3,
    retry_base_delay=2.0,
    retry_enabled=True,
)
```

## Валидация

```python
from yandex_direct import RequestValidator, ValidationError

try:
    criteria = RequestValidator.validate_get_ads(campaign_ids=[123, 456])
except ValidationError as e:
    print(f"Ошибка валидации: {e}")
```

## Доступные сервисы V5

| Сервис | Описание |
|--------|----------|
| `adextensions` | Расширения объявлений |
| `adgroups` | Группы объявлений |
| `adimages` | Изображения |
| `ads` | Объявления |
| `agencyclients` | Клиенты агентства |
| `audiencetargets` | Аудиторные цели |
| `bidmodifiers` | Корректировки ставок |
| `bids` | Ставки |
| `businesses` | Бизнесы |
| `campaigns` | Кампании |
| `changes` | Изменения |
| `clients` | Клиенты |
| `dictionaries` | Справочники |
| `dynamictextadtargets` | Динамические цели |
| `feeds` | Фиды |
| `keywordbids` | Ставки ключевых слов |
| `keywords` | Ключевые слова |
| `keywordsresearch` | Исследование ключевых слов |
| `leads` | Лиды |
| `negativekeywordsharedsets` | Общие минус-слова |
| `retargetinglists` | Ретаргетинг |
| `sitelinks` | Быстрые ссылки |
| `smartadtargets` | Цели умных кампаний |
| `strategies` | Стратегии |
| `turbopages` | Турбо-страницы |
| `vcards` | Визитки |

## Лицензия

MIT
