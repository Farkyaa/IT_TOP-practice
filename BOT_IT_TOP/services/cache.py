import hashlib
from pathlib import Path

_cache_storage = {}

def get_file_hash(file_path: Path) -> str:
    try:
        data = file_path.read_bytes()
        return hashlib.md5(data).hexdigest()
    except Exception:
        return ""

def make_cache_key(report_type: int, file_hash: str, extra: str | None) -> str:
    return f"{report_type}:{file_hash}:{extra or 'none'}"

def get_cached_report(report_type: int, file_path: Path, extra: str | None, save: str | None = None):

    file_hash = get_file_hash(file_path)
    if not file_hash:
        return None

    key = make_cache_key(report_type, file_hash, extra)

    if save is not None:
        _cache_storage[key] = save
        return save

    return _cache_storage.get(key)
