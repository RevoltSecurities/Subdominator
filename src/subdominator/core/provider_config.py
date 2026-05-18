from __future__ import annotations

import random
from pathlib import Path

import aiofiles
import yaml


PROVIDER_ALIASES: dict[str, tuple[str, ...]] = {
    "coderog": ("rapidapi",),
    "rapidfinder": ("rapidapi",),
    "rapidscan": ("rapidapi",),
    "whoisxml": ("whoisxmlapi",),
    "zoomeyeapi": ("zoomeye",),
}

PROVIDER_TEMPLATE: dict[str, list[str]] = {
    "alienvault": [],
    "anubis": [],
    "argosdns": [],
    "arpsyndicate": [],
    "bevigil": [],
    "binaryedge": [],
    "bufferover": [],
    "builtwith": [],
    "c99": [],
    "censys": [],
    "sitedossier": [],
    "submd": [],
    "thc": [],
    "threatbook": [],
    "threatcrowd": [],
    "threatminer": [],
    "certspotter": [],
    "chaos": [],
    "chinaz": [],
    "coderog": [],
    "digitalyama": [],
    "dnsdb": [],
    "dnsdumpster": [],
    "domscan": [],
    "dnsrepo": [],
    "domainsproject": [],
    "driftnet": [],
    "facebook": [],
    "fofa": [],
    "fullhunt": [],
    "github": [],
    "google": [],
    "hackertarget": [],
    "hudsonrock": [],
    "huntermap": [],
    "intelx": [],
    "leakix": [],
    "merklemap": [],
    "netlas": [],
    "odin": [],
    "onyphe": [],
    "profundis": [],
    "pugrecon": [],
    "quake": [],
    "rapidapi": [],
    "rapiddns": [],
    "rapidfinder": [],
    "rapidscan": [],
    "reconcloud": [],
    "reconeer": [],
    "redhuntlabs": [],
    "riddler": [],
    "robtex": [],
    "rsecloud": [],
    "securitytrails": [],
    "shodan": [],
    "shodanx": [],
    "trickest": [],
    "urlscan": [],
    "virustotal": [],
    "waybackarchive": [],
    "windvane": [],
    "whoisfreaks": [],
    "whoisxml": [],
    "zoomeyeapi": [],
    "slack": [],
    "pushbullet": [],
}


class ProviderConfig:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data: dict[str, list[str]] = {}

    async def load(self) -> None:
        if not self.path.exists():
            self.data = PROVIDER_TEMPLATE.copy()
            await self.dump(self.data)
            return

        async with aiofiles.open(self.path, encoding="utf-8") as fh:
            raw = await fh.read()
        loaded: dict = yaml.safe_load(raw) or {}
        self.data = {
            str(key).lower(): [str(value) for value in values]
            for key, values in loaded.items()
            if isinstance(values, list)
        }

        missing_keys = False
        for key in PROVIDER_TEMPLATE:
            if key not in self.data:
                self.data[key] = []
                missing_keys = True
                
        if missing_keys:
            await self.dump(self.data)

    async def dump(self, data: dict) -> None:
        """Write *data* back to the provider config file using yaml.dump."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        text = yaml.dump(data, default_flow_style=False, allow_unicode=True)
        async with aiofiles.open(self.path, "w", encoding="utf-8") as fh:
            await fh.write(text)

    def get_values(self, provider: str) -> list[str]:
        names = (provider.lower(), *PROVIDER_ALIASES.get(provider.lower(), ()))
        values: list[str] = []
        for name in names:
            values.extend(self.data.get(name, []))
        return [value for value in values if value]

    def get_random_value(self, provider: str) -> str | None:
        values = self.get_values(provider)
        return random.choice(values) if values else None

    def get_random_pair(
        self,
        provider: str,
        separator: str = ":",
        from_right: bool = False,
    ) -> tuple[str | None, str | None]:
        value = self.get_random_value(provider)
        if value is None or separator not in value:
            return None, None
        left, right = value.rsplit(separator, 1) if from_right else value.split(separator, 1)
        return left.strip(), right.strip()
