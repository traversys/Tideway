from dataclasses import dataclass, field


@dataclass
class ReportResult:
    """Tabular report output."""

    name: str
    headers: list = field(default_factory=list)
    rows: list = field(default_factory=list)
    raw: object = None
    files: list = field(default_factory=list)


@dataclass
class TextResult:
    """Plain text report output."""

    name: str
    text: str = ""
    files: list = field(default_factory=list)


@dataclass
class BatchReportResult:
    """Collection of report outputs."""

    results: list = field(default_factory=list)
    files: list = field(default_factory=list)
