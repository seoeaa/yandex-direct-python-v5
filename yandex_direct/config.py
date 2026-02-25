from dataclasses import dataclass


@dataclass(frozen=True)
class DirectConfig:
    """Connection settings for Yandex Direct API."""

    access_token: str
    client_login: str
    locale: str = "ru"
    api_url: str = "https://api.direct.yandex.com/json/v5"
    reports_url: str = "https://api.direct.yandex.com/json/v5/reports"

    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Login": self.client_login,
            "Accept-Language": self.locale,
            "Content-Type": "application/json; charset=utf-8",
        }
