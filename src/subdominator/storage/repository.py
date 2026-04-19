from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import text

from subdominator.core.models import Finding


@dataclass(slots=True)
class StoredDomainSummary:
    root_domain: str
    findings_count: int
    last_discovered_at: datetime | None
    latest_run_id: int | None
    latest_run_at: datetime | None


@dataclass(slots=True)
class StoredRunSummary:
    run_id: int
    root_domain: str
    created_at: datetime
    findings_count: int


@dataclass(slots=True)
class StoredDomainStats:
    root_domain: str
    findings_count: int
    unique_resources: int
    latest_run_id: int | None
    latest_run_at: datetime | None
    first_discovered_at: datetime | None
    last_discovered_at: datetime | None


class EnumerationRepository:
    def __init__(self, database) -> None:
        self.database = database

    def get_saved_findings(self, root_domain: str) -> list[Finding]:
        return [
            Finding(
                domain=root_domain,
                subdomain=subdomain,
                resource="legacy-db",
                query_target=root_domain,
                recursion_depth=0,
                discovered_at=datetime.now(UTC),
            )
            for subdomain in self._load_subdomains(root_domain)
        ]

    def save_findings(self, root_domain: str, findings: list[Finding]) -> int | None:
        incoming = {finding.subdomain.strip().lower() for finding in findings if finding.subdomain.strip()}
        with self.database.session_factory() as session:
            row = session.execute(
                text("SELECT subdomains FROM subdomains WHERE domain = :domain"),
                {"domain": root_domain},
            ).first()
            existing = {
                item.strip().lower()
                for item in ((row[0] if row else "") or "").split(",")
                if item.strip()
            }
            merged = sorted(existing.union(incoming))
            if row:
                session.execute(
                    text("UPDATE subdomains SET subdomains = :subdomains WHERE domain = :domain"),
                    {"domain": root_domain, "subdomains": ",".join(merged)},
                )
            else:
                session.execute(
                    text("INSERT INTO subdomains(domain, subdomains) VALUES (:domain, :subdomains)"),
                    {"domain": root_domain, "subdomains": ",".join(merged)},
                )
            session.commit()
        return None

    def list_domains(self) -> list[StoredDomainSummary]:
        with self.database.session_factory() as session:
            rows = session.execute(
                text("SELECT domain, subdomains FROM subdomains ORDER BY domain")
            ).all()
        return [
            StoredDomainSummary(
                root_domain=row[0],
                findings_count=len([item for item in (row[1] or "").split(",") if item.strip()]),
                last_discovered_at=None,
                latest_run_id=None,
                latest_run_at=None,
            )
            for row in rows
        ]

    def get_domain_stats(self, root_domain: str) -> StoredDomainStats | None:
        findings = self.get_saved_findings(root_domain)
        if not findings:
            return None
        resources = {item.resource for item in findings}
        return StoredDomainStats(
            root_domain=root_domain,
            findings_count=len(findings),
            unique_resources=len(resources),
            latest_run_id=None,
            latest_run_at=None,
            first_discovered_at=None,
            last_discovered_at=None,
        )

    def list_runs(self, root_domain: str | None = None) -> list[StoredRunSummary]:
        return []

    def get_findings(self, root_domain: str) -> list[Finding]:
        return self.get_saved_findings(root_domain)

    def delete_domain(self, root_domain: str) -> int:
        findings_count = len(self.get_saved_findings(root_domain))
        if findings_count == 0:
            return 0
        with self.database.session_factory() as session:
            session.execute(
                text("DELETE FROM subdomains WHERE domain = :domain"),
                {"domain": root_domain},
            )
            session.commit()
        return findings_count

    def _load_subdomains(self, root_domain: str) -> list[str]:
        with self.database.session_factory() as session:
            row = session.execute(
                text("SELECT subdomains FROM subdomains WHERE domain = :domain"),
                {"domain": root_domain},
            ).first()
        return sorted(
            {
                item.strip().lower()
                for item in ((row[0] if row else "") or "").split(",")
                if item.strip()
            }
        )
