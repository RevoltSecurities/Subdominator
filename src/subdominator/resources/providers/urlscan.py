from __future__ import annotations

import re
import urllib.parse
from urllib.parse import urlparse

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class UrlscanResource(BaseResource):
    name = "urlscan"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        headers = {"api-key": key}
        base_url = "https://urlscan.io/api/v1/search/"
        max_pages = 5
        max_per_page = 100
        
        search_after = ""
        current_page = 0
        findings: set[str] = set()

        pattern = re.compile(rf'[a-zA-Z0-9\*_.-]+\.{re.escape(target)}', re.IGNORECASE)

        while current_page < max_pages:
            search_url = f"{base_url}?q=domain:{urllib.parse.quote(target)}&size={max_per_page}"
            if search_after:
                search_url += f"&search_after={urllib.parse.quote(search_after)}"

            try:
                data = await self.client.get_json(
                    search_url,
                    headers=headers,
                    expected_status={200},
                )
            except RuntimeError:
                break

            if not isinstance(data, dict):
                break

            results = data.get("results", [])
            if not isinstance(results, list):
                break

            for result in results:
                if not isinstance(result, dict):
                    continue

                task = result.get("task", {})
                page = result.get("page", {})
                
                candidates = []
                if isinstance(task, dict):
                    candidates.append(task.get("domain", ""))
                    task_url = task.get("url", "")
                    if task_url:
                        try:
                            parsed = urlparse(task_url)
                            if parsed.hostname:
                                candidates.append(parsed.hostname)
                        except Exception:
                            pass
                            
                if isinstance(page, dict):
                    candidates.append(page.get("domain", ""))
                    page_url = page.get("url", "")
                    if page_url:
                        try:
                            parsed = urlparse(page_url)
                            if parsed.hostname:
                                candidates.append(parsed.hostname)
                        except Exception:
                            pass

                for candidate in candidates:
                    if not candidate:
                        continue
                    for match in pattern.finditer(candidate):
                        val = match.group(0).lower()
                        val = val.strip('"\'>/<')
                        findings.add(val)

            has_more = data.get("has_more", False)
            if not has_more or len(results) == 0:
                break

            last_result = results[-1]
            if not isinstance(last_result, dict):
                break
                
            sort_arr = last_result.get("sort", [])
            if not sort_arr or not isinstance(sort_arr, list):
                break

            sort_values = []
            for v in sort_arr:
                if isinstance(v, (int, float)):
                    sort_values.append(f"{v:.0f}")
                else:
                    sort_values.append(str(v))
            
            search_after = ",".join(sort_values)
            current_page += 1

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
