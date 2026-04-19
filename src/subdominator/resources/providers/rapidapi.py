from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class RapidApiResource(BaseResource):
    name = "rapidapi"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        rapidapi_key = self.provider_config.get_random_value("rapidapi")
        whoisxml_key = self.provider_config.get_random_value("whoisxml")
        if rapidapi_key is None or whoisxml_key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                "https://subdomains-lookup.p.rapidapi.com/api/v1",
                headers={
                    "X-RapidAPI-Key": rapidapi_key,
                    "X-RapidAPI-Host": "subdomains-lookup.p.rapidapi.com",
                },
                params={"domainName": target, "apiKey": whoisxml_key, "outputFormat": "JSON"},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [
            record.get("domain", "")
            for record in data.get("result", {}).get("records", [])
            if isinstance(record, dict)
        ]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
