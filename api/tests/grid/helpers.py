import zipfile
from pathlib import Path

import geopandas as gpd


def zip_shapefiles(archive: Path, layers: dict[str, gpd.GeoDataFrame]) -> Path:
    """Write each layer as ``<name>/<name>.shp`` inside one zip, like the ISTAT boundary archive."""
    with zipfile.ZipFile(archive, "w") as zf:
        for name, frame in layers.items():
            folder = archive.parent / f"_{name}"
            folder.mkdir()
            frame.to_file(folder / f"{name}.shp")
            for part in folder.iterdir():
                zf.write(part, f"{name}/{part.name}")
    return archive
