from dataclasses import dataclass, field


@dataclass
class ReportRequest:
    """Typed wrapper for reports endpoint request payload."""

    report_definition: dict
    return_money_in_micros: bool = False
    skip_report_header: bool = True
    skip_column_header: bool = False
    skip_report_summary: bool = True
    include_vat: bool | None = None
    include_discount: bool | None = None
    processing_mode: str | None = None
    extra_headers: dict[str, str] = field(default_factory=dict)

    def headers(self) -> dict[str, str]:
        headers = {
            "returnMoneyInMicros": str(self.return_money_in_micros).lower(),
            "skipReportHeader": str(self.skip_report_header).lower(),
            "skipColumnHeader": str(self.skip_column_header).lower(),
            "skipReportSummary": str(self.skip_report_summary).lower(),
        }
        if self.include_vat is not None:
            headers["IncludeVAT"] = "YES" if self.include_vat else "NO"
        if self.include_discount is not None:
            headers["IncludeDiscount"] = "YES" if self.include_discount else "NO"
        if self.processing_mode is not None:
            headers["processingMode"] = self.processing_mode
        headers.update(self.extra_headers)
        return headers

    def payload(self) -> dict:
        return {"params": self.report_definition}
