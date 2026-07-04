from core.v93.realtime.realtime_core import RealtimeCore

class RealtimeHealth:
    def check(self):
        return RealtimeCore().health()
