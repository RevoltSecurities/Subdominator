from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class Finding:
    domain: str
    subdomain: str
    resource: str
    query_target: str
    recursion_depth: int
    discovered_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(slots=True)
class ResourceResult:
    resource: str
    target: str
    recursion_depth: int
    findings: list[str]
    error: str | None = None
    duration_ms: int = 0


@dataclass(slots=True)
class ResourceExecution:
    resource: str
    target: str
    recursion_depth: int
    findings_count: int
    duration_ms: int
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.error is None


@dataclass(slots=True)
class EnumerationSummary:
    root_domain: str
    recursive_depth: int
    started_at: datetime
    completed_at: datetime
    targets_scanned: list[str]
    findings: list[Finding]
    resource_executions: list[ResourceExecution]
    fresh_findings_count: int = 0
    historical_findings_count: int = 0
    new_findings_count: int = 0
    reused_historical_findings_count: int = 0

    @property
    def duration_ms(self) -> int:
        return int((self.completed_at - self.started_at).total_seconds() * 1000)

    @property
    def total_unique_findings(self) -> int:
        return len(self.findings)

    @property
    def total_resource_executions(self) -> int:
        return len(self.resource_executions)

    @property
    def failed_resource_executions(self) -> int:
        return sum(1 for execution in self.resource_executions if not execution.success)

    @property
    def successful_resource_executions(self) -> int:
        return sum(1 for execution in self.resource_executions if execution.success)
