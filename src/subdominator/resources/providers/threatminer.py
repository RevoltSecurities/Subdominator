from __future__ import annotations

import logging
from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource

logger = logging.getLogger(__name__)


class ThreatMinerResource(BaseResource):
    name = "threatminer"
    requires_config = False

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        api_url = f"https://api.threatminer.org/v2/domain.php?q={target}&rt=5"

        try:
            data = await self.client.get_json(
                api_url,
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()

        if isinstance(data, dict):
            status_code = data.get("status_code", "")
            if str(status_code) != "200":
                msg = data.get("status_message", "Unknown status")
                logger.debug(f"[ThreatMiner] API Error: {msg}")

            results = data.get("results", [])
            if isinstance(results, list):
                for subdomain in results:
                    if isinstance(subdomain, str) and subdomain:
                        findings.add(subdomain)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
