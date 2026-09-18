from typing import Literal

Species = Literal["porcini", "ovoli", "gallinacci"]
SPECIES: tuple[Species, ...] = ("porcini", "ovoli", "gallinacci")

SpeciesOrCombined = Literal["porcini", "ovoli", "gallinacci", "combined"]
