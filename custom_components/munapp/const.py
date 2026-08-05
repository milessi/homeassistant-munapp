"""Constants for the MunApp integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "munapp"
NAME = "MunApp School Transport"

MANUFACTURER = "Kuntalogistiikka"

API_BASE = "https://intra.kuntalogistiikka.fi/api/MunAppAPI/v1"

DEFAULT_SCAN_INTERVAL = timedelta(minutes=30)

CONF_USERNAME = "username"
CONF_PASSWORD = "password"

PLATFORMS: list[str] = [
    "sensor",
    "binary_sensor",
    "button",
    "switch",
    "calendar",
]

LOGIN_ENDPOINT = "/model/Login"
CUSTOMERS_ENDPOINT = "/model/Customer"
SCHEDULE_ENDPOINT = "/model/MunAppSchedule"
NOTIFICATIONS_ENDPOINT = "/model/MunAppNotification"
ROUTEPOINTS_ENDPOINT = "/model/VehicleReservationsRoutepoints"
USER_ENDPOINT = "/model/StdiUsers"
USER_GROUPS_ENDPOINT = "/model/StdiUserGroups"

CANCEL_ENDPOINT = "/model/MunschoolMultiScheduleCancel"
REMOVE_CANCEL_ENDPOINT = "/model/MunschoolMultiScheduleRemoveCancel"
