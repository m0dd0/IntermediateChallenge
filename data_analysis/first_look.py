from pathlib import Path
import json
from tqdm import tqdm

DATA_PATH = Path(__file__).parent.parent / "data" / "DBDaten"

def print_station_file_count():
    # pront how many files exist per station
    for city_dir in DATA_PATH.iterdir():
        print(f"{city_dir.stem}: {len(list(city_dir.iterdir()))} files")

def assert_keys_equality(all_files):
    # check that all keys in all entries of all files are the same (takes a while)
    with open(all_files[0]) as f:
        keys = set(json.load(f)[0].keys())
    for file in tqdm(all_files, leave=False):
        with open(file) as f:
            data = json.load(f)
        for entry in data:
            assert keys == set(entry.keys())

if __name__ == "__main__":
    print_station_file_count()

    # get all json fiel paths
    all_files = [f for city_dir in DATA_PATH.iterdir() for f in city_dir.iterdir()]
    
    assert_keys_equality(all_files)