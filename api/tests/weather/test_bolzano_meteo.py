import zipfile
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

import pytest

from api.weather.bolzano_meteo import PACKAGE_URL, parse_resources, parse_workbook, read_network

SHEET_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def workbook(path: Path, rows: dict[int, dict[str, str | float]]) -> Path:
    """A one-sheet xlsx: strings go through the shared-strings table, numbers inline."""
    strings: list[str] = []
    cells_xml = []
    for number, cells in sorted(rows.items()):
        cells_out = []
        for column, value in cells.items():
            ref = f"{column}{number}"
            if isinstance(value, str):
                strings.append(value)
                cells_out.append(f'<c r="{ref}" t="s"><v>{len(strings) - 1}</v></c>')
            else:
                cells_out.append(f'<c r="{ref}"><v>{value}</v></c>')
        cells_xml.append(f'<row r="{number}">{"".join(cells_out)}</row>')
    sheet = f'<worksheet xmlns="{SHEET_NS}"><sheetData>{"".join(cells_xml)}</sheetData></worksheet>'
    shared = (
        f'<sst xmlns="{SHEET_NS}">'
        + "".join(f"<si><t>{escape(s)}</t></si>" for s in strings)
        + "</sst>"
    )
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("xl/worksheets/sheet1.xml", sheet)
        zf.writestr("xl/sharedStrings.xml", shared)
    return path


def brunico(path: Path) -> Path:
    return workbook(
        path,
        {
            8: {"B": "Station / stazione", "C": "BRUNECK / BRUNICO", "H": "x: 723674"},
            9: {"B": "Nr. / cod.", "C": "59700MS", "H": "y: 5187588"},
            10: {"B": "erstellt am\ncreato il", "C": "23.01.2025", "H": 829},
            13: {"C": "Datum\nData", "D": "Niederschlag\nPrecipitazione\n[mm]\n09:00 - 09:00"},
            14: {"D": "sum", "E": "min", "F": "max"},
            15: {"C": "01.01.1981", "D": "---", "E": "---", "F": "---"},
            16: {"C": "29.12.2024", "D": 12.4, "E": -8.4, "F": 4},
            17: {"C": "30.12.2024", "D": 0, "E": -8.8, "F": 3.3},
            18: {"C": "31.12.2024", "D": "0.6", "E": -9.8, "F": 2.5},
            19: {"C": "dd/mm/yyyy", "D": "valueN", "E": "value_Tmin", "F": "value_Tmax"},
        },
    )


def test_parse_workbook_reads_the_station_and_its_daily_rain(tmp_path: Path) -> None:
    station, rain = parse_workbook(brunico(tmp_path / "59700MS.xlsx"))

    assert station["code"] == "59700MS"
    assert station["name"] == "BRUNECK / BRUNICO"
    assert station["elevation_m"] == 829
    assert station["lon"] == pytest.approx(11.9315, abs=1e-3)
    assert station["lat"] == pytest.approx(46.8043, abs=1e-3)
    assert rain.to_dict() == {
        date(2024, 12, 29): 12.4,
        date(2024, 12, 30): 0.0,
        date(2024, 12, 31): 0.6,
    }


def test_parse_workbook_skips_a_negative_or_unreadable_value(tmp_path: Path) -> None:
    path = workbook(
        tmp_path / "x.xlsx",
        {
            8: {"C": "X / Y", "H": "x: 680000"},
            9: {"C": "1MS", "H": "y: 5150000"},
            10: {"H": 250},
            15: {"C": "01.06.2024", "D": -1},
            16: {"C": "02.06.2024", "D": "n.d."},
            17: {"C": "03.06.2024", "D": 3.2},
        },
    )

    _, rain = parse_workbook(path)

    assert rain.to_dict() == {date(2024, 6, 3): 3.2}


def test_parse_resources_lists_the_station_workbooks() -> None:
    package = {
        "result": {
            "resources": [
                {
                    "name": "Brunico",
                    "format": "XLSX",
                    "url": "http://www.provinz.bz.it/wetter/download/59700MS-Bruneck-Brunico-"
                    "multiannual-LT-N-daily-temperature-precipitation.xlsx",
                },
                {"name": "Readme", "format": "PDF", "url": "http://example.org/readme.pdf"},
            ]
        }
    }

    assert parse_resources(package) == [
        (
            "59700MS",
            "https://www.provinz.bz.it/wetter/download/59700MS-Bruneck-Brunico-"
            "multiannual-LT-N-daily-temperature-precipitation.xlsx",
        )
    ]


def test_read_network_skips_a_station_whose_link_is_dead(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A dead link lands on the weather site's 404 page (HTML), not a workbook; a mangled one
    is refused outright."""
    import json
    import urllib.error

    base = "https://www.provinz.bz.it/wetter/download/"
    package = {
        "result": {
            "resources": [
                {"url": f"{base}59700MS-Bruneck-Brunico-x.xlsx"},
                {"url": f"{base}39100MS-Brixen-Vahrn-x.xlsx"},
                {"url": f"{base}56900MS-M%C2%81hlen-x.xlsx"},
            ]
        }
    }
    files = {
        PACKAGE_URL: lambda dest: dest.write_text(json.dumps(package)),
        f"{base}59700MS-Bruneck-Brunico-x.xlsx": lambda dest: brunico(dest),
        f"{base}39100MS-Brixen-Vahrn-x.xlsx": lambda dest: dest.write_text("<!DOCTYPE html>"),
    }

    def fake_fetch(url: str, dest: Path) -> Path:
        if "%C2%81" in url:  # the portal's own mangled "Mühlen": the server answers 400
            raise urllib.error.HTTPError(url, 400, "Bad Request", None, None)
        dest.parent.mkdir(parents=True, exist_ok=True)
        files[url](dest)
        return dest

    gauges, series = read_network(tmp_path / "bz", fake_fetch)

    assert list(gauges["code"]) == ["59700MS"]
    assert list(series) == ["59700MS"]
    out = capsys.readouterr().out
    assert "39100MS" in out
    assert "56900MS" in out
