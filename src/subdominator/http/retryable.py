from __future__ import annotations

import asyncio
import base64
from collections.abc import Mapping
import json
from typing import Any

import aiohttp
from revoltlogger import Logger


class RetryableHttpClient:
    def __init__(
        self,
        logger: Logger,
        timeout: float = 20.0,
        retries: int = 3,
        user_agent: str | None = None,
        proxy: str | None = None,
        ssl_verify: bool = True,
        retry_backoff: float = 1.0, 
    ) -> None:
        self.logger = logger
        self.ssl_verify = ssl_verify
        self.timeout = aiohttp.ClientTimeout(total=timeout, connect=timeout)
        self.retries = retries
        self.retry_backoff = retry_backoff
        self.user_agent = user_agent or "Subdominator/V3.0.0"
        self.proxy = proxy
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "RetryableHttpClient":
        connector = aiohttp.TCPConnector(resolver=aiohttp.ThreadedResolver(), ssl=None if self.ssl_verify else False)
        self._session = aiohttp.ClientSession(
            timeout=self.timeout,
            headers={"User-Agent": self.user_agent},
            trust_env=True,
            connector=connector,
        )
        return self

    async def __aexit__(self, *_: object) -> None:
        if self._session is not None:
            await self._session.close()

    async def request(
        self,
        method: str,
        url: str,
        *,
        expected_status: int | set[int] = 200,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        json_body: Any | None = None,
    ) -> str:
        statuses = {expected_status} if isinstance(expected_status, int) else expected_status
        last_error: Exception | None = None

        if self._session is None:
            raise RuntimeError("RetryableHttpClient session is not initialized")

        for attempt in range(1, self.retries + 1):
            try:
                async with self._session.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    json=json_body,
                    proxy=self.proxy,
                ) as response:
                    text = await response.text()
                    if response.status in statuses:
                        return text
                    last_error = RuntimeError(
                        f"{method} {url} returned unexpected status {response.status}"
                    )
                    self.logger.debug(str(last_error))
                    if not self._should_retry_status(response.status):
                        break
            except (
                aiohttp.ClientError,
                asyncio.TimeoutError,
                RuntimeError,
            ) as exc:
                last_error = exc
                self.logger.debug(f"HTTP attempt {attempt}/{self.retries} failed for {url}: {exc}")

            if attempt < self.retries:
                await asyncio.sleep(self.retry_backoff * attempt)

        raise RuntimeError(f"request failed after {self.retries} attempts: {last_error}")

    @staticmethod
    def _should_retry_status(status_code: int) -> bool:
        # Retry transient server/network-side failures, but do not keep hammering
        # endpoints on client-side errors like auth problems or rate limits.
        if 400 <= status_code < 500 and status_code != 408:
            return False
        return True

    async def get_json(
        self,
        url: str,
        *,
        expected_status: int | set[int] = 200,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> Any:
        text = await self.request(
            "GET",
            url,
            expected_status=expected_status,
            headers=headers,
            params=params,
        )
        return json.loads(text)

    async def request_json(
        self,
        method: str,
        url: str,
        *,
        expected_status: int | set[int] = 200,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        json_body: Any | None = None,
    ) -> Any:
        text = await self.request(
            method,
            url,
            expected_status=expected_status,
            headers=headers,
            params=params,
            json_body=json_body,
        )
        return json.loads(text)

    @staticmethod
    def basic_auth_header(username: str, password: str) -> str:
        token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
        return f"Basic {token}"
