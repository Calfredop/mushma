"""HTTP cache headers for the read-only, date-scoped endpoints.

Scores and hotspots change at most once a day, when ``api.jobs.daily`` runs. That run re-scores
today -6 to +7 every morning (new reanalysis days replace forecast weather), so every day in that
window gets a short cache. Older days only change when history is re-scored (a finished backfill,
new rules): rare, but real, and replaying any past day is a feature (M6), so they are kept for a
day rather than forever.
"""

from datetime import date, timedelta

from api.jobs.daily import WINDOW_BACK_DAYS
from api.timeutil import today_rome

# 10 minutes: the pipeline runs once a day, so this buys real CDN/browser relief with only a
# short window where a same-day rescore wouldn't show up immediately.
SHORT_LIVED = "public, max-age=600"
# Tables that change at most when something is rebuilt: a past day's or season's scores, the
# comuni list.
DAILY = "public, max-age=86400"


def cache_control_for_date(target_date: date) -> str:
    rescored_from = today_rome() - timedelta(days=WINDOW_BACK_DAYS)
    return DAILY if target_date < rescored_from else SHORT_LIVED
