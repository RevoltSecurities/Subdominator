from __future__ import annotations

import re
import urllib.parse

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource

class WaybackArchiveResource(BaseResource):
    name = "waybackarchive"
    requires_config = False

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            text = await self.client.request(
                "GET",
                f"http://web.archive.org/cdx/search/cdx?url=*.{target}/*&output=txt&fl=original&collapse=urlkey",
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()

        # Engine extractor matching explicit pattern matching global regex extraction
        pattern = re.compile(rf'[a-zA-Z0-9\*_.-]+\.{re.escape(target)}', re.IGNORECASE)

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            line = urllib.parse.unquote(line)
            
            for match in pattern.finditer(line):
                subdomain = match.group(0).lower()
                
                # TrimPrefix exact match mechanics matching legacy codebase
                if subdomain.startswith("25"):
                    subdomain = subdomain[2:]
                if subdomain.startswith("2f"):
                    subdomain = subdomain[2:]
                    
                subdomain = subdomain.strip('"\'>/<')
                if subdomain:
                    findings.add(subdomain)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
