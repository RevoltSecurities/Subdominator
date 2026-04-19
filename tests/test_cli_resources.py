from __future__ import annotations

import unittest

from subdominator.cli.app import _render_resource_markdown


class CliResourceFormattingTests(unittest.TestCase):
    def test_plain_resource_markdown(self) -> None:
        self.assertEqual(
            _render_resource_markdown("crtsh", "crtsh", "https://crt.sh", False),
            "[***crtsh***](https://crt.sh)",
        )

    def test_config_resource_markdown(self) -> None:
        self.assertEqual(
            _render_resource_markdown("virustotal", "virustotal", "https://virustotal.com/", True),
            "[***virustotal****](https://virustotal.com/)",
        )


if __name__ == "__main__":
    unittest.main()
