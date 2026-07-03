from core.realtime import AutoImportWatcher


def test_auto_import_watcher_pending():
    watcher = AutoImportWatcher()
    files = watcher.pending_files()
    assert isinstance(files, list)
