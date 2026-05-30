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



# Exact v2 flat template written by v2.1.x config.py — the first line has no space
# after the colon (arpsyndicate:[]) which causes yaml.safe_load to raise ScannerError.
_V2_FLAT_TEMPLATE = (
    "arpsyndicate:[]\n"
    "\n"
    "bevigil: []          \n"
    "\n"
    "binaryedge: []\n"
    "\n"
    "bufferover: []\n"
    "\n"
    "github: []\n"
    "\n"
    "virustotal: []\n"
    "\n"
    "# for notifications\n"
    "slack: []\n"
    "\n"
    "pushbullet: []\n"
)


class V2MigrationTests(unittest.TestCase):

    def test_v2_flat_empty_migrates_without_crash(self) -> None:
        """Exact v2 template (arpsyndicate:[] no space) must not crash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "provider-config.yaml"
            path.write_text(_V2_FLAT_TEMPLATE, encoding="utf-8")

            config = ProviderConfig(path)
            asyncio.run(config.load())   # must not raise

            self.assertEqual(config.get_values("bevigil"), [])
            self.assertEqual(config.get_values("virustotal"), [])

    def test_v2_flat_filled_keys_preserved(self) -> None:
        """Keys filled in by the user inside the v2 flat format are carried over."""
        content = (
            "arpsyndicate:[]\n"
            "\n"
            "bevigil: [my_bevigil_key]\n"
            "\n"
            "github: [ghp_tokenABC]\n"
            "\n"
            "virustotal: []\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "provider-config.yaml"
            path.write_text(content, encoding="utf-8")

            config = ProviderConfig(path)
            asyncio.run(config.load())

            self.assertEqual(config.get_values("bevigil"), ["my_bevigil_key"])
            self.assertEqual(config.get_values("github"), ["ghp_tokenABC"])
            self.assertEqual(config.get_values("virustotal"), [])

    def test_v2_flat_block_list_keys_preserved(self) -> None:
        """Block-list format under v2 flat header preserves multiple keys."""
        content = (
            "arpsyndicate:[]\n"
            "\n"
            "bevigil:\n"
            "- key_one\n"
            "- key_two\n"
            "\n"
            "virustotal: []\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "provider-config.yaml"
            path.write_text(content, encoding="utf-8")

            config = ProviderConfig(path)
            asyncio.run(config.load())

            self.assertEqual(config.get_values("bevigil"), ["key_one", "key_two"])

    def test_v2_placeholder_values_filtered(self) -> None:
        """Placeholder values (#YOUR_...) must not appear in the migrated data."""
        content = (
            "arpsyndicate:[]\n"
            "\n"
            "bevigil: [#YOUR_BEVIGIL_API_KEY]\n"
            "\n"
            "virustotal: []\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "provider-config.yaml"
            path.write_text(content, encoding="utf-8")

            config = ProviderConfig(path)
            asyncio.run(config.load())

            self.assertEqual(config.get_values("bevigil"), [])

    def test_v2_nested_old_format_keys_preserved(self) -> None:
        """Very old v2 nested format (Provider:\\n  api_key: val) preserves values."""
        content = (
            "arpsyndicate:[]\n"
            "\n"
            "Bevigil:\n"
            "\n"
            "  api_key: real_bevigil_key\n"
            "\n"
            "virustotal: []\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "provider-config.yaml"
            path.write_text(content, encoding="utf-8")

            config = ProviderConfig(path)
            asyncio.run(config.load())

            self.assertEqual(config.get_values("bevigil"), ["real_bevigil_key"])

    def test_v2_migration_rewrites_file_as_valid_yaml(self) -> None:
        """After migration the on-disk file must be parseable by yaml.safe_load."""
        import yaml

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "provider-config.yaml"
            path.write_text(_V2_FLAT_TEMPLATE, encoding="utf-8")

            config = ProviderConfig(path)
            asyncio.run(config.load())

            reloaded = yaml.safe_load(path.read_text(encoding="utf-8"))
            self.assertIsInstance(reloaded, dict)

    def test_v2_migration_all_template_keys_present_after(self) -> None:
        """All PROVIDER_TEMPLATE keys must exist in the migrated config."""
        from subdominator.core.provider_config import PROVIDER_TEMPLATE

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "provider-config.yaml"
            path.write_text(_V2_FLAT_TEMPLATE, encoding="utf-8")

            config = ProviderConfig(path)
            asyncio.run(config.load())

            for key in PROVIDER_TEMPLATE:
                self.assertIn(key, config.data, f"Missing key after migration: {key}")

    def test_v3_format_completely_unaffected(self) -> None:
        """Valid v3 YAML must load normally without triggering migration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "provider-config.yaml"
            path.write_text(
                "virustotal:\n  - vt-key\nbevigil:\n  - bv-key\n",
                encoding="utf-8",
            )

            config = ProviderConfig(path)
            asyncio.run(config.load())

            self.assertEqual(config.get_values("virustotal"), ["vt-key"])
            self.assertEqual(config.get_values("bevigil"), ["bv-key"])


if __name__ == "__main__":
    unittest.main()
