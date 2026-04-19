from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path

from subdominator.core.provider_config import ProviderConfig


class ProviderConfigTests(unittest.TestCase):
    def test_load_and_extract_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "provider-config.yaml"
            path.write_text(
                "virustotal:\n"
                "  - key-a\n"
                "securitytrails:\n"
                "  - user:key-b\n",
                encoding="utf-8",
            )

            config = ProviderConfig(path)
            asyncio.run(config.load())

            self.assertEqual(config.get_values("virustotal"), ["key-a"])
            self.assertEqual(config.get_random_pair("securitytrails"), ("user", "key-b"))

    def test_aliases_cover_shared_and_legacy_provider_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "provider-config.yaml"
            path.write_text(
                "rapidapi:\n"
                "  - rapid-key\n"
                "whoisxmlapi:\n"
                "  - whois-key\n"
                "zoomeye:\n"
                "  - api.zoomeye.hk:zoom-key\n",
                encoding="utf-8",
            )

            config = ProviderConfig(path)
            asyncio.run(config.load())

            self.assertEqual(config.get_values("coderog"), ["rapid-key"])
            self.assertEqual(config.get_values("rapidfinder"), ["rapid-key"])
            self.assertEqual(config.get_values("rapidscan"), ["rapid-key"])
            self.assertEqual(config.get_values("whoisxml"), ["whois-key"])
            self.assertEqual(config.get_random_pair("zoomeyeapi"), ("api.zoomeye.hk", "zoom-key"))

    def test_intelx_pair_preserves_legacy_left_split(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "provider-config.yaml"
            path.write_text(
                "intelx:\n"
                "  - intelx.example:9443:key-a\n",
                encoding="utf-8",
            )

            config = ProviderConfig(path)
            asyncio.run(config.load())

            self.assertEqual(config.get_random_pair("intelx"), ("intelx.example", "9443:key-a"))
            self.assertEqual(
                config.get_random_pair("intelx", from_right=True),
                ("intelx.example:9443", "key-a"),
            )


if __name__ == "__main__":
    unittest.main()
