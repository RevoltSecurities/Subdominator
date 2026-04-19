from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

import tldextract

from subdominator.core.models import ResourceResult
from subdominator.core.provider_config import ProviderConfig
from subdominator.http.retryable import RetryableHttpClient


_TLD_EXTRACT = tldextract.TLDExtract(suffix_list_urls=(), cache_dir=None)


class BaseResource(ABC):
    name: str
    requires_config: bool = False
    has_optional_config: bool = False

    def __init__(self, client: RetryableHttpClient, provider_config: ProviderConfig) -> None:
        self.client = client
        self.provider_config = provider_config

    @abstractmethod
    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        raise NotImplementedError

    def normalize_findings(self, target: str, items: Iterable[str]) -> list[str]:
        normalized: set[str] = set()
        target = target.lower().strip()
        for item in items:
            value = item.strip().lower().lstrip("*.") if item else ""
            if value.endswith(f".{target}") or value == target:
                normalized.add(value)
        return sorted(normalized)

    @staticmethod
    def registered_domain(value: str) -> str:
        extracted = _TLD_EXTRACT(value)
        return ".".join(part for part in [extracted.domain, extracted.suffix] if part)

    def get_required_value(self) -> str | None:
        value = self.provider_config.get_random_value(self.name)
        if value is None:
            self.client.logger.debug(f"Skipping {self.name}: provider config value is missing")
        return value

    def get_required_pair(
        self,
        separator: str = ":",
        from_right: bool = False,
    ) -> tuple[str | None, str | None]:
        left, right = self.provider_config.get_random_pair(
            self.name,
            separator=separator,
            from_right=from_right,
        )
        if left is None or right is None:
            self.client.logger.debug(f"Skipping {self.name}: provider config pair is missing")
        return left, right
