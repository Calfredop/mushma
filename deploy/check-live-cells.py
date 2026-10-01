"""Slow check of the live API across every served region, after a deploy or a re-score.

    uv run --project api python deploy/check-live-cells.py [cells per region]

For each region: /factors for each species, then /cells/{id} for a random sample of its scored
cells (10 by default). One request about every second, so the per-IP rate limiter never answers
429. Prints each region's count of forecast days served without a breakdown (the store had no
usable factor row: the API logs which), then every non-200, and exits 1 if there was any.
API_URL points it somewhere else.
"""

import json
import os
import random
import sys
import time
import urllib.error
import urllib.request

API = os.environ.get("API_URL", "https://api.mappafunghi.app")
PAUSE_S = 1.1


def get(path: str) -> tuple[int, dict | None]:
    time.sleep(PAUSE_S)
    try:
        with urllib.request.urlopen(API + path, timeout=60) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, None


def main() -> int:
    per_region = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    _, regions = get("/regions")
    problems: list[str] = []
    requests = 0
    for region in regions["regions"]:
        rid = region["id"]
        for species in region["species"]:
            code, _ = get(f"/factors?species={species}&region={rid}")
            requests += 1
            if code != 200:
                problems.append(f"{rid} /factors?species={species}: {code}")
        code, scores = get(f"/scores?species=combined&region={rid}")
        if code != 200:
            problems.append(f"{rid} /scores: {code}")
            continue
        cells = [cell["cell_id"] for cell in scores["cells"]]
        sample = random.sample(cells, min(per_region, len(cells)))
        without_breakdown = 0
        for cell_id in sample:
            code, detail = get(f"/cells/{cell_id}?region={rid}")
            requests += 1
            if code != 200:
                problems.append(f"{rid} /cells/{cell_id}: {code}")
                continue
            days = [day for forecast in detail["species"] for day in forecast["days"]]
            without_breakdown += sum(1 for day in days if not day["factors"])
        print(
            f"{rid}: sampled {len(sample)} of {len(cells)} cells, "
            f"{without_breakdown} days without a breakdown",
            flush=True,
        )
    print(f"\n{requests} requests, {len(problems)} not 200")
    print("\n".join(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
