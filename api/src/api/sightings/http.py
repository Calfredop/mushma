"""HTTP helper shared by the GBIF and iNaturalist clients: retries with backoff, and a per-page
JSON cache with a completion marker so a paged fetch resumes without re-asking pages it already
has (mirrors ``api.grid.sources.fetch_arcgis_features``)."""

import json
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

USER_AGENT = "mushma-sightings/0.1"


@dataclass
class JsonClient:
    sleep: Callable[[float], None] = time.sleep
    retries: int = 4
    backoff_s: float = 2.0
    timeout_s: float = 30.0

    def get(self, url: str) -> dict:
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        failures = 0
        while True:
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
                    return json.loads(response.read())
            except urllib.error.HTTPError as error:
                retryable = error.code == 429 or error.code >= 500
                if not retryable or failures >= self.retries:
                    raise ValueError(f"{url} -> {error.code} {error.reason}") from error
            except (urllib.error.URLError, TimeoutError) as error:
                if failures >= self.retries:
                    raise ValueError(f"{url} -> {error}") from error
            self.sleep(self.backoff_s * 2**failures)
            failures += 1


def fetch_pages(
    client: JsonClient,
    url_for_offset: Callable[[int], str],
    cache_dir: Path,
    page_size: int,
    is_last_page: Callable[[dict], bool],
) -> list[dict]:
    """Page through an offset-paginated API, caching each page under ``cache_dir``. Safe to
    re-run: pages already on disk are not re-fetched, and a ``.complete`` marker skips the scan
    once every page has been seen."""
    marker = cache_dir / ".complete"
    if marker.exists():
        return _cached_pages(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    pages, offset = [], 0
    while True:
        page_path = cache_dir / f"page_{offset:07d}.json"
        if page_path.exists():
            payload = json.loads(page_path.read_text())
        else:
            payload = client.get(url_for_offset(offset))
            partial = page_path.with_name(page_path.name + ".part")
            partial.write_text(json.dumps(payload))
            partial.replace(page_path)
        pages.append(payload)
        offset += page_size
        if is_last_page(payload):
            break
    marker.touch()
    return pages


def _cached_pages(cache_dir: Path) -> list[dict]:
    paths = sorted(cache_dir.glob("page_*.json"), key=lambda p: int(p.stem.split("_")[1]))
    return [json.loads(p.read_text()) for p in paths]
