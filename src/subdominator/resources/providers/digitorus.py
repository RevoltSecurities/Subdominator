from __future__ import annotations

import re

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class DigitorusResource(BaseResource):
    name = "digitorus"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            text = await self.client.request(
                "GET",
                f"https://certificatedetails.com/{target}",
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        pattern = re.compile(rf"(?i)(?:https?://)?([a-zA-Z0-9*_.-]+\.{re.escape(target)})")
        findings = pattern.findall(text)
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
