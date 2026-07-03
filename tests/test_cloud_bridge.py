from core.cloud_bridge import CloudBridge


def test_cloud_bridge_publish():
    bridge = CloudBridge(cloud_dir="cloud_test")
    r = bridge.publish()
    assert r["ok"] is True
