from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class WindvaneResource(BaseResource):
    name = "windvane"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        headers = {"Content-Type": "application/json", "X-Api-Key": key}
        api_url = "https://windvane.lichoin.com/trpc.backendhub.public.WindvaneService/ListSubDomain"

        page = 1
        count = 1000
        findings: set[str] = set()

        while True:
            req_body = {
                "domain": target,
                "page_request": {
                    "page": page,
                    "count": count
                }
            }

            try:
                data = await self.client.request_json(
                    "POST",
                    api_url,
                    json_body=req_body,
                    headers=headers,
                    expected_status={200},
                )
            except RuntimeError:
                break

            if not isinstance(data, dict):
                break

            data_block = data.get("data", {})
            if not isinstance(data_block, dict):
                break

            records = data_block.get("list", [])
            if isinstance(records, list):
                for record in records:
                    if isinstance(record, dict):
                        domain = record.get("domain")
                        if isinstance(domain, str) and domain:
                            findings.add(domain)

            page_info = data_block.get("page_response", {})
            if not isinstance(page_info, dict):
                break

            try:
                total_records = int(page_info.get("total", 0))
                records_per_page = int(page_info.get("count", 0))
            except ValueError:
                break

            if records_per_page == 0:
                break

            if (page - 1) * records_per_page >= total_records:
                break

            page += 1

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
