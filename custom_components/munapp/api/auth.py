"""Authentication for the MunApp API."""

from __future__ import annotations

from .exceptions import MunAppAuthenticationError


class AuthenticationMixin:
    """Authentication mixin."""

    _token: str | None
    _user_id: int | None
    _username: str
    _password: str
    _session: object

    async def login(self) -> None:
        """Authenticate with MunApp."""

        response = await self._session.post(
            f"{self.BASE_URL}/model/Login",
            json={
                "username": self._username,
                "password": self._password,
            },
        )

        if response.status != 200:
            raise MunAppAuthenticationError(
                f"Login failed ({response.status})"
            )

        data = await response.json()

        self._token = data["ApiAccessToken"]
        self._user_id = data["StdiUsersId"]
