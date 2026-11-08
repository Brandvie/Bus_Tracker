# Front end (Hafid)

Login, passenger and driver pages for the Bus Tracker. Plain HTML, CSS and JavaScript, no build step.

| File | What it is |
|---|---|
| `login.html`, `js/login.js` | Sign in, then go to the driver or passenger page |
| `index.html`, `js/passenger.js` (passenger page, the home page) | Quiet / Busy / Full status, places left, wheelchair space, other buses |
| `driver.html`, `js/driver.js` | Live count, capacity, overcrowding alarm, reset count, set capacity, recent activity |
| `js/api.js` | All API calls, login redirect and the crowd thresholds in one place |
| `css/styles.css` | Shared styles (light passenger theme, dark driver theme) |
| `dev/mock_server.py` | Fake API for trying the pages without the back end |

The pages refresh every 5 seconds. The API they expect is in `../docs/frontend-api-contract.md`.

## Run with the real back end

    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload

Open http://127.0.0.1:8000/ (passenger) or http://127.0.0.1:8000/driver.html (driver). Needs MongoDB running and `backend/.env` (copy `.env.example`).

## Try it without MongoDB

    cd frontend
    python dev/mock_server.py

Open http://localhost:8080/ . The mock has the same routes as the real back end.
