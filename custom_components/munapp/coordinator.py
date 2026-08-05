"""Data update coordinator for MunApp."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .api import MunAppEndpoints
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class MunAppDataUpdateCoordinator(DataUpdateCoordinator):
    """MunApp data coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: MunAppEndpoints,
    ) -> None:
        """Initialize coordinator."""

        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )

        self.api = api

    async def _async_update_data(self) -> dict:
        """Fetch data from MunApp."""

        try:
            user = await self.api.get_user()

            groups = await self.api.get_user_groups()

            customers_response = await self.api.get_customers()
            customers = customers_response.get("items", [])

            notifications = await self.api.get_notifications()

            schedules: dict[int, list] = {}

            reservation_ids: list[str] = []
            customer_row_ids: list[int] = []

            for customer in customers:
                customer_row_id = customer["CustomerRiviId"]

                schedule_response = await self.api.get_schedule(
                    customer_row_id,
                )

                items = schedule_response.get("items", [])

                schedules[customer_row_id] = items

                customer_row_ids.append(customer_row_id)

                for week in items:
                    for key, value in week.items():
                        if (
                            key.endswith(
                                (
                                    "ApReittiTunniste",
                                    "IpReittiTunniste",
                                )
                            )
                            and value
                        ):
                            reservation_ids.append(value)

            reservation_ids = list(dict.fromkeys(reservation_ids))
            customer_row_ids = list(dict.fromkeys(customer_row_ids))

            routepoints = []

            if reservation_ids:
                routepoints = await self.api.get_routepoints(
                    reservation_ids,
                    customer_row_ids,
                )

            return {
                "user": user,
                "groups": groups,
                "customers": customers,
                "notifications": notifications,
                "routepoints": routepoints,
                "schedules": schedules,
            }

        except Exception:
            _LOGGER.exception("MunApp update failed")
            raise
