from __future__ import annotations

import re

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class SiteDossierResource(BaseResource):
    name = "sitedossier"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        # Legacy used http:// — switched to https:// to avoid plain-text scraping.
        # Pagination: page increments by 100 (legacy: page += 100), stops when
        # "Show next 100 items" disappears from the response.
        findings: set[str] = set()
        page = 1
        pattern = re.compile(rf"(?i)(?:https?://)?([a-zA-Z0-9*_.-]+\.{re.escape(target)})")

        while True:
            try:
                text = await self.client.request(
                    "GET",
                    f"https://www.sitedossier.com/parentdomain/{target}/{page}",
                    expected_status={200},
                )
            except RuntimeError:
                break

            findings.update(match.lower() for match in pattern.findall(text))

            if "Show next 100 items" not in text:
                break

            page += 100

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
