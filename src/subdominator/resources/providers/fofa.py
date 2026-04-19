from __future__ import annotations

import base64

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class FofaResource(BaseResource):
    name = "fofa"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        page = 1
        query = base64.b64encode(f'domain="{target}" '.encode("utf-8")).decode("utf-8")
        findings: set[str] = set()

        while True:
            try:
                data = await self.client.get_json(
                    "https://fofa.info/api/v1/search/all",
                    params={
                        "key": key,
                        "qbase64": query,
                        "page": str(page),
                        "full": "true",
                        "size": "1000",
                    },
                )
            except RuntimeError:
                break
            results = data.get("results", [])
            if not results:
                break

            for result in results:
                if not result:
                    continue
                host = str(result[0])
                if host.startswith("https://"):
                    host = host[8:]
                elif host.startswith("http://"):
                    host = host[7:]
                host = host.split(":")[0]
                findings.add(host)

            if int(data.get("size", 0) or 0) < 1000:
                break
            page += 1

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
