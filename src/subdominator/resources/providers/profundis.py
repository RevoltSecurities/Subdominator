from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class ProfundisResource(BaseResource):
    name = "profundis"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": key,
            "Accept": "text/event-stream",
        }

        json_body = {"domain": target}

        try:
            raw_text = await self.client.request(
                "POST",
                "https://api.profundis.io/api/v2/common/data/subdomains",
                headers=headers,
                json_body=json_body,
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()

        for line in raw_text.splitlines():
            line = line.strip()
            if line:
                findings.add(line)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
