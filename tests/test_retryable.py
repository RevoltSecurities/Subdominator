from __future__ import annotations

import asyncio
import unittest

from revoltlogger import LogLevel, Logger

from subdominator.http.retryable import RetryableHttpClient
from subdominator.resources.providers.fofa import FofaResource
from subdominator.resources.providers.thc import ThcResource


class _FakeProviderConfig:
    def get_random_value(self, _: str) -> str | None:
        return "test-key"


class _FofaClient:
    def __init__(self) -> None:
        self.logger = Logger(name="test", level=LogLevel.NONE)
        self.calls = 0

    async def get_json(self, url: str, *, params: dict[str, str]) -> dict:
        self.calls += 1
        if self.calls == 1:
            return {
                "results": [
                    ["https://a.example.com:443"],
                    ["http://b.example.com:80"],
                    ["c.example.com"],
                ],
                "size": 1000,
            }
        raise RuntimeError("request failed after 1 attempts: GET https://fofa.info/api/v1/search/all returned unexpected status 429")


class _ThcClient:
    def __init__(self) -> None:
        self.logger = Logger(name="test", level=LogLevel.NONE)
        self.calls = 0

    async def request_json(self, method: str, url: str, *, json_body: dict, headers: dict[str, str], expected_status: set[int]) -> dict:
        self.calls += 1
        raise RuntimeError("request failed after 1 attempts: POST https://ip.thc.org/api/v1/lookup/subdomains returned unexpected status 429")


class _FakeResponse:
    def __init__(self, status: int, text: str = "") -> None:
        self.status = status
        self._text = text
        self.headers: dict[str, str] = {}

    async def text(self) -> str:
        return self._text


class _FakeRequestContext:
    def __init__(self, response: _FakeResponse) -> None:
        self._response = response

    async def __aenter__(self) -> _FakeResponse:
        return self._response

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None


class _FakeSession:
    def __init__(self, responses: list[_FakeResponse]) -> None:
        self.responses = responses
        self.calls = 0

    def request(self, *args, **kwargs) -> _FakeRequestContext:
        response = self.responses[self.calls]
        self.calls += 1
        return _FakeRequestContext(response)


class RetryableHttpClientTests(unittest.TestCase):
    def test_unexpected_429_is_not_retried(self) -> None:
        async def run_check() -> int:
            client = RetryableHttpClient(
                logger=Logger(name="test", level=LogLevel.NONE),
                retries=5,
            )
            client._session = _FakeSession([_FakeResponse(429)])
            with self.assertRaises(RuntimeError):
                await client.request("GET", "https://example.com", expected_status=200)
            return client._session.calls

        calls = asyncio.run(run_check())
        self.assertEqual(calls, 1)


class ProviderPartialResultTests(unittest.TestCase):
    def test_fofa_keeps_partial_findings_when_later_page_fails(self) -> None:
        async def run_check() -> list[str]:
            resource = FofaResource(_FofaClient(), _FakeProviderConfig())  # type: ignore[arg-type]
            result = await resource.enumerate("example.com", 0)
            return result.findings

        findings = asyncio.run(run_check())
        self.assertEqual(findings, ["a.example.com", "b.example.com", "c.example.com"])

    def test_thc_skips_future_requests_after_rate_limit(self) -> None:
        async def run_check() -> tuple[int, list[str], list[str]]:
            client = _ThcClient()
            resource = ThcResource(client, _FakeProviderConfig())  # type: ignore[arg-type]
            first = await resource.enumerate("example.com", 0)
            second = await resource.enumerate("api.example.com", 1)
            return client.calls, first.findings, second.findings

        calls, first_findings, second_findings = asyncio.run(run_check())
        self.assertEqual(calls, 1)
        self.assertEqual(first_findings, [])
        self.assertEqual(second_findings, [])


if __name__ == "__main__":
    unittest.main()
