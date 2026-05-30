from __future__ import annotations

import re
import random
import sys
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

        migrated = False
        try:
            loaded: dict = yaml.safe_load(raw) or {}
        except yaml.YAMLError:
            loaded = self._parse_v2(raw)
            migrated = True
            print(
                f"\n[Subdominator] provider-config.yaml was in an older v2 format and has "
                f"been automatically migrated to v3. Your existing API keys have been preserved.\n"
                f"  Config: {self.path}\n",
                file=sys.stderr,
            )

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

        if missing_keys or migrated:
            await self.dump(self.data)

    def _parse_v2(self, raw: str) -> dict[str, list[str]]:
        """Line-by-line parser for v2 provider-config formats that fail yaml.safe_load.

        Handles both v2 formats found in the wild:
        - Flat (v2.1.x): arpsyndicate:[]  /  bevigil: [mykey]  /  block list (- mykey)
        - Nested (very old v2): Bevigil:\\n  api_key: realvalue

        Placeholder values starting with '#' are filtered out.
        """
        data: dict[str, list[str]] = {}
        current_key: str | None = None

        for line in raw.splitlines():
            stripped = line.strip()

            if not stripped or stripped.startswith('#'):
                continue

            # Block list item: "- value" under the current provider key
            if stripped.startswith('- ') and current_key is not None:
                value = stripped[2:].strip().strip('"\'')
                if value and not value.startswith('#'):
                    data.setdefault(current_key, []).append(value)
                continue

            m = re.match(r'^([A-Za-z][A-Za-z0-9_]*)\s*:\s*(.*)', stripped)
            if not m:
                continue

            key_raw, value_part = m.group(1), m.group(2).strip()

            # Indented line = nested sub-field of current provider (very old v2 format)
            if line[:1] in (' ', '\t') and current_key is not None:
                if value_part and not value_part.startswith('#'):
                    data.setdefault(current_key, []).append(value_part)
                continue

            # Top-level provider key
            current_key = key_raw.lower()
            data.setdefault(current_key, [])

            # Inline flow sequence: [] or [val] or [v1, v2]
            if value_part.startswith('['):
                inner = value_part.lstrip('[').rstrip().rstrip(']').strip()
                if inner:
                    for v in inner.split(','):
                        v = v.strip().strip('"\'')
                        if v and not v.startswith('#'):
                            data[current_key].append(v)
            elif value_part and not value_part.startswith('#'):
                data[current_key].append(value_part)

        return data

    async def dump(self, data: dict) -> None:
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
