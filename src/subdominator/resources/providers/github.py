import asyncio
import json
import re
import time
import urllib.parse
from typing import Any

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class TokenManager:
    def __init__(self, keys: list[str]) -> None:
        self.pool = [{"hash": key, "exceeded_time": 0.0, "retry_after": 0.0} for key in keys]
        self.current = 0

    def get(self) -> dict[str, Any] | None:
        self._reset_exceeded()
        if not self.pool:
            return None

        start_idx = self.current
        while True:
            idx = self.current % len(self.pool)
            self.current += 1
            if self.pool[idx]["retry_after"] == 0:
                return self.pool[idx]
            if self.current % len(self.pool) == start_idx:
                return None  # All tokens are currently rate-limited

    def set_exceeded(self, token_hash: str, retry_after: float) -> None:
        for t in self.pool:
            if t["hash"] == token_hash:
                if t["retry_after"] == 0:
                    t["exceeded_time"] = time.time()
                    t["retry_after"] = retry_after
                break

    def _reset_exceeded(self) -> None:
        now = time.time()
        for t in self.pool:
            if t["retry_after"] > 0:
                if now - t["exceeded_time"] > t["retry_after"]:
                    t["retry_after"] = 0.0
                    t["exceeded_time"] = 0.0


class GithubResource(BaseResource):
    name = "github"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        keys = self.provider_config.get_values(self.name)
        if not keys:
            return ResourceResult(self.name, target, recursion_depth, [])

        tokens = TokenManager(keys)
        findings: set[str] = set()

        search_url = f"https://api.github.com/search/code?per_page=100&q={urllib.parse.quote(target)}&sort=created&order=asc"
        rdomain = target.replace(".", "\\.")
        domain_pattern = re.compile(rf"([a-zA-Z0-9_\.-]+\.{rdomain})", re.IGNORECASE)

        await self._enumerate_recursive(search_url, domain_pattern, tokens, target, findings)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))

    async def _enumerate_recursive(self, url: str, pattern: re.Pattern, tokens: TokenManager, target: str, findings: set[str]) -> None:
        token = tokens.get()
        if not token:
            return

        headers = {
            "Accept": "application/vnd.github.v3.text-match+json",
            "Authorization": f"token {token['hash']}",
        }

        try:
            async with self.client._session.request("GET", url, headers=headers, proxy=self.client.proxy) as resp:
                text = await resp.text()
                status = resp.status
                resp_headers = dict(resp.headers)
        except Exception:
            return

        if status == 403:
            remaining = int(resp_headers.get("X-Ratelimit-Remaining", -1))
            if remaining == 0:
                retry_after = int(resp_headers.get("Retry-After", 60))
                tokens.set_exceeded(token["hash"], float(retry_after))
                await self._enumerate_recursive(url, pattern, tokens, target, findings)
            return

        if status != 200:
            return

        try:
            data = json.loads(text)
        except Exception:
            return

        items = data.get("items", [])
        tasks = []
        for item in items:
            matches = item.get("text_matches", [])
            for match in matches:
                fragment = match.get("fragment", "")
                self._extract(fragment, pattern, findings)

            html_url = item.get("html_url", "")
            if html_url:
                tasks.append(self._fetch_raw(html_url, pattern, findings))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        link_header = resp_headers.get("Link", "")
        if link_header:
            next_url = self._extract_next_link(link_header)
            if next_url:
                await self._enumerate_recursive(next_url, pattern, tokens, target, findings)

    def _extract_next_link(self, link_header: str) -> str:
        parts = link_header.split(",")
        for part in parts:
            if 'rel="next"' in part:
                url_match = re.search(r'<(.*?)>', part)
                if url_match:
                    return url_match.group(1).strip()
        return ""

    async def _fetch_raw(self, html_url: str, pattern: re.Pattern, findings: set[str]) -> None:
        raw_url = html_url.replace("https://github.com/", "https://raw.githubusercontent.com/")
        raw_url = raw_url.replace("/blob/", "/")
        try:
            text = await self.client.request("GET", raw_url, expected_status=200)
            if text:
                self._extract(text, pattern, findings)
        except Exception:
            pass

    def _extract(self, content: str, pattern: re.Pattern, findings: set[str]) -> None:
        normalized = urllib.parse.unquote(content)
        normalized = normalized.replace("\\t", "").replace("\\n", "")
        for match in pattern.finditer(normalized):
            val = match.group(0).lower()
            val = val.strip('"\'>/<')
            if val:
                findings.add(val)