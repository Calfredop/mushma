from pathlib import Path

import pytest

from api.history.config import HistoryConfigError, load_history_config, rain_lead_days
from api.model.rules import load_rules
from tests.live.helpers import factor, ruleset, species_rules


def test_the_shipped_config_loads_and_cites_known_references() -> None:
    config = load_history_config()

    assert 0 < config.good_score <= 1
    assert 0 < config.plausible_fit <= 1
    assert config.baseline.start_year <= config.baseline.end_year
    assert config.outlook.rain.drier_pct < 100 < config.outlook.rain.wetter_pct
    assert config.normals.window_days % 2 == 1


def test_the_baseline_lists_its_years() -> None:
    config = load_history_config()

    years = config.baseline.years

    assert years[0] == config.baseline.start_year
    assert years[-1] == config.baseline.end_year


def test_an_unknown_reference_is_rejected(tmp_path: Path) -> None:
    text = Path(load_history_config.__defaults__[0]).read_text()
    broken = tmp_path / "history.yaml"
    broken.write_text(text.replace("source: [", "source: [no_such_reference, ", 1))

    with pytest.raises(HistoryConfigError, match="no_such_reference"):
        load_history_config(broken)


def _rain_event(lag: list[int], id: str = "rain_trigger"):
    return factor(
        id,
        "driver",
        weight=1.0,
        kind="rain_event",
        input={"variable": "precipitation_sum", "accumulation_days": 3},
        response={"amount_mm": [10, 30, None, None], "lag_days": lag},
    )


def test_the_rain_lead_is_the_plateau_of_the_groups_rain_event_lags() -> None:
    rules = ruleset(
        {
            "a": species_rules("a", "porcini", [_rain_event([6, 10, 16, 24])]),
            "b": species_rules("b", "porcini", [_rain_event([4, 8, 12, 20])]),
        },
        groups={"porcini": ["a", "b"]},
    )

    assert rain_lead_days(rules, ["a", "b"]) == (8, 16)


def test_the_real_rules_give_every_group_a_rain_lead() -> None:
    rules = load_rules()

    for keys in rules.groups.values():
        low, high = rain_lead_days(rules, keys)
        assert 0 <= low <= high
