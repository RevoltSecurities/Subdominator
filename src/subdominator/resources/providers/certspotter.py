from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class CertSpotterResource(BaseResource):
    name = "certspotter"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: list[str] = []
        headers = {"Authorization": f"Bearer {key}"}

        # Legacy: start with the base URL including all params, then subsequent
        # pages embed the `after` cursor directly into the URL. Use None as the
        # sentinel for "done" (cleaner than an empty string).
        next_url: str | None = (
            f"https://api.certspotter.com/v1/issuances"
            f"?domain={target}&include_subdomains=true&expand=dns_names"
        )

        while next_url is not None:
            try:
                data = await self.client.get_json(
                    next_url,
                    headers=headers,
                    expected_status={200},
                )
            except RuntimeError:
                # Non-200 (auth error, rate limit) — return what we have.
                break

            if not isinstance(data, list) or not data:
                break

            for entry in data:
                findings.extend(entry.get("dns_names", []))

            last_id = data[-1].get("id")
            if last_id:
                next_url = (
                    f"https://api.certspotter.com/v1/issuances"
                    f"?domain={target}&include_subdomains=true&expand=dns_names&after={last_id}"
                )
            else:
                next_url = None

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
