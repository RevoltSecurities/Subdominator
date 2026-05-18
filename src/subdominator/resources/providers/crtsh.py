from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class CrtShResource(BaseResource):
    name = "crtsh"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        findings: list[str] = []

        try:
            findings = await self._get_from_sql(target)
        except ImportError:
            self.client.logger.debug("crtsh postgres skipped: asyncpg not installed, using HTTP fallback")
        except Exception as e:
            self.client.logger.debug(f"crtsh postgres connection failed for {target}: {e}")

        if not findings:
            findings = await self._get_from_http(target)

        return ResourceResult(
            self.name, target, recursion_depth, self.normalize_findings(target, findings)
        )

    async def _get_from_sql(self, target: str) -> list[str]:
        try:
            import asyncpg
        except ImportError:
            raise ImportError("asyncpg is required for crt.sh PostgreSQL queries")

        findings: list[str] = []
        timeout = 20.0
        if hasattr(self.client, "timeout") and hasattr(self.client.timeout, "total") and self.client.timeout.total:
             timeout = self.client.timeout.total

        conn = await asyncpg.connect(
            host="crt.sh",
            user="guest",
            database="certwatch",
            timeout=timeout,
            statement_cache_size=0,
            ssl=False,
        )

        try:
            # Set statement timeout dynamically based on client config
            await conn.execute(f"SET statement_timeout = '{int(timeout * 1000)}'")
            
            query = """
            WITH ci AS (
                SELECT min(sub.CERTIFICATE_ID) ID,
                    min(sub.ISSUER_CA_ID) ISSUER_CA_ID,
                    array_agg(DISTINCT sub.NAME_VALUE) NAME_VALUES,
                    x509_commonName(sub.CERTIFICATE) COMMON_NAME,
                    x509_notBefore(sub.CERTIFICATE) NOT_BEFORE,
                    x509_notAfter(sub.CERTIFICATE) NOT_AFTER,
                    encode(x509_serialNumber(sub.CERTIFICATE), 'hex') SERIAL_NUMBER
                    FROM (SELECT *
                            FROM certificate_and_identities cai
                            WHERE plainto_tsquery('certwatch', $1) @@ identities(cai.CERTIFICATE)
                                AND cai.NAME_VALUE ILIKE ('%' || $1 || '%')
                                LIMIT 10000
                        ) sub
                    GROUP BY sub.CERTIFICATE
            )
            SELECT array_to_string(ci.NAME_VALUES, chr(10)) NAME_VALUE
                FROM ci
                        LEFT JOIN LATERAL (
                            SELECT min(ctle.ENTRY_TIMESTAMP) ENTRY_TIMESTAMP
                                FROM ct_log_entry ctle
                                WHERE ctle.CERTIFICATE_ID = ci.ID
                        ) le ON TRUE,
                    ca
                WHERE ci.ISSUER_CA_ID = ca.ID
                ORDER BY le.ENTRY_TIMESTAMP DESC NULLS LAST;
            """
            
            rows = await conn.fetch(query, target)
            for row in rows:
                if row.get("name_value"):
                    findings.extend(row["name_value"].splitlines())
        finally:
            await conn.close()
            
        return findings

    async def _get_from_http(self, target: str) -> list[str]:
        try:
            data = await self.client.get_json(
                f"https://crt.sh/?q=%25.{target}&output=json",
                expected_status={200},
            )
        except RuntimeError:
            return []

        findings: list[str] = []
        for entry in data:
            findings.extend(entry.get("name_value", "").splitlines())
        return findings
