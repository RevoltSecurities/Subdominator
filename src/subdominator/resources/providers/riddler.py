from __future__ import annotations

import re
from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class RiddlerResource(BaseResource):
    name = "riddler"
    requires_config = False

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            raw_text = await self.client.request(
                "GET",
                f"https://riddler.io/search?q=pld:{target}&view_type=data_table",
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()

        # Engine extractor pattern recreating subscraping Extractor regex matches
        pattern = re.compile(rf'[a-zA-Z0-9\*_.-]+\.{re.escape(target)}', re.IGNORECASE)

        for line in raw_text.splitlines():
            line = line.strip()
            if not line:
                continue

            for match in pattern.finditer(line):
                val = match.group(0).lower()
                val = val.strip('"\'>/<')
                findings.add(val)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
