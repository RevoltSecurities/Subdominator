from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path

from revoltlogger import LogLevel, Logger

from subdominator.core.provider_config import ProviderConfig
from subdominator.http.retryable import RetryableHttpClient
from subdominator.resources.registry import ResourceRegistry


class RegistryTests(unittest.TestCase):
    def test_metadata_marks_config_backed_resources(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ProviderConfig(Path(tmpdir) / "provider-config.yaml")
            asyncio.run(config.load())

            async def run_check() -> list[tuple[str, bool]]:
                async with RetryableHttpClient(
                    logger=Logger(name="test", level=LogLevel.NONE),
                    timeout=1,
                    retries=1,
                ) as client:
                    registry = ResourceRegistry(client, config)
                    return registry.all_metadata()

            metadata = {str(item["name"]): bool(item["requires_config"]) for item in asyncio.run(run_check())}

            self.assertFalse(metadata["crtsh"])
            self.assertFalse(metadata["abuseipdb"])
            self.assertFalse(metadata["cyfare"])
            self.assertFalse(metadata["hudsonrock"])
            self.assertFalse(metadata["sitedossier"])
            self.assertFalse(metadata["myssl"])
            self.assertFalse(metadata["racent"])
            self.assertFalse(metadata["shodanx"])
            self.assertFalse(metadata["shrewdeye"])
            self.assertTrue(metadata["binaryedge"])
            self.assertTrue(metadata["bevigil"])
            self.assertTrue(metadata["builtwith"])
            self.assertTrue(metadata["c99"])
            self.assertTrue(metadata["censys"])
            self.assertTrue(metadata["certspotter"])
            self.assertTrue(metadata["coderog"])
            self.assertTrue(metadata["facebook"])
            self.assertTrue(metadata["google"])
            self.assertTrue(metadata["huntermap"])
            self.assertTrue(metadata["intelx"])
            self.assertTrue(metadata["merklemap"])
            self.assertTrue(metadata["odin"])
            self.assertTrue(metadata["quake"])
            self.assertTrue(metadata["rapidapi"])
            self.assertTrue(metadata["rapidfinder"])
            self.assertTrue(metadata["rapidscan"])
            self.assertTrue(metadata["redhuntlabs"])
            self.assertTrue(metadata["rsecloud"])
            self.assertTrue(metadata["trickest"])
            self.assertTrue(metadata["virustotal"])
            self.assertTrue(metadata["securitytrails"])
            self.assertTrue(metadata["bufferover"])
            self.assertTrue(metadata["shodan"])
            self.assertTrue(metadata["whoisxml"])
            self.assertTrue(metadata["netlas"])
            self.assertTrue(metadata["zoomeyeapi"])

    def test_default_selection_skips_long_running_resources(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ProviderConfig(Path(tmpdir) / "provider-config.yaml")
            asyncio.run(config.load())

            async def run_check() -> tuple[list[str], list[str], list[str], list[str]]:
                async with RetryableHttpClient(
                    logger=Logger(name="test", level=LogLevel.NONE),
                    timeout=1,
                    retries=1,
                ) as client:
                    registry = ResourceRegistry(client, config)
                    default_names = [resource.name for resource in registry.select()]
                    all_names = [resource.name for resource in registry.select(include_all=True)]
                    include_names = [resource.name for resource in registry.select(include=["github", "virustotal"])]
                    exclude_names = [
                        resource.name
                        for resource in registry.select(include=["github", "virustotal"], exclude=["github"])
                    ]
                    return default_names, all_names, include_names, exclude_names

            default_names, all_names, include_names, exclude_names = asyncio.run(run_check())

            self.assertNotIn("commoncrawl", default_names)
            self.assertNotIn("github", default_names)
            self.assertNotIn("virustotal", default_names)
            self.assertNotIn("waybackarchive", default_names)
            self.assertIn("github", all_names)
            self.assertIn("virustotal", all_names)
            self.assertEqual(include_names, ["github", "virustotal"])
            self.assertEqual(exclude_names, ["virustotal"])


if __name__ == "__main__":
    unittest.main()
