from __future__ import annotations

import logging
from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource

logger = logging.getLogger(__name__)


class ThreatBookResource(BaseResource):
    name = "threatbook"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        api_url = f"https://api.threatbook.cn/v3/domain/sub_domains?apikey={key}&resource={target}"

        try:
            data = await self.client.get_json(
                api_url,
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()

        if isinstance(data, dict):
            response_code = data.get("response_code")
            if response_code != 0:
                msg = data.get("verbose_msg", "Unknown error")
                logger.debug(f"[ThreatBook] API Error code {response_code}, {msg}")
                return ResourceResult(self.name, target, recursion_depth, [])

            data_dict = data.get("data")
            if isinstance(data_dict, dict):
                sub_domains_dict = data_dict.get("sub_domains")
                if isinstance(sub_domains_dict, dict):
                    # Natively pull from data array bypassing unnecessary total parseInt casts
                    sub_data = sub_domains_dict.get("data", [])
                    if isinstance(sub_data, list):
                        for subds in sub_data:
                            if isinstance(subds, str) and subds:
                                findings.add(subds)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
