"""Helpers for parsing MunApp transport schedules."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from homeassistant.util import dt as dt_util

DAY_PREFIX = {
    0: "Ma",
    1: "Ti",
    2: "Ke",
    3: "To",
    4: "Pe",
    5: "La",
    6: "Su",
}


def _prefix(day: date) -> str:
    """Return MunApp day prefix."""

    return DAY_PREFIX[day.weekday()]


def _find_week(schedule: list[dict], day: date) -> dict | None:
    """Return the schedule item containing the requested date."""

    iso_week = day.isocalendar().week

    for item in schedule:
        if (
            item.get("Week") == iso_week
            and item.get("Year") == day.year
        ):
            return item

    return None


def get_day_transport(
    schedule: list[dict],
    day: date,
) -> dict | None:
    """Return parsed transport information for one day."""

    week = _find_week(schedule, day)

    if week is None:
        return None

    prefix = _prefix(day)

    customer_row_id = week.get("CustomerRiviId")
    day_date = week.get(f"{prefix}Pvm")

    return {
        "date": day_date,
        "customer_row_id": customer_row_id,
        "student_id": week.get("OppilasId"),
        "morning": {
            "available": week.get(f"{prefix}KulkeeMeno", False),
            "morning": True,
            "date": day_date,
            "customer_row_id": customer_row_id,
            "schedule_id": week.get(f"{prefix}OppilasLukujarjestysId"),
            "pickup": week.get(f"{prefix}Haku"),
            "route": week.get(f"{prefix}MenoReitti"),
            "route_id": week.get(f"{prefix}MenoReittiId"),
            "vehicle": week.get(f"{prefix}ApAuto"),
            "school": week.get(f"{prefix}ApKohdeKoulu"),
            "address": week.get(f"{prefix}ApOsoite"),
            "reservation_id": week.get(f"{prefix}ApReittiTunniste"),
        },
        "afternoon": {
            "available": week.get(f"{prefix}KulkeePaluu", False),
            "morning": False,
            "date": day_date,
            "customer_row_id": customer_row_id,
            "schedule_id": week.get(f"{prefix}OppilasLukujarjestysId"),
            "departure": week.get(f"{prefix}IpLahtoaika"),
            "arrival": week.get(f"{prefix}IpArvioituSaapumisAika"),
            "route": week.get(f"{prefix}PaluuReitti"),
            "route_id": week.get(f"{prefix}PaluuReittiId"),
            "vehicle": week.get(f"{prefix}IpAuto"),
            "school": week.get(f"{prefix}IpNoutoKoulu"),
            "address": week.get(f"{prefix}IpOsoite"),
            "reservation_id": week.get(f"{prefix}IpReittiTunniste"),
        },
    }


def get_today(schedule: list[dict]) -> dict | None:
    """Return today's transport."""

    return get_day_transport(
        schedule,
        dt_util.now().date(),
    )


def get_tomorrow(schedule: list[dict]) -> dict | None:
    """Return tomorrow's transport."""

    return get_day_transport(
        schedule,
        dt_util.now().date() + timedelta(days=1),
    )


def get_week_events(
    schedule: list[dict],
) -> list[dict]:
    """Return all transport events from the schedule."""

    events: list[dict] = []

    for week in schedule:
        for prefix in DAY_PREFIX.values():
            day_date = week.get(f"{prefix}Pvm")

            if not day_date:
                continue

            if week.get(f"{prefix}KulkeeMeno"):
                pickup = week.get(f"{prefix}Haku")

                if pickup:
                    events.append(
                        {
                            "summary": "School Transport → School",
                            "direction": "morning",
                            "start": datetime.fromisoformat(
                                f"{day_date[:10]}T{pickup}"
                            ),
                            "route": week.get(f"{prefix}MenoReitti"),
                            "vehicle": week.get(f"{prefix}ApAuto"),
                            "school": week.get(f"{prefix}ApKohdeKoulu"),
                            "address": week.get(f"{prefix}ApOsoite"),
                        }
                    )

            if week.get(f"{prefix}KulkeePaluu"):
                departure = week.get(f"{prefix}IpLahtoaika")

                if departure:
                    events.append(
                        {
                            "summary": "School Transport → Home",
                            "direction": "afternoon",
                            "start": datetime.fromisoformat(
                                f"{day_date[:10]}T{departure}"
                            ),
                            "route": week.get(f"{prefix}PaluuReitti"),
                            "vehicle": week.get(f"{prefix}IpAuto"),
                            "school": week.get(f"{prefix}IpNoutoKoulu"),
                            "address": week.get(f"{prefix}IpOsoite"),
                        }
                    )

    return sorted(
        events,
        key=lambda event: event["start"],
    )
