from datetime import timedelta

import pytest

from api.cache import IMMUTABLE, SHORT_LIVED, cache_control_for_date
from api.timeutil import today_rome


class TestCacheControlForDate:
    def test_a_past_date_is_immutable(self) -> None:
        assert cache_control_for_date(today_rome() - timedelta(days=1)) == IMMUTABLE

    def test_a_far_past_date_is_immutable(self) -> None:
        assert cache_control_for_date(today_rome() - timedelta(days=3000)) == IMMUTABLE

    def test_today_is_short_lived(self) -> None:
        assert cache_control_for_date(today_rome()) == SHORT_LIVED

    def test_a_forecast_date_is_short_lived(self) -> None:
        assert cache_control_for_date(today_rome() + timedelta(days=7)) == SHORT_LIVED

    def test_immutable_and_short_lived_are_distinct_public_directives(self) -> None:
        assert "immutable" in IMMUTABLE
        assert "immutable" not in SHORT_LIVED
        assert "public" in IMMUTABLE
        assert "public" in SHORT_LIVED


@pytest.mark.parametrize("directive", [IMMUTABLE, SHORT_LIVED])
def test_directives_declare_a_max_age(directive: str) -> None:
    assert "max-age=" in directive
