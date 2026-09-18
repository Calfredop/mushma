"""Hand-picked fixture cells across real Tuscan forest areas.

Not the M2 woodland grid (no real EPSG:3035 projection, no forest survey) --
just enough named, geographically plausible cells for the map, spot panel,
"why" breakdown and hotspots to have something real-looking to show. `cell_id`
is illustrative EEA-grid-style (`1kmN<northing_km>E<easting_km>`); the real
ids come from M2.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CellSpec:
    id: str
    lon: float
    lat: float
    elevation_m: float
    habitat: str
    comune: str
    nearest_place: str


CELLS: tuple[CellSpec, ...] = (
    CellSpec("1kmN2438E4372", 11.7333, 43.8500, 850, "fir_spruce", "Poppi", "Camaldoli"),
    CellSpec("1kmN2441E4375", 11.7167, 43.8667, 1100, "beech", "Poppi", "Eremo di Camaldoli"),
    CellSpec("1kmN2435E4368", 11.7667, 43.8167, 720, "chestnut", "Bibbiena", "Serravalle"),
    CellSpec("1kmN2432E4362", 11.8000, 43.7167, 980, "beech", "Chiusi della Verna", "La Verna"),
    CellSpec(
        "1kmN2444E4370",
        11.6667,
        43.9000,
        1250,
        "fir_spruce",
        "Pratovecchio Stia",
        "Monte Falterona",
    ),
    CellSpec(
        "1kmN2447E4373", 11.6500, 43.9167, 1450, "beech", "Pratovecchio Stia", "Lago degli Idoli"
    ),
    CellSpec(
        "1kmN2455E4358", 11.5000, 44.0000, 650, "chestnut", "San Godenzo", "Castagno d'Andrea"
    ),
    CellSpec(
        "1kmN2458E4350", 11.4333, 44.0167, 800, "mixed_broadleaf_conifer", "Marradi", "Popolano"
    ),
    CellSpec(
        "1kmN2461E4345", 11.3833, 44.0500, 550, "chestnut", "Palazzuolo sul Senio", "Bordignano"
    ),
    CellSpec("1kmN2418E4368", 11.7667, 43.6333, 1050, "fir_spruce", "Reggello", "Vallombrosa"),
    CellSpec("1kmN2415E4363", 11.7167, 43.6167, 700, "chestnut", "Reggello", "Saltino"),
    CellSpec("1kmN2352E4285", 11.0000, 42.8833, 1100, "chestnut", "Piancastagnaio", "Monte Amiata"),
    CellSpec("1kmN2349E4288", 11.0333, 42.8667, 1450, "beech", "Santa Fiora", "Vetta Amiata"),
    CellSpec("1kmN2355E4280", 10.9500, 42.9000, 850, "chestnut", "Arcidosso", "Bagnolo"),
    CellSpec(
        "1kmN2358E4275", 10.9000, 42.9167, 600, "mixed_broadleaf", "Castel del Piano", "Montenero"
    ),
    CellSpec("1kmN2361E4290", 11.0500, 42.9333, 950, "chestnut", "Seggiano", "Pescina"),
    CellSpec("1kmN2472E4245", 10.5167, 44.1167, 1150, "beech", "Fivizzano", "Sassalbo"),
    CellSpec("1kmN2469E4240", 10.4667, 44.1000, 850, "chestnut", "Careggine", "Vagli di Sotto"),
    CellSpec(
        "1kmN2475E4248",
        10.5500,
        44.1333,
        1550,
        "fir_spruce",
        "Sillano Giuncugnano",
        "Passo delle Radici",
    ),
    CellSpec("1kmN2465E4252", 10.6000, 44.0667, 700, "chestnut", "Camporgiano", "Casciana"),
    CellSpec("1kmN2405E4260", 10.9167, 43.5333, 950, "fir_spruce", "Abetone Cutigliano", "Abetone"),
    CellSpec("1kmN2402E4258", 10.9333, 43.5167, 700, "beech", "San Marcello Piteglio", "Gavinana"),
    CellSpec(
        "1kmN2378E4318", 11.4000, 43.4667, 480, "deciduous_oak", "Radda in Chianti", "Volpaia"
    ),
    CellSpec(
        "1kmN2375E4322", 11.4333, 43.4500, 420, "evergreen_oak", "Gaiole in Chianti", "Vertine"
    ),
    CellSpec(
        "1kmN2380E4315",
        11.3667,
        43.5000,
        380,
        "deciduous_oak",
        "Castellina in Chianti",
        "Fonterutoli",
    ),
    CellSpec("1kmN2368E4300", 11.2000, 43.3833, 550, "deciduous_oak", "Montalcino", "Sant'Antimo"),
    CellSpec("1kmN2371E4293", 11.1333, 43.4167, 750, "deciduous_oak", "Radicofani", "Le Briccole"),
    CellSpec("1kmN2374E4288", 11.0833, 43.4333, 550, "deciduous_oak", "Sarteano", "Bagno Grande"),
    CellSpec(
        "1kmN2400E4245",
        10.7833,
        42.9167,
        120,
        "mediterranean_pine",
        "Castiglione della Pescaia",
        "Pineta del Tombolo",
    ),
    CellSpec("1kmN2398E4250", 10.8333, 42.9333, 60, "macchia", "Follonica", "Puntone"),
    CellSpec(
        "1kmN2390E4260", 10.9333, 42.9833, 380, "evergreen_oak", "Massa Marittima", "Poggio Diavolo"
    ),
    CellSpec(
        "1kmN2384E4248",
        10.8167,
        43.0500,
        300,
        "mediterranean_pine",
        "Sassetta",
        "Poggio Frassinaio",
    ),
    CellSpec(
        "1kmN2340E4180",
        10.3167,
        42.7833,
        200,
        "evergreen_oak",
        "Portoferraio",
        "Monte Capanne (bassa)",
    ),
    CellSpec(
        "1kmN2336E4178", 10.2000, 42.7500, 700, "mediterranean_pine", "Capoliveri", "Monte Calamita"
    ),
)
