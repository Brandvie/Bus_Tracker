# Bus Tracker

An IoT system that tells passengers how full a bus is before they board, and alerts the driver when the bus is over capacity.

Group SD3b-G5 (team AAB), Dundalk Institute of Technology.
GitHub: https://github.com/Brandvie/Bus_Tracker

## How it works

1. Sensors on the bus (IR break-beam and motion) detect passengers entering and leaving.
2. A Raspberry Pi Zero 2 W counts them and sends the data to the back end (MQTT over TLS).
3. The FastAPI back end stores the bus data in MongoDB and exposes a REST API.
4. The web pages read the API every 5 seconds:
   - **Passenger page** (`/`): Quiet / Busy / Full, places left, wheelchair space.
   - **Driver page** (`/driver.html`): live count, over-capacity alarm, reset count, recent activity.

Crowd levels: under 60% of capacity is Quiet, 60-90% is Busy, over 90% is Full.

## Team

| Member | Part |
|---|---|
| Abdi | Hardware and software testing |
| Brandyvie | Back end and database |
| Hafid | UX design and front end |

## Project structure

```text
backend/    FastAPI app, MongoDB access, sensor and occupancy routes
frontend/   index.html (passenger), driver.html, login.html, js/, css/
docs/       API notes and design documents
```

## Run it

Requirements: Python, [uv](https://docs.astral.sh/uv/) and MongoDB running locally.

```
cd backend
copy .env.example .env
uv run --with-requirements requirements.txt uvicorn main:app --reload
```

Open http://127.0.0.1:8000/ (passenger) and http://127.0.0.1:8000/driver.html (driver).

To try it without MongoDB: `python frontend/dev/mock_server.py`, then open http://localhost:8080/.

Simulate passengers boarding (PowerShell):

```
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/occupancy/DKIT_BUS_01/movement -ContentType "application/json" -Body '{"direction":"in","quantity":5}'
```

## Security

- Secrets live in `backend/.env`, which is git-ignored (`.env.example` shows the format).
- The front end builds all page text with `textContent`, so server data is never inserted as HTML.
- Pages redirect to the login page when the API answers 401.

## Status

Alpha prototype for G-CA2. Not done yet: login and driver-only permissions on the API, setting capacity from the driver page, and the AWS HTTPS deployment.
