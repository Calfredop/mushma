import zipfile
from pathlib import Path

import geopandas as gpd


def zip_shapefiles(
    archive: Path, layers: dict[str, gpd.GeoDataFrame], without_cpg: bool = False
) -> Path:
    """Write each layer as ``<name>/<name>.shp`` inside one zip, like the ISTAT boundary archive.

    ``without_cpg`` drops the ``.cpg`` sidecar GDAL writes alongside a UTF-8 shapefile, like the
    real ISTAT archives: the DBF bytes are UTF-8 but nothing declares it, so a reader that assumes
    the shapefile default (Latin-1-ish) mangles any accented character.
    """
    with zipfile.ZipFile(archive, "w") as zf:
        for name, frame in layers.items():
            folder = archive.parent / f"_{name}"
            folder.mkdir()
            frame.to_file(folder / f"{name}.shp", encoding="utf-8")
            for part in folder.iterdir():
                if without_cpg and part.suffix == ".cpg":
                    continue
                zf.write(part, f"{name}/{part.name}")
    return archive
