"""Type definitions for Yandex Direct API v5 requests and responses.

This module provides type hints and dataclasses for all major API methods,
enabling autocomplete and type checking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ============================================================================
# Selection Criteria - Filter classes for API requests
# ============================================================================


@dataclass
class AdsSelectionCriteria:
    """Criteria for filtering ads in ads.get method."""

    ids: list[int] | None = None
    campaign_ids: list[int] | None = None
    ad_group_ids: list[int] | None = None
    states: list[str] | None = None
    statuses: list[str] | None = None

    def to_dict(self) -> dict[str, list[int]]:
        result: dict[str, list[int]] = {}
        if self.ids:
            result["Ids"] = self.ids
        if self.campaign_ids:
            result["CampaignIds"] = self.campaign_ids
        if self.ad_group_ids:
            result["AdGroupIds"] = self.ad_group_ids
        if self.states:
            result["States"] = self.states
        if self.statuses:
            result["Statuses"] = self.statuses
        return result


@dataclass
class CampaignsSelectionCriteria:
    """Criteria for filtering campaigns in campaigns.get method."""

    ids: list[int] | None = None
    states: list[str] | None = None
    statuses: list[str] | None = None

    def to_dict(self) -> dict[str, list[int] | list[str]]:
        result: dict[str, list[int] | list[str]] = {}
        if self.ids:
            result["Ids"] = self.ids
        if self.states:
            result["States"] = self.states
        if self.statuses:
            result["Statuses"] = self.statuses
        return result


@dataclass
class AdGroupsSelectionCriteria:
    """Criteria for filtering ad groups in adgroups.get method."""

    ids: list[int] | None = None
    campaign_ids: list[int] | None = None
    types: list[str] | None = None
    states: list[str] | None = None
    statuses: list[str] | None = None

    def to_dict(self) -> dict[str, list[int] | list[str]]:
        result: dict[str, list[int] | list[str]] = {}
        if self.ids:
            result["Ids"] = self.ids
        if self.campaign_ids:
            result["CampaignIds"] = self.campaign_ids
        if self.types:
            result["Types"] = self.types
        if self.states:
            result["States"] = self.states
        if self.statuses:
            result["Statuses"] = self.statuses
        return result


@dataclass
class KeywordsSelectionCriteria:
    """Criteria for filtering keywords in keywords.get method."""

    ids: list[int] | None = None
    ad_group_ids: list[int] | None = None
    campaign_ids: list[int] | None = None
    states: list[str] | None = None
    statuses: list[str] | None = None

    def to_dict(self) -> dict[str, list[int] | list[str]]:
        result: dict[str, list[int] | list[str]] = {}
        if self.ids:
            result["Ids"] = self.ids
        if self.ad_group_ids:
            result["AdGroupIds"] = self.ad_group_ids
        if self.campaign_ids:
            result["CampaignIds"] = self.campaign_ids
        if self.states:
            result["States"] = self.states
        if self.statuses:
            result["Statuses"] = self.statuses
        return result


# ============================================================================
# Field Enums - Common field names for each method
# ============================================================================


class AdFields:
    """Field names for ads.get method."""

    ID = "Id"
    AD_GROUP_ID = "AdGroupId"
    CAMPAIGN_ID = "CampaignId"
    STATUS = "Status"
    STATE = "State"
    TYPE = "Type"
    AGE_LABEL = "AgeLabel"
    AD_CATEGORIES = "AdCategories"
    SHORT_TITLE = "ShortTitle"
    TITLE = "Title"
    TITLE2 = "Title2"
    TEXT = "Text"
    HREF = "Href"
    DISPLAY_DOMAIN = "DisplayDomain"
    VISUAL_VIEW_PROBABILITY = "VisualViewProbability"


class CampaignFields:
    """Field names for campaigns.get method."""

    ID = "Id"
    NAME = "Name"
    STATUS = "Status"
    STATE = "State"
    TYPE = "Type"
    START_DATE = "StartDate"
    END_DATE = "EndDate"
    DAILY_BUDGET = "DailyBudget"
    PAYMENT_TYPE = "PaymentType"
    NOTIFICATIONS = "Notifications"
    TIME_TARGETING = "TimeTargeting"


class AdGroupFields:
    """Field names for adgroups.get method."""

    ID = "Id"
    CAMPAIGN_ID = "CampaignId"
    NAME = "Name"
    STATUS = "Status"
    STATE = "State"
    TYPE = "Type"


class KeywordFields:
    """Field names for keywords.get method."""

    ID = "Id"
    AD_GROUP_ID = "AdGroupId"
    CAMPAIGN_ID = "CampaignId"
    KEYWORD = "Keyword"
    STATUS = "Status"
    STATE = "State"
    BID = "Bid"
    CONTEXT_BID = "ContextBid"


# ============================================================================
# Request Builders - Easy way to construct API requests
# ============================================================================


class GetAdsRequest:
    """Builder for ads.get requests."""

    def __init__(
        self,
        criteria: AdsSelectionCriteria,
        field_names: list[str] | None = None,
        page: dict | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ):
        self.criteria = criteria
        self.field_names = field_names or [AdFields.ID, AdFields.STATUS, AdFields.STATE]
        self.page = page
        self.limit = limit
        self.offset = offset

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "SelectionCriteria": self.criteria.to_dict(),
            "FieldNames": self.field_names,
        }
        if self.page:
            result["Page"] = self.page
        if self.limit:
            result["Page"] = {"Limit": self.limit, "Offset": self.offset or 0}
        if self.offset and not self.limit:
            result["Page"] = {"Offset": self.offset}
        return result


class GetCampaignsRequest:
    """Builder for campaigns.get requests."""

    def __init__(
        self,
        criteria: CampaignsSelectionCriteria,
        field_names: list[str] | None = None,
        page: dict | None = None,
    ):
        self.criteria = criteria
        self.field_names = field_names or [CampaignFields.ID, CampaignFields.NAME, CampaignFields.STATUS]
        self.page = page

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "SelectionCriteria": self.criteria.to_dict(),
            "FieldNames": self.field_names,
        }
        if self.page:
            result["Page"] = self.page
        return result


class GetAdGroupsRequest:
    """Builder for adgroups.get requests."""

    def __init__(
        self,
        criteria: AdGroupsSelectionCriteria,
        field_names: list[str] | None = None,
        page: dict | None = None,
    ):
        self.criteria = criteria
        self.field_names = field_names or [AdGroupFields.ID, AdGroupFields.CAMPAIGN_ID, AdGroupFields.NAME]
        self.page = page

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "SelectionCriteria": self.criteria.to_dict(),
            "FieldNames": self.field_names,
        }
        if self.page:
            result["Page"] = self.page
        return result


class GetKeywordsRequest:
    """Builder for keywords.get requests."""

    def __init__(
        self,
        criteria: KeywordsSelectionCriteria,
        field_names: list[str] | None = None,
        page: dict | None = None,
    ):
        self.criteria = criteria
        self.field_names = field_names or [KeywordFields.ID, KeywordFields.KEYWORD, KeywordFields.BID]
        self.page = page

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "SelectionCriteria": self.criteria.to_dict(),
            "FieldNames": self.field_names,
        }
        if self.page:
            result["Page"] = self.page
        return result


# ============================================================================
# Add Requests creating - For new entities
# ============================================================================


@dataclass
class TextAdAdd:
    """Text ad for adding."""

    text: str
    title: str
    title2: str | None = None
    href: str | None = None
    display_domain: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"Text": self.text, "Title": self.title}
        if self.title2:
            result["Title2"] = self.title2
        if self.href:
            result["Href"] = self.href
        if self.display_domain:
            result["DisplayDomain"] = self.display_domain
        return result


@dataclass
class AdAddItem:
    """Single ad to add."""

    ad_group_id: int
    text_ad: TextAdAdd

    def to_dict(self) -> dict[str, Any]:
        return {"AdGroupId": self.ad_group_id, "TextAd": self.text_ad.to_dict()}


class AddAdsRequest:
    """Builder for ads.add requests."""

    def __init__(self, ads: list[AdAddItem]):
        self.ads = ads

    def to_dict(self) -> dict[str, Any]:
        return {"Ads": [ad.to_dict() for ad in self.ads]}


@dataclass
class CampaignAddItem:
    """Campaign to add."""

    name: str
    campaign_type: str = "TEXT"
    daily_budget: int | None = None
    start_date: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"Name": self.name, "Type": self.campaign_type}
        if self.daily_budget:
            result["DailyBudget"] = {"Amount": self.daily_budget}
        if self.start_date:
            result["StartDate"] = self.start_date
        return result


class AddCampaignsRequest:
    """Builder for campaigns.add requests."""

    def __init__(self, campaigns: list[CampaignAddItem]):
        self.campaigns = campaigns

    def to_dict(self) -> dict[str, Any]:
        return {"Campaigns": [c.to_dict() for c in self.campaigns]}


# ============================================================================
# Update Requests - For updating entities
# ============================================================================


@dataclass
class AdUpdateItem:
    """Ad to update."""

    id: int
    text_ad: TextAdAdd | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"Id": self.id}
        if self.text_ad:
            result["TextAd"] = self.text_ad.to_dict()
        return result


class UpdateAdsRequest:
    """Builder for ads.update requests."""

    def __init__(self, ads: list[AdUpdateItem]):
        self.ads = ads

    def to_dict(self) -> dict[str, Any]:
        return {"Ads": [ad.to_dict() for ad in self.ads]}


# ============================================================================
# V4 API Support
# ============================================================================


# V4 API endpoint (different from V5)
V4_API_URL = "https://api.direct.yandex.com/v4/json"


@dataclass
class V4Request:
    """V4 API request wrapper."""

    method: str
    token: str
    locale: str = "ru"

    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept-Language": self.locale,
        }
