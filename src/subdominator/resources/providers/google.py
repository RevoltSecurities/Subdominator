from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource

# Google Custom Search Engine caps results at 100 (start index 1..91, 10 results each).
# Requesting start > 100 returns HTTP 400 which the retryable client raises as an error.
_CSE_MAX_START = 91
_CSE_PAGE_SIZE = 10


class GoogleResource(BaseResource):
    name = "google"
    requires_config = True

    def __init__(self, client, provider_config, dork: str | None = None) -> None:
        super().__init__(client, provider_config)
        self.dork = dork

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        cx, key = self.get_required_pair()
        if cx is None or key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        dork = self.dork or f"site:*.{target} -www"
        start = 1
        findings: set[str] = set()

        while start <= _CSE_MAX_START:
            try:
                data = await self.client.get_json(
                    "https://customsearch.googleapis.com/customsearch/v1",
                    params={
                        "q": dork,
                        "cx": cx,
                        "num": str(_CSE_PAGE_SIZE),
                        "start": str(start),
                        "key": key,
                        "alt": "json",
                    },
                    expected_status={200},
                )
            except RuntimeError:
                # Non-200 response (e.g. 429 rate-limit, 400 quota exceeded) —
                # return whatever we collected so far rather than marking the
                # entire resource as failed.
                break

            items = data.get("items", [])
            if not items:
                break

            for item in items:
                link = item.get("displayLink", "")
                if link:
                    findings.add(link)

            start += _CSE_PAGE_SIZE

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
