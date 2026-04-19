from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class BufferOverResource(BaseResource):
    name = "bufferover"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                "https://tls.bufferover.run/dns",
                headers={"x-api-key": key},
                params={"q": f".{target}"},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: list[str] = []
        for row in data.get("Results", []):
            parts = row.split(",")
            if len(parts) >= 5:
                findings.append(parts[4].strip())
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
