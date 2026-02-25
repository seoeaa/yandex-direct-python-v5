"""Python client for Yandex Direct API."""

from .client import (
    V5_SERVICES,
    ServiceProxy,
    YandexDirectClient,
    enable_logging,
    set_log_level,
)
from .config import DirectConfig
from .exceptions import DirectApiError, DirectError, DirectTransportError
from .reports import ReportRequest
from .validators import (
    COMMON_AD_FIELDS,
    COMMON_ADGROUP_FIELDS,
    COMMON_CAMPAIGN_FIELDS,
    RequestValidator,
    ValidationError,
)
from .v4 import (
    # V4 API
    V4_API_URL,
    V4Request,
    # Selection Criteria
    AdsSelectionCriteria,
    AdGroupsSelectionCriteria,
    CampaignsSelectionCriteria,
    KeywordsSelectionCriteria,
    # Field Classes
    AdFields,
    AdGroupFields,
    CampaignFields,
    KeywordFields,
    # Request Builders
    AddAdsRequest,
    AddCampaignsRequest,
    GetAdsRequest,
    GetAdGroupsRequest,
    GetCampaignsRequest,
    GetKeywordsRequest,
    UpdateAdsRequest,
    AdAddItem,
    AdUpdateItem,
    CampaignAddItem,
    TextAdAdd,
)

__all__ = [
    # Client
    "DirectApiError",
    "DirectConfig",
    "DirectError",
    "DirectTransportError",
    "ReportRequest",
    "ServiceProxy",
    "V5_SERVICES",
    "YandexDirectClient",
    # Logging
    "enable_logging",
    "set_log_level",
    # Validators
    "RequestValidator",
    "ValidationError",
    "COMMON_AD_FIELDS",
    "COMMON_CAMPAIGN_FIELDS",
    "COMMON_ADGROUP_FIELDS",
    # V4 API
    "V4_API_URL",
    "V4Request",
    # Type Definitions
    "AdsSelectionCriteria",
    "AdGroupsSelectionCriteria",
    "CampaignsSelectionCriteria",
    "KeywordsSelectionCriteria",
    # Field Classes
    "AdFields",
    "AdGroupFields",
    "CampaignFields",
    "KeywordFields",
    # Request Builders
    "AddAdsRequest",
    "AddCampaignsRequest",
    "GetAdsRequest",
    "GetAdGroupsRequest",
    "GetCampaignsRequest",
    "GetKeywordsRequest",
    "UpdateAdsRequest",
    "AdAddItem",
    "AdUpdateItem",
    "CampaignAddItem",
    "TextAdAdd",
]
