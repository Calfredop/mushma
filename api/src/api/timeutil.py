"""Europe/Rome date helpers (AGENTS.md: dates are always Europe/Rome local days)."""

from datetime import date, datetime
from zoneinfo import ZoneInfo

ROME_TZ = ZoneInfo("Europe/Rome")


def today_rome() -> date:
    return datetime.now(ROME_TZ).date()
