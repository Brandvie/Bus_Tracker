"""Fake Bus Tracker API (same routes and field names as ../backend) so the front end
can be tried without MongoDB.

Run from the frontend folder:   python dev/mock_server.py
Open http://localhost:8080/   (passenger)  and  http://localhost:8080/driver.html

Simulate the sensor:  curl -X POST localhost:8080/api/occupancy/DKIT_BUS_01/movement -H "Content-Type: application/json" -d "{\"direction\":\"in\",\"quantity\":1}"
Local testing only - never deploy this. Standard library only.
"""
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
buses = {
    "DKIT_BUS_01": {"bus_id": "DKIT_BUS_01", "capacity": 25, "current_passengers": 8,
                    "crowd_status": "Quiet", "motion_detected": False, "active": True},
    "DKIT_BUS_02": {"bus_id": "DKIT_BUS_02", "capacity": 25, "current_passengers": 17,
                    "crowd_status": "Normal", "motion_detected": False, "active": True},
}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)

    def send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/api/buses/":
            return self.send_json(200, list(buses.values()))
        if path.startswith("/api/"):
            return self.send_json(404, {"detail": "Not Found"})  # like the real back end: no /api/me
        super().do_GET()

    def do_POST(self):
        parts = self.path.split("?")[0].strip("/").split("/")  # api occupancy ID action
        bus = buses.get(parts[2]) if len(parts) == 4 else None
        if not bus:
            return self.send_json(404, {"detail": "Bus not found"})
        n = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(n) or b"{}")
        if parts[3] == "reset":
            bus["current_passengers"] = 0
        elif parts[3] == "movement":
            step = body.get("quantity", 1) * (1 if body.get("direction") == "in" else -1)
            bus["current_passengers"] = max(0, min(bus["capacity"], bus["current_passengers"] + step))
        elif parts[3] == "count":
            bus["current_passengers"] = int(body["current_passengers"])
        self.send_json(200, bus)


if __name__ == "__main__":
    print("Mock API on http://localhost:8080/")
    ThreadingHTTPServer(("", 8080), Handler).serve_forever()
