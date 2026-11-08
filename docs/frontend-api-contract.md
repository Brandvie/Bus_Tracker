# Front end <-> back end API

The front end in `frontend/` uses these routes of the FastAPI back end in `backend/`. All JSON, same server (the back end serves the front end, so no CORS).
Field names are translated in one place: `frontend/js/api.js`.

| Method | Path | Used for |
|---|---|---|
| GET | `/api/buses/` | List of buses: `bus_id, capacity, current_passengers, crowd_status, motion_detected, active` |
| POST | `/api/occupancy/{bus_id}/reset` | Driver "Reset count" |
| POST | `/api/occupancy/{bus_id}/movement` | Sensor/Pi: `{"direction":"in"\|"out","quantity":1}` |
| GET | `/api/me`, POST `/api/login`, `/api/logout` | **Not built yet.** If `/api/me` returns 404 the pages open as "guest". Once it exists the pages redirect to `login.html` on a 401 |

The front end works out Quiet / Busy / Full from `current_passengers / capacity` (under 60% Quiet, 60-90% Busy, over 90% Full).
The "recent activity" list is built in the browser from count changes (there is no events route yet).

## Still missing on the back end (needed for the CA2 security marks)
- Login and sessions, and a check that only drivers can call `reset` and `movement` / `count`.
- A "set capacity" route (`POST /api/buses/{id}/capacity`). Then set `CAPACITY_EDITABLE = true` in `api.js`.
- `crowd_status` in the database uses counts (10/20/25) while the screens use percentages: pick one rule.
- `.env` must stay out of git (see `.gitignore`); copy `backend/.env.example` to `backend/.env`.
