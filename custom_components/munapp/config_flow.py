"""Config flow for the MunApp integration."""

from __future__ import annotations

from asyncio import TimeoutError

import voluptuous as vol
from aiohttp import ClientError
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MunAppEndpoints
from .api.exceptions import (
    MunAppApiError,
    MunAppAuthenticationError,
)
from .const import DOMAIN


class MunAppConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MunApp."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors: dict[str, str] = {}

        if user_input is not None:
            session = async_get_clientsession(self.hass)

            api = MunAppEndpoints(
                session=session,
                username=user_input[CONF_USERNAME],
                password=user_input[CONF_PASSWORD],
            )

            try:
                await api.login()
            except MunAppAuthenticationError:
                errors["base"] = "invalid_auth"
            except (
                ClientError,
                TimeoutError,
                MunAppApiError,
            ):
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(str(api._user_id))
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"MunApp ({api._user_id})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )
