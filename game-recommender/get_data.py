from __future__ import annotations
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import requests


DATA_DIR = Path(__file__).parent.resolve() / 'data'
assert DATA_DIR.exists(), f"Path not a directory: '{DATA_DIR}'"

STEAM_200K_URL = 'https://www.kaggle.com/api/v1/datasets/download/tamber/steam-video-games'
STEAM_INSIGHTS_URL = 'https://github.com/NewbieIndieGameDev/steam-insights/archive/refs/heads/main.zip'


def main() -> None:
    get_csv_from_zip(STEAM_200K_URL, DATA_DIR)
    # get_csv_from_zip(STEAM_200K_URL, DATA_DIR)
    return


def get_csv_from_zip(url: str, output_dir: Path) -> None:
    assert output_dir.is_dir(), f"Path not a directory: '{output_dir}'"

    resp = requests.get(url)
    zip_file = ZipFile(BytesIO(resp.content))

    filenames = zip_file.namelist()
    for name in filenames:
        out_path = output_dir / name
        out_path.write_bytes(zip_file.read(name))
    
    return


if __name__ == '__main__':
    main()