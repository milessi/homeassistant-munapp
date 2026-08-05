"""MunApp API endpoints."""

from __future__ import annotations

from urllib.parse import quote

from .client import MunAppClient


class MunAppEndpoints(MunAppClient):
    """MunApp endpoint methods."""

    async def get_user(self) -> dict:
        """Return logged in user."""
        return await self.request(
            "GET",
            f"/model/StdiUsers/{self._user_id}",
        )

    async def get_user_groups(self) -> dict:
        """Return user groups."""
        return await self.request(
            "GET",
            f"/model/StdiUserGroups?Uid={self._user_id}",
        )

    async def get_customers(self) -> dict:
        """Return customers."""
        return await self.request(
            "GET",
            "/model/Customer",
        )

    async def get_schedule(
        self,
        customer_id: int,
    ) -> dict:
        """Return schedule for a customer."""

        return await self.request(
            "GET",
            f"/model/MunAppSchedule/{customer_id}",
        )

    async def get_notifications(self) -> dict:
        """Return notifications."""

        return await self.request(
            "GET",
            (
                "/model/MunAppNotification"
                f"?StdiUsersId={self._user_id}"
                "&Deleted=false"
                "&page=0"
                "&pageSize=10"
                "&orderBy=sent"
                "&orderAsc=DESC"
            ),
        )

    async def get_routepoints(
        self,
        reservation_ids: list[str],
        customer_ids: list[int],
    ) -> dict:
        """Return routepoints."""

        reservation_string = ",".join(
            quote(item, safe="")
            for item in reservation_ids
        )

        customer_string = ",".join(
            str(item)
            for item in customer_ids
        )

        return await self.request(
            "GET",
            (
                "/model/VehicleReservationsRoutepoints"
                f"?ReservationsExportSystemIdIn={reservation_string}"
                f"&RoutepointsCustomerRiviIdIn={customer_string}"
            ),
        )

    async def cancel_transport(
        self,
        customer_row_id: int,
        date: str,
        morning: bool,
        schedule_id: int,
        cancellation_notes: str = "",
    ) -> dict:
        """Cancel transport."""

        payload = {
            "CustomerRiviId": customer_row_id,
            "Date": date,
            "MorningOrAfternoon": morning,
            "Enabled": True,
            "CancellationNotes": cancellation_notes,
            "ScheduleId": schedule_id,
        }

        return await self.request(
            "POST",
            "/model/MunschoolMultiScheduleCancel",
            json=payload,
        )

    async def restore_transport(
        self,
        customer_row_id: int,
        date: str,
        morning: bool,
        schedule_id: int,
    ) -> dict:
        """Restore cancelled transport."""

        payload = {
            "CustomerRiviId": customer_row_id,
            "Date": date,
            "MorningOrAfternoon": morning,
            "Enabled": False,
            "ScheduleId": schedule_id,
        }

        endpoint = (
            "/model/MunschoolMultiScheduleCancel/"
            f"{customer_row_id}/"
            f"{quote(date, safe='')}/"
            f"{str(morning).lower()}/"
            f"{schedule_id}"
        )

        return await self.request(
            "PUT",
            endpoint,
            json=payload,
        )
