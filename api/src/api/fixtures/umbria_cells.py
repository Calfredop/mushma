"""Fixture cells for the second served region (Umbria), so tests and the web card can route
between two without real Parquet stores.
"""

from api.fixtures.cells import CellSpec

# A handful of plausible Umbrian woodland spots inside config/regions/umbria.yaml's bbox.
UMBRIA_CELLS: tuple[CellSpec, ...] = (
    CellSpec("1kmN2405E4550", 12.3833, 43.1167, 650, "deciduous_oak", "Perugia", "Monte Tezio"),
    CellSpec("1kmN2410E4560", 12.4500, 43.1500, 800, "beech", "Gubbio", "Monte Ingino"),
    CellSpec("1kmN2395E4575", 12.6167, 43.0500, 550, "chestnut", "Foligno", "Colle San Lorenzo"),
    CellSpec("1kmN2388E4540", 12.3000, 42.9833, 420, "evergreen_oak", "Todi", "Pontenna"),
    CellSpec("1kmN2420E4580", 12.6500, 43.2167, 950, "beech", "Città di Castello", "Monte Acuto"),
    CellSpec("1kmN2375E4565", 12.5000, 42.8500, 700, "deciduous_oak", "Spoleto", "Monteluco"),
)
