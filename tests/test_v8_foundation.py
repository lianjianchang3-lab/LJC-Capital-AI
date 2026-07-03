from pathlib import Path
from core import LJCAppCore


def test_version_exists():
    assert Path("VERSION").exists()


def test_core_boot():
    core = LJCAppCore()
    result = core.boot()
    assert "version" in result
    assert "app" in result
