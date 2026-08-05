"""Switch platform for MunApp."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import MunAppEndpoints
from .const import DOMAIN
from .coordinator import MunAppDataUpdateCoordinator
from .entity import MunAppEntity
from .transport import get_today, get_tomorrow

ORDER = [
    ("today", "morning"),
    ("today", "afternoon"),
    ("tomorrow", "morning"),
    ("tomorrow", "afternoon"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MunApp switches."""

    data = hass.data[DOMAIN][entry.entry_id]

    coordinator: MunAppDataUpdateCoordinator = data["coordinator"]
    api: MunAppEndpoints = data["api"]

    entities: list[MunAppTransportSwitch] = []

    for customer in coordinator.data.get("customers", []):
        for day, direction in ORDER:
            entities.append(
                MunAppTransportSwitch(
                    coordinator,
                    api,
                    customer,
                    day,
                    direction,
                )
            )

    async_add_entities(entities)


class MunAppTransportSwitch(MunAppEntity, SwitchEntity):
    """Representation of a transport switch."""

    _attr_icon = "mdi:bus-school"

    def __init__(
        self,
        coordinator: MunAppDataUpdateCoordinator,
        api: MunAppEndpoints,
        customer: dict,
        day: str,
        direction: str,
    ) -> None:
        """Initialize switch."""

        super().__init__(coordinator)

        self._api = api
        self._customer = customer
        self._customer_row_id = customer["CustomerRiviId"]
        self._day = day
        self._direction = direction

        self._attr_unique_id = (
            f"munapp_{self._customer_row_id}_{day}_{direction}"
        )

        self._attr_name = (
            f"{customer['CustomerNameFirst']} "
            f"{day.capitalize()} "
            f"{direction.capitalize()} Transport"
        )

    @property
    def is_on(self) -> bool:
        """Return True if transport is enabled."""

        schedules = self.coordinator.data.get("schedules", {})
        schedule = schedules.get(self._customer_row_id, [])

        transport = (
            get_today(schedule)
            if self._day == "today"
            else get_tomorrow(schedule)
        )

        if transport is None:
            return False

        return transport[self._direction]["available"]

    async def async_turn_off(self, **kwargs) -> None:
        """Cancel transport."""

        schedules = self.coordinator.data.get("schedules", {})
        schedule = schedules.get(self._customer_row_id, [])

        transport = (
            get_today(schedule)
            if self._day == "today"
            else get_tomorrow(schedule)
        )

        if transport is None:
            return

        info = transport[self._direction]

        await self._api.cancel_transport(
            customer_row_id=info["customer_row_id"],
            date=info["date"],
            morning=info["morning"],
            schedule_id=info["schedule_id"],
        )

        await self.coordinator.async_request_refresh()

    async def async_turn_on(self, **kwargs) -> None:
        """Restore transport."""

        schedules = self.coordinator.data.get("schedules", {})
        schedule = schedules.get(self._customer_row_id, [])

        transport = (
            get_today(schedule)
            if self._day == "today"
            else get_tomorrow(schedule)
        )

        if transport is None:
            return

        info = transport[self._direction]

        await self._api.restore_transport(
            customer_row_id=info["customer_row_id"],
            date=info["date"],
            morning=info["morning"],
            schedule_id=info["schedule_id"],
        )

        await self.coordinator.async_request_refresh()
