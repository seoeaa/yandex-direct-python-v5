"""Validation utilities for Yandex Direct API parameters."""

from __future__ import annotations

from typing import Any


class ValidationError(ValueError):
    """Raised when validation fails."""

    pass


def validate_id(id_value: int, param_name: str = "Id") -> None:
    """Validate that ID is a positive integer."""
    if not isinstance(id_value, int) or id_value <= 0:
        raise ValidationError(f"{param_name} must be a positive integer, got: {id_value}")


def validate_ids(ids: list[int], param_name: str = "Ids") -> None:
    """Validate that IDs is a non-empty list of positive integers."""
    if not isinstance(ids, list):
        raise ValidationError(f"{param_name} must be a list, got: {type(ids).__name__}")
    if not ids:
        raise ValidationError(f"{param_name} cannot be empty")
    for i, id_val in enumerate(ids):
        if not isinstance(id_val, int) or id_val <= 0:
            raise ValidationError(f"{param_name}[{i}] must be a positive integer, got: {id_val}")


def validate_not_empty(value: Any, param_name: str) -> None:
    """Validate that value is not empty (not None, not empty string/list/dict)."""
    if value is None:
        raise ValidationError(f"{param_name} cannot be None")
    if isinstance(value, (str, list, dict)) and not value:
        raise ValidationError(f"{param_name} cannot be empty")


def validate_field_names(field_names: list[str], param_name: str = "FieldNames") -> None:
    """Validate that field names is a non-empty list of non-empty strings."""
    if not isinstance(field_names, list):
        raise ValidationError(f"{param_name} must be a list, got: {type(field_names).__name__}")
    if not field_names:
        raise ValidationError(f"{param_name} cannot be empty")
    for i, name in enumerate(field_names):
        if not isinstance(name, str) or not name:
            raise ValidationError(f"{param_name}[{i}] must be a non-empty string, got: {name}")


def validate_selection_criteria(criteria: dict, required_fields: list[str] | None = None) -> None:
    """Validate selection criteria dictionary."""
    if not isinstance(criteria, dict):
        raise ValidationError(f"SelectionCriteria must be a dict, got: {type(criteria).__name__}")
    if required_fields:
        for field in required_fields:
            if field not in criteria:
                raise ValidationError(f"SelectionCriteria must contain '{field}'")


class RequestValidator:
    """Validator for Yandex Direct API requests."""

    @staticmethod
    def validate_get_ads(campaign_ids: list[int] | None = None, ad_group_ids: list[int] | None = None, ids: list[int] | None = None) -> dict:
        """Validate and build selection criteria for ads.get."""
        criteria: dict[str, list[int]] = {}

        if campaign_ids is not None:
            validate_ids(campaign_ids, "CampaignIds")
            criteria["CampaignIds"] = campaign_ids

        if ad_group_ids is not None:
            validate_ids(ad_group_ids, "AdGroupIds")
            criteria["AdGroupIds"] = ad_group_ids

        if ids is not None:
            validate_ids(ids, "Ids")

        if not criteria:
            raise ValidationError("At least one of campaign_ids, ad_group_ids, or ids must be provided")

        return criteria

    @staticmethod
    def validate_get_campaigns(campaign_ids: list[int] | None = None, states: list[str] | None = None) -> dict:
        """Validate and build selection criteria for campaigns.get."""
        criteria: dict[str, list[int] | list[str]] = {}

        if campaign_ids is not None:
            validate_ids(campaign_ids, "CampaignIds")
            criteria["CampaignIds"] = campaign_ids

        if states is not None:
            if not isinstance(states, list):
                raise ValidationError("states must be a list")
            valid_states = {"ON", "OFF", "SUSPENDED", "ARCHIVED"}
            for state in states:
                if state not in valid_states:
                    raise ValidationError(f"Invalid state: {state}. Must be one of: {valid_states}")
            criteria["States"] = states

        return criteria

    @staticmethod
    def validate_get_ad_groups(campaign_ids: list[int] | None = None, ad_group_ids: list[int] | None = None) -> dict:
        """Validate and build selection criteria for adgroups.get."""
        criteria: dict[str, list[int]] = {}

        if campaign_ids is not None:
            validate_ids(campaign_ids, "CampaignIds")
            criteria["CampaignIds"] = campaign_ids

        if ad_group_ids is not None:
            validate_ids(ad_group_ids, "AdGroupIds")
            criteria["AdGroupIds"] = ad_group_ids

        if not criteria:
            raise ValidationError("At least one of campaign_ids or ad_group_ids must be provided")

        return criteria


# Common field names for API methods
COMMON_AD_FIELDS = [
    "Id",
    "AdGroupId",
    "CampaignId",
    "Status",
    "State",
    "Type",
    "AgeLabel",
    "AdCategories",
]

COMMON_CAMPAIGN_FIELDS = [
    "Id",
    "Name",
    "Status",
    "State",
    "Type",
    "StartDate",
    "EndDate",
    "DailyBudget",
    "PaymentType",
]

COMMON_ADGROUP_FIELDS = [
    "Id",
    "CampaignId",
    "Name",
    "Status",
    "State",
    "Type",
]
