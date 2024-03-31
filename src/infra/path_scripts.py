from functools import lru_cache
from pathlib import Path


def get_temp_dir() -> Path:
    temp_dir = get_root_dir() / "temp"
    if not temp_dir.exists():
        temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


def get_dir_from_root(*args) -> Path:
    dir_path = get_root_dir()
    if args:
        for arg in args:
            dir_path = dir_path / arg
    return dir_path


@lru_cache
def get_root_dir() -> Path:
    current_file = Path(__file__)
    current_file_dir = current_file.parent
    project_root = current_file_dir.parent
    project_root_absolute = project_root.resolve()
    return project_root_absolute
