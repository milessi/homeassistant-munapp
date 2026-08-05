"""Data models for MunApp."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Customer:
    """Customer (child)."""

    id: int
    name: str


@dataclass(slots=True)
class Transport:
    """Single transport."""

    reservation_id: int
    customer_id: int
    date: datetime
    pickup_time: str | None
    destination: str | None
    cancelled: bool
