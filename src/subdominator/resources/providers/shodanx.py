from __future__ import annotations

import re

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class ShodanXResource(BaseResource):
    name = "shodanx"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        if self.registered_domain(target) != target:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            text = await self.client.request(
                "GET",
                f"https://www.shodan.io/domain/{target}",
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        match = re.search(r'<ul[^>]*id="subdomains"[^>]*>(.*?)</ul>', text, flags=re.DOTALL | re.IGNORECASE)
        if not match:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [f"{value.strip()}.{target}" for value in re.findall(r"<li[^>]*>([^<]+)</li>", match.group(1))]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
