from __future__ import annotations

import re
import urllib.parse
from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class SubMdResource(BaseResource):
    name = "submd"
    has_optional_config = True
    requires_config = False  # OptionalKey handling

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        headers = {}
        
        # Optional Key injection upgrading native query to Bearer auth
        if self.provider_config:
            keys = self.provider_config.get_values(self.name)
            if keys and isinstance(keys, list):
                headers["Authorization"] = f"Bearer {keys[0]}"
                
        endpoint = f"https://api.sub.md/v1/search?apex={urllib.parse.quote(target)}"

        try:
            raw_text = await self.client.request(
                "GET",
                endpoint,
                headers=headers if headers else None,
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()

        # Engine extractor pattern matching global generic Regex session Extractor natively
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
