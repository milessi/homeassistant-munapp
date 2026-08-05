"""Base entity for the MunApp integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import MunAppDataUpdateCoordinator


class MunAppEntity(CoordinatorEntity[MunAppDataUpdateCoordinator]):
    """Base entity for MunApp."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MunAppDataUpdateCoordinator,
    ) -> None:
        """Initialize entity."""

        super().__init__(coordinator)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""

        user = self.coordinator.data.get("user", {})

        return DeviceInfo(
            identifiers={(DOMAIN, str(user.get("Id", "unknown")))},
            name="MunApp",
            manufacturer=MANUFACTURER,
            model="School Transport",
            configuration_url="https://munapp.kuntalogistiikka.fi/",
        )
