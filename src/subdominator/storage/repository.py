from __future__ import annotations

from sqlalchemy import select

from subdominator.core.models import Finding
from subdominator.storage.models import EnumerationRun, FindingRecord


class EnumerationRepository:
    def __init__(self, database) -> None:
        self.database = database

    def save_findings(self, root_domain: str, findings: list[Finding]) -> int:
        with self.database.session_factory() as session:
            run = EnumerationRun(root_domain=root_domain)
            session.add(run)
            session.flush()

            for finding in findings:
                existing = session.scalar(
                    select(FindingRecord).where(
                        FindingRecord.root_domain == root_domain,
                        FindingRecord.subdomain == finding.subdomain,
                    )
                )
                if existing is None:
                    session.add(
                        FindingRecord(
                            run_id=run.id,
                            root_domain=root_domain,
                            subdomain=finding.subdomain,
                            resource=finding.resource,
                            query_target=finding.query_target,
                            recursion_depth=finding.recursion_depth,
                            discovered_at=finding.discovered_at,
                        )
                    )

            session.commit()
            return run.id
