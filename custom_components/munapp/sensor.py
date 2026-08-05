"""Sensor platform for MunApp."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import MunAppDataUpdateCoordinator
from .entity import MunAppEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MunApp sensors."""

    data = hass.data[DOMAIN][entry.entry_id]

    coordinator: MunAppDataUpdateCoordinator = data["coordinator"]

    entities: list[MunAppChildSensor] = []

    customers = coordinator.data.get("customers", [])

    for customer in customers:
        entities.append(
            MunAppChildSensor(
                coordinator,
                customer,
            )
        )

    async_add_entities(entities)


class MunAppChildSensor(MunAppEntity, SensorEntity):
    """Representation of a MunApp child."""

    _attr_icon = "mdi:bus-school"

    def __init__(
        self,
        coordinator: MunAppDataUpdateCoordinator,
        customer: dict,
    ) -> None:
        """Initialize sensor."""

        super().__init__(coordinator)

        self._customer = customer
        self._customer_id = customer["CustomerRiviId"]

        self._attr_unique_id = (
            f"munapp_child_{self._customer_id}"
        )

        self._attr_name = (
            f"{customer['CustomerNameFirst']} Transport"
        )

    @property
    def native_value(self) -> str:
        """Return sensor state."""

        schedules = self.coordinator.data.get("schedules", {})
        schedule = schedules.get(self._customer_id)

        if not schedule:
            return "No transport"

        return "Transport available"

    @property
    def extra_state_attributes(self) -> dict:
        """Return attributes."""

        return {
            "first_name": self._customer["CustomerNameFirst"],
            "last_name": self._customer["CustomerNameLast"],
            "customer_row_id": self._customer["CustomerRiviId"],
            "external_id": self._customer["ExternalId"],
            "phone": self._customer["CustomerPhonenumber"],
        }
