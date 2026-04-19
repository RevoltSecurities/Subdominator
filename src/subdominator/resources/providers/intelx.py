from __future__ import annotations

import asyncio

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class IntelXResource(BaseResource):
    name = "intelx"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        host, key = self.get_required_pair()
        if host is None or key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        # Step 1: kick off a phonebook search and get back a search ID.
        try:
            search_id_data = await self.client.request_json(
                "POST",
                f"https://{host}/phonebook/search",
                params={"k": key},
                json_body={
                    "Maxresults": 100000,
                    "Media": 0,
                    "Target": 1,
                    "Term": target,
                    "Terminate": None,
                    "Timeout": 20,
                },
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        search_id = search_id_data.get("id")
        if not search_id:
            return ResourceResult(self.name, target, recursion_depth, [])

        # Step 2: poll for results.
        # Legacy status semantics (confirmed from legacy code + IntelX docs):
        #   status == 3  →  results still assembling, keep polling
        #   status == 0  →  complete, stop
        #   anything else →  error / timeout, stop
        findings: set[str] = set()
        for _ in range(20):
            try:
                data = await self.client.get_json(
                    f"https://{host}/phonebook/search/result",
                    params={"k": key, "id": search_id, "limit": "10000"},
                    expected_status={200},
                )
            except RuntimeError:
                break

            for item in data.get("selectors", []):
                value = item.get("selectorvalue", "")
                if value:
                    findings.add(value)

            status = data.get("status")
            if status != 3:
                # status 0 → done; anything else (error/timeout) → also stop
                break

            await asyncio.sleep(0.25)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
