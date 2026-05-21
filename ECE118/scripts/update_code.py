import binascii
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import requests


CLASS_NAME = "ECE118"
DEFAULT_SOURCE_URL = f"https://users.soe.ucsc.edu/~elkaim/ClassZips/{CLASS_NAME}.zip"


def get_target_base() -> Path:
    env_target_dir = os.environ.get("ECE118_TARGET_DIR")
    if env_target_dir:
        return Path(env_target_dir).expanduser()

    env_target_root = os.environ.get("ECE118_TARGET_ROOT")
    if env_target_root:
        return Path(env_target_root).expanduser()

    if os.name == "nt":
        return Path("C:/")

    return Path.home()


def is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def main() -> int:
    source_url = os.environ.get("ECE118_SOURCE_URL", DEFAULT_SOURCE_URL)
    target_base = get_target_base().resolve()
    target_dir = (target_base / CLASS_NAME).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    with requests.get(source_url, stream=True) as response:
        response.raise_for_status()
        response.raw.decode_content = True

        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
            shutil.copyfileobj(response.raw, temp_zip)
            zip_path = Path(temp_zip.name)

    extracted_paths = set()

    try:
        with zipfile.ZipFile(zip_path) as archive:
            for zip_info in archive.infolist():
                relative_path = Path(zip_info.filename)
                if relative_path.is_absolute():
                    print(f"Skipping invalid absolute path: {zip_info.filename}")
                    continue

                destination_path = (target_base / relative_path).resolve()
                if not is_relative_to(destination_path, target_dir):
                    print(f"Skipping unsafe path outside target directory: {zip_info.filename}")
                    continue

                if zip_info.is_dir():
                    destination_path.mkdir(parents=True, exist_ok=True)
                    continue

                extracted_paths.add(destination_path)
                destination_path.parent.mkdir(parents=True, exist_ok=True)

                should_extract = True
                if destination_path.exists():
                    with destination_path.open("rb") as existing_file:
                        should_extract = binascii.crc32(existing_file.read()) != zip_info.CRC

                if should_extract:
                    print(f"updating {destination_path}")
                    with archive.open(zip_info) as source_file, destination_path.open("wb") as dest_file:
                        shutil.copyfileobj(source_file, dest_file)
    finally:
        zip_path.unlink(missing_ok=True)

    for current_path in target_dir.rglob("*"):
        if current_path.is_file() and current_path.resolve() not in extracted_paths:
            print(f"removing stale file {current_path}")
            current_path.unlink()

    for current_path in sorted(target_dir.rglob("*"), reverse=True):
        if current_path.is_dir():
            try:
                current_path.rmdir()
            except OSError:
                pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
