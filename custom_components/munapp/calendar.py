"""Calendar platform for MunApp."""

from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.calendar import (
    CalendarEntity,
    CalendarEvent,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .coordinator import MunAppDataUpdateCoordinator
from .entity import MunAppEntity
from .transport import get_week_events


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MunApp calendars."""

    data = hass.data[DOMAIN][entry.entry_id]

    coordinator: MunAppDataUpdateCoordinator = data["coordinator"]

    entities: list[MunAppCalendar] = []

    for customer in coordinator.data.get("customers", []):
        entities.append(
            MunAppCalendar(
                coordinator,
                customer,
            )
        )

    async_add_entities(entities)


class MunAppCalendar(
    MunAppEntity,
    CalendarEntity,
):
    """MunApp transport calendar."""

    def __init__(
        self,
        coordinator: MunAppDataUpdateCoordinator,
        customer: dict,
    ) -> None:
        """Initialize calendar."""

        super().__init__(coordinator)

        self._customer = customer
        self._customer_id = customer["CustomerRiviId"]

        self._attr_unique_id = (
            f"{self._customer_id}_calendar"
        )

        self._attr_name = (
            f"{customer['CustomerNameFirst']} School Transport"
        )

        self._event: CalendarEvent | None = None

    @property
    def event(self) -> CalendarEvent | None:
        """Return next calendar event."""

        return self._event

    async def async_update(self) -> None:
        """Update current event."""

        schedules = self.coordinator.data["schedules"].get(
            self._customer_id,
            [],
        )

        events = get_week_events(schedules)

        now = dt_util.now()

        future_events = []

        for event in events:
            start = event["start"]

            if start.tzinfo is None:
                start = start.replace(
                    tzinfo=dt_util.DEFAULT_TIME_ZONE,
                )

            if start >= now:
                future_events.append(
                    (start, event)
                )

        if not future_events:
            self._event = None
            return

        start, event = future_events[0]

        self._event = CalendarEvent(
            summary=(
                f"🚌 {self._customer['CustomerNameFirst']} → "
                f"{'School' if event['direction'] == 'morning' else 'Home'}"
            ),
            start=start,
            end=start + timedelta(minutes=1),
            description=(
                f"Route: {event['route']}\n"
                f"Vehicle: {event['vehicle']}\n"
                f"School: {event['school']}\n"
                f"Address: {event['address']}"
            ),
        )

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return calendar events."""

        schedules = self.coordinator.data["schedules"].get(
            self._customer_id,
            [],
        )

        events = get_week_events(schedules)

        calendar_events: list[CalendarEvent] = []

        for event in events:
            start = event["start"]

            if start.tzinfo is None:
                start = start.replace(
                    tzinfo=dt_util.DEFAULT_TIME_ZONE,
                )

            if start_date <= start <= end_date:
                calendar_events.append(
                    CalendarEvent(
                        summary=(
                            f"🚌 {self._customer['CustomerNameFirst']} → "
                            f"{'School' if event['direction'] == 'morning' else 'Home'}"
                        ),
                        start=start,
                        end=start + timedelta(minutes=1),
                        description=(
                            f"Route: {event['route']}\n"
                            f"Vehicle: {event['vehicle']}\n"
                            f"School: {event['school']}\n"
                            f"Address: {event['address']}"
                        ),
                    )
                )

        return calendar_events
