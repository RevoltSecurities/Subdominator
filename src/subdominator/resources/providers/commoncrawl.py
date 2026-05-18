from __future__ import annotations

import re
from datetime import datetime

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource

# Legacy: queries the 6 most recent annual indices (up to 1 per year for the
# past 6 years). The rewrite capped at 3 — restored to 6 to match legacy.
_MAX_INDICES = 6


class CommonCrawlResource(BaseResource):
    name = "commoncrawl"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            all_indices = await self.client.get_json(
                "https://index.commoncrawl.org/collinfo.json",
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        # Legacy selects up to 1 index per calendar year for the past 6 years,
        # deduplicated by year (most recent index per year wins).
        current_year = datetime.now().year
        target_years = {str(current_year - i) for i in range(6)}
        selected: list[str] = []
        seen_years: set[str] = set()

        for index in all_indices:
            name = index.get("name", "")
            for year in target_years:
                if year in name and year not in seen_years:
                    api_url = index.get("cdx-api")
                    if api_url:
                        selected.append(api_url)
                        seen_years.add(year)
            if len(selected) >= _MAX_INDICES:
                break

        findings: set[str] = set()
        pattern = re.compile(rf"([a-zA-Z0-9_.-]+\.{re.escape(target)})")

        for api_url in selected:
            try:
                text = await self.client.request(
                    "GET",
                    api_url,
                    params={"url": f"*.{target}"},
                    expected_status={200},
                )
            except RuntimeError:
                continue
            findings.update(match.lower() for match in pattern.findall(text))

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
