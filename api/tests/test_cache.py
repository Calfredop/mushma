from datetime import timedelta

import pytest

from api.cache import DAILY, SHORT_LIVED, cache_control_for_date
from api.jobs.daily import WINDOW_BACK_DAYS
from api.timeutil import today_rome


class TestCacheControlForDate:
    def test_yesterday_is_short_lived_because_the_daily_job_rescores_it(self) -> None:
        assert cache_control_for_date(today_rome() - timedelta(days=1)) == SHORT_LIVED

    def test_the_first_day_the_job_rescores_is_short_lived(self) -> None:
        first = today_rome() - timedelta(days=WINDOW_BACK_DAYS)
        assert cache_control_for_date(first) == SHORT_LIVED

    def test_an_older_day_is_kept_for_a_day(self) -> None:
        older = today_rome() - timedelta(days=WINDOW_BACK_DAYS + 1)
        assert cache_control_for_date(older) == DAILY
        assert cache_control_for_date(today_rome() - timedelta(days=3000)) == DAILY

    def test_today_is_short_lived(self) -> None:
        assert cache_control_for_date(today_rome()) == SHORT_LIVED

    def test_a_forecast_date_is_short_lived(self) -> None:
        assert cache_control_for_date(today_rome() + timedelta(days=7)) == SHORT_LIVED

    def test_nothing_is_cached_forever(self) -> None:
        assert "immutable" not in DAILY
        assert "immutable" not in SHORT_LIVED
        assert "public" in DAILY
        assert "public" in SHORT_LIVED


@pytest.mark.parametrize("directive", [DAILY, SHORT_LIVED])
def test_directives_declare_a_max_age(directive: str) -> None:
    assert "max-age=" in directive
