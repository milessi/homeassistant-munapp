"""Binary sensors for MunApp."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .coordinator import MunAppDataUpdateCoordinator
from .entity import MunAppEntity

DAY_PREFIX = {
    0: "Ma",
    1: "Ti",
    2: "Ke",
    3: "To",
    4: "Pe",
    5: "La",
    6: "Su",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensors."""

    data = hass.data[DOMAIN][entry.entry_id]

    coordinator: MunAppDataUpdateCoordinator = data["coordinator"]

    entities: list[MunAppTransportTodayBinarySensor] = []

    for customer in coordinator.data.get("customers", []):
        entities.append(
            MunAppTransportTodayBinarySensor(
                coordinator,
                customer,
            )
        )

    async_add_entities(entities)


class MunAppTransportTodayBinarySensor(
    MunAppEntity,
    BinarySensorEntity,
):
    """Today's transport binary sensor."""

    _attr_device_class = None
    _attr_icon = "mdi:bus-school"

    def __init__(
        self,
        coordinator: MunAppDataUpdateCoordinator,
        customer: dict,
    ) -> None:
        """Initialize binary sensor."""

        super().__init__(coordinator)

        self._customer = customer
        self._customer_id = customer["CustomerRiviId"]

        self._attr_unique_id = (
            f"{self._customer_id}_transport_today"
        )

        self._attr_name = (
            f"{customer['CustomerNameFirst']} Transport Today"
        )

    @property
    def is_on(self) -> bool:
        """Return whether transport exists today."""

        schedules = self.coordinator.data["schedules"].get(
            self._customer_id,
            [],
        )

        if not schedules:
            return False

        week = schedules[0]

        prefix = DAY_PREFIX[
            dt_util.now().weekday()
        ]

        return bool(
            week.get(f"{prefix}KulkeeMeno")
            or week.get(f"{prefix}KulkeePaluu")
        )
