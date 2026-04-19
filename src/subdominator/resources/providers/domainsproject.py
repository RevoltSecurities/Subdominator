from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class DomainsProjectResource(BaseResource):
    name = "domainsproject"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        username, password = self.provider_config.get_random_pair(self.name)
        if not username or not password:
            return ResourceResult(self.name, target, recursion_depth, [])

        headers = {
            "Authorization": self.client.basic_auth_header(username, password),
        }

        try:
            data = await self.client.get_json(
                f"https://api.domainsproject.org/api/tld/search?domain={target}",
                headers=headers,
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()
        
        if isinstance(data, dict):
            error_msg = data.get("error", "")
            if error_msg:
                # Silently fail on API level errors
                return ResourceResult(self.name, target, recursion_depth, [])

            domains = data.get("domains")
            if isinstance(domains, list):
                for subdomain in domains:
                    if isinstance(subdomain, str) and not subdomain.startswith("."):
                        findings.add(subdomain)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
