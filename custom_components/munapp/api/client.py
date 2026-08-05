"""HTTP client for the MunApp API."""

from __future__ import annotations

from typing import Any

import aiohttp

from ..const import API_BASE
from .auth import AuthenticationMixin
from .exceptions import MunAppApiError


class MunAppClient(AuthenticationMixin):
    """MunApp API client."""

    BASE_URL = API_BASE

    def __init__(
        self,
        session: aiohttp.ClientSession,
        username: str,
        password: str,
    ) -> None:
        """Initialize client."""

        self._session = session
        self._username = username
        self._password = password

        self._token: str | None = None
        self._user_id: int | None = None

    async def request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> Any:
        """Execute authenticated request."""

        if self._token is None:
            await self.login()

        headers = kwargs.pop("headers", {})
        headers["apiAccessToken"] = self._token

        response = await self._session.request(
            method,
            f"{API_BASE}{endpoint}",
            headers=headers,
            **kwargs,
        )

        body = await response.text()

        if response.status >= 400:
            raise MunAppApiError(
                f"{method} {endpoint} failed ({response.status})"
            )

        if response.content_type == "application/json":
            return await response.json()

        return body
