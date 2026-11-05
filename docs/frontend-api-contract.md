# Front end <-> back end API contract

What the pages in `frontend/` expect from the FastAPI back end. If the back end differs, change `frontend/js/api.js` only (one place).
Run the pages without the real back end: `python frontend/dev/mock_server.py`.

All JSON. Login uses an **HttpOnly session cookie** set by the server (the JS never stores a token).
Any endpoint except `POST /api/login` answers **401** when not logged in; the pages then go to `login.html`.

| Method | Path | Body | Response |
|---|---|---|---|
| POST | `/api/login` | `{"username","password"}` | `200 {"username","role"}` (`role` = `driver` or `passenger`) + `Set-Cookie`; `401` if wrong |
| POST | `/api/logout` | - | `204`, cookie cleared |
| GET | `/api/me` | - | `{"username","role"}` |
| GET | `/api/buses` | - | list of buses (below) |
| GET | `/api/buses/{id}/events?limit=5` | - | `[{"type":"IN"\|"OUT","time":"ISO-8601"}]`, newest first |
| POST | `/api/buses/{id}/reset` | - | updated bus. Driver only |
| POST | `/api/buses/{id}/capacity` | `{"capacity": 1-200}` | updated bus. Driver only |

Bus object: `{"id","route","name","capacity","count","wheelchair_free": true|false|null,"eta_minutes": number|null}`

`count` is derived from the IN/OUT events. The front end works out Quiet / Busy / Full from `count / capacity`
(under 60% Quiet, 60-90% Busy, over 90% Full).

Security notes for the back end: validate `capacity` as an integer 1-200, check the role on the reset and capacity routes,
set the cookie `HttpOnly; Secure; SameSite=Strict` once on HTTPS, and keep secrets in `.env` (never committed).
