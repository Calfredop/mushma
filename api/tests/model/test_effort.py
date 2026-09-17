from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from api.model.effort import FUNGI_TAXON_ID, daily_effort, histogram_url


class FakeClient:
    def __init__(self) -> None:
        self.urls: list[str] = []

    def get(self, url: str) -> dict:
        self.urls.append(url)
        year = parse_qs(urlparse(url).query)["d1"][0][:4]
        return {"results": {"day": {f"{year}-09-01": 4, f"{year}-09-02": 0, f"{year}-09-03": 7}}}


def test_the_histogram_asks_for_verifiable_fungi_observed_per_day_in_the_place() -> None:
    query = parse_qs(urlparse(histogram_url(13073, 2020)).query)

    assert query["taxon_id"] == [str(FUNGI_TAXON_ID)]
    assert query["place_id"] == ["13073"]
    assert (query["d1"], query["d2"]) == (["2020-01-01"], ["2020-12-31"])
    assert (query["interval"], query["date_field"]) == (["day"], ["observed"])
    assert query["verifiable"] == ["true"]


def test_daily_effort_reads_each_year_once_and_fills_missing_days_with_zero(
    tmp_path: Path,
) -> None:
    client = FakeClient()

    effort = daily_effort(client, 13073, [2020, 2021], tmp_path)
    again = daily_effort(client, 13073, [2020, 2021], tmp_path)

    assert len(client.urls) == 2
    assert effort[date(2020, 9, 3)] == 7
    assert effort[date(2021, 9, 2)] == 0
    assert effort[date(2020, 1, 1)] == 0
    assert len(effort) == 366 + 365
    assert again.equals(effort)
