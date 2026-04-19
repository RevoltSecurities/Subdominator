from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class WhoisXmlResource(BaseResource):
    name = "whoisxml"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                "https://subdomains.whoisxmlapi.com/api/v1",
                params={"apiKey": key, "domainName": target},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [
            record.get("domain", "")
            for record in data.get("result", {}).get("records", [])
            if isinstance(record, dict)
        ]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
