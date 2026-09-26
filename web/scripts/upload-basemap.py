#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["boto3"]
# ///
"""Uploads the basemap extracts to the R2 bucket behind tiles.mappafunghi.app (README → Deploying).

    uv run scripts/upload-basemap.py            # data/basemap/italy{,-terrain}.pmtiles
    uv run scripts/upload-basemap.py FILE ...   # other extracts, each under its own file name

`wrangler r2 object put` stops at 300 MiB and italy.pmtiles is 2.2 GiB, so this goes through R2's
S3 API in 64 MiB parts instead. It needs an R2 API token with Object Read & Write on the bucket
in the environment, never printed: R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY and R2_ENDPOINT
(https://<account id>.r2.cloudflarestorage.com). R2_BUCKET overrides the bucket (mushma-tiles).
Each upload is checked against the local file's size afterwards.
"""

import argparse
import os
import sys
import threading
import time
from pathlib import Path

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.config import Config

WEB = Path(__file__).resolve().parent.parent
DEFAULT_FILES = [WEB / "data/basemap/italy.pmtiles", WEB / "data/basemap/italy-terrain.pmtiles"]
PART = 64 * 1024 * 1024
CREDENTIALS = ("R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_ENDPOINT")


class Progress:
    """Prints every 10 % of one file, from the transfer's worker threads."""

    def __init__(self, name: str, size: int) -> None:
        self.name, self.size, self.sent, self.next_step = name, size, 0, 0
        self.start = time.monotonic()
        self.lock = threading.Lock()

    def __call__(self, sent: int) -> None:
        with self.lock:
            self.sent += sent
            percent = self.sent * 100 // self.size
            if percent >= self.next_step:
                rate = self.sent / max(time.monotonic() - self.start, 1) / 1e6
                print(f"  {self.name}: {percent}% ({rate:.1f} MB/s)", flush=True)
                self.next_step = percent - percent % 10 + 10


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="*", type=Path, default=DEFAULT_FILES)
    args = parser.parse_args()

    missing = [name for name in CREDENTIALS if not os.environ.get(name)]
    if missing:
        sys.exit(f"set {', '.join(missing)} (an R2 API token: README → Deploying → Basemap)")
    for path in args.files:
        if not path.is_file():
            sys.exit(f"no such file: {path} (run scripts/extract-basemap.sh first)")

    bucket = os.environ.get("R2_BUCKET", "mushma-tiles")
    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ["R2_ENDPOINT"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
        config=Config(
            retries={"max_attempts": 10, "mode": "standard"},
            # R2 takes the classic MD5-free multipart upload; newer boto3 checksums are optional.
            request_checksum_calculation="when_required",
            response_checksum_validation="when_required",
        ),
    )
    transfer = TransferConfig(multipart_threshold=PART, multipart_chunksize=PART, max_concurrency=4)

    for path in args.files:
        size = path.stat().st_size
        print(f"{path.name} ({size / 1e6:.0f} MB) -> {bucket}/{path.name}", flush=True)
        progress = Progress(path.name, size)
        s3.upload_file(str(path), bucket, path.name, Config=transfer, Callback=progress)
        remote = s3.head_object(Bucket=bucket, Key=path.name)["ContentLength"]
        if remote != size:
            sys.exit(f"{path.name}: R2 has {remote} bytes, the local file {size}")
        print(f"  {path.name}: uploaded, {remote} bytes as on disk", flush=True)


if __name__ == "__main__":
    main()
