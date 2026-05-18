from __future__ import annotations

import asyncio
import base64
from datetime import UTC, datetime, timedelta

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class HunterMapResource(BaseResource):
    name = "huntermap"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        query = base64.urlsafe_b64encode(target.encode("utf-8")).decode("ascii")
        end_time = datetime.now(UTC).strftime("%Y-%m-%d")
        # Legacy uses 27.8 * 12 ≈ 334 days as the look-back window.
        start_time = (datetime.now(UTC) - timedelta(days=334)).strftime("%Y-%m-%d")
        page = 1
        page_size = 100
        findings: set[str] = set()
        total: int | None = None

        while True:
            try:
                data = await self.client.get_json(
                    "https://api.hunter.how/search",
                    params={
                        "api-key": key,
                        "query": query,
                        "start_time": start_time,
                        "end_time": end_time,
                        "page": str(page),
                        "page_size": str(page_size),
                    },
                    expected_status={200},
                )
            except RuntimeError:
                break

            if not isinstance(data, dict):
                break

            payload = data.get("data") or {}
            items = payload.get("list") or []
            total = int(payload.get("total") or total or 0)

            for item in items:
                domain = item.get("domain", "")
                # Legacy: only add if domain ends with the target.
                if domain and domain.endswith(f".{target}"):
                    findings.add(domain)

            if not items or (total is not None and len(findings) >= total):
                break

            page += 1
            # Legacy used time.sleep(2.5) — replaced with asyncio.sleep to
            # avoid blocking the event loop while the semaphore is held.
            await asyncio.sleep(2.5)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
