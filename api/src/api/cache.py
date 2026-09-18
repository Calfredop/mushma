"""HTTP cache headers for the read-only, date-scoped endpoints (M4-api.md: "past dates immutable,
today and forecast short-lived"). Scores and hotspots change at most once a day, when
``api.jobs.daily`` runs -- a past date's response never changes again, so browsers and CDNs can
cache it forever; today's and the forecast's can still be rescored by a later run that day, so
they get a short cache instead.
"""

from datetime import date

from api.timeutil import today_rome

IMMUTABLE = "public, max-age=31536000, immutable"
# 10 minutes: the pipeline runs once a day, so this buys real CDN/browser relief with only a
# short window where a same-day rescore wouldn't show up immediately.
SHORT_LIVED = "public, max-age=600"


def cache_control_for_date(target_date: date) -> str:
    return IMMUTABLE if target_date < today_rome() else SHORT_LIVED
