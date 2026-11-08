// Shared helpers for every Bus Tracker page.
// The API contract this file relies on is in docs/frontend-api-contract.md.

export const POLL_MS = 5000; // how often the screens refresh themselves

// Crowd levels as a percentage of capacity (same thresholds as the design document).
//   under 60%  -> Quiet
//   60% - 90%  -> Busy
//   over 90%   -> Full
export const THRESHOLDS = { busy: 60, full: 90 };

export const STATUS_LABEL = {
  quiet: 'QUIET',
  busy: 'BUSY',
  full: 'FULL',
  unknown: 'NO DATA',
};

const PAGES = ['index.html', 'driver.html'];

export class AuthError extends Error {
  constructor(message = 'Not logged in') {
    super(message);
    this.name = 'AuthError';
  }
}

// ---------------------------------------------------------------- API calls
// Talks to the FastAPI back end in ../backend (same server, so no CORS needed).

// The back end has no "set capacity" route yet (capacity is fixed in database.py),
// so the driver page hides that button. Set to true once the route exists.
export const CAPACITY_EDITABLE = false;

async function request(path, { method = 'GET', body } = {}) {
  const options = {
    method,
    credentials: 'same-origin', // session cookie (once the back end has login)
    headers: { Accept: 'application/json' },
  };
  if (body !== undefined) {
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(body);
  }
  const res = await fetch(path, options);
  if (res.status === 401) throw new AuthError();
  if (!res.ok) {
    const err = new Error(`Request failed (${res.status})`);
    err.status = res.status;
    throw err;
  }
  return res.status === 204 ? null : res.json();
}

// Back end field names -> the names the pages use.
function normaliseBus(b) {
  return {
    id: b.bus_id,
    route: b.route || '',
    name: b.name || String(b.bus_id).replace(/_/g, ' '),
    capacity: b.capacity,
    count: b.current_passengers,
    wheelchair_free: b.wheelchair_free ?? null,
    eta_minutes: b.eta_minutes ?? null,
    motion: Boolean(b.motion_detected),
  };
}

export const login = (username, password) =>
  request('/api/login', { method: 'POST', body: { username, password } });
export const logout = () => request('/api/logout', { method: 'POST' });

// Until the back end has login there is no /api/me (404). Then everyone is a "guest"
// and the pages open without a sign-in. Once /api/me exists, login is enforced.
export async function getMe() {
  try {
    return await request('/api/me');
  } catch (err) {
    if (err.status === 404) return { username: 'guest', role: 'guest' };
    throw err;
  }
}

export const getBuses = async () => (await request('/api/buses/')).map(normaliseBus);
export const resetCount = (id) =>
  request(`/api/occupancy/${encodeURIComponent(id)}/reset`, { method: 'POST' });
export const setCapacity = (id, capacity) =>
  request(`/api/buses/${encodeURIComponent(id)}/capacity`, { method: 'POST', body: { capacity } });

// ------------------------------------------------------------ login handling

export function redirectToLogin() {
  const page = location.pathname.split('/').pop();
  const next = PAGES.includes(page) ? `?next=${encodeURIComponent(page)}` : '';
  location.replace(`login.html${next}`);
}

// Only ever redirect to one of our own pages (stops "open redirect" tricks).
export function safeNext() {
  const next = new URLSearchParams(location.search).get('next');
  return PAGES.includes(next) ? next : null;
}

export function goToLogin() {
  location.replace('login.html');
}

export async function requireLogin() {
  try {
    return await getMe();
  } catch (err) {
    if (err instanceof AuthError) {
      redirectToLogin();
      return null;
    }
    throw err;
  }
}

// ------------------------------------------------------- occupancy / status

export function occupancy(bus) {
  const capacity = Number(bus.capacity) || 0;
  const count = Math.max(0, Math.round(Number(bus.count) || 0));
  const pct = capacity > 0 ? (count / capacity) * 100 : 0;

  let status = 'unknown';
  if (capacity > 0) {
    status = pct < THRESHOLDS.busy ? 'quiet' : pct <= THRESHOLDS.full ? 'busy' : 'full';
  }

  return {
    count,
    capacity,
    pct: Math.min(pct, 100),
    placesLeft: Math.max(capacity - count, 0),
    over: Math.max(count - capacity, 0),
    atCapacity: capacity > 0 && count >= capacity,
    status,
  };
}

// ---------------------------------------------------------------- formatting

export function formatTime(iso) {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '--:--:--';
  return d.toLocaleTimeString('en-IE', { hour12: false });
}

export function timeAgo(ms) {
  const s = Math.max(0, Math.floor(ms / 1000));
  if (s < 5) return 'just now';
  if (s < 60) return `${s} seconds ago`;
  const m = Math.floor(s / 60);
  return m === 1 ? '1 minute ago' : `${m} minutes ago`;
}

// ------------------------------------------------------------------- DOM

// Builds elements with textContent only, so text from the server can never become HTML.
export function el(tag, { className, text, attrs } = {}, ...children) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  if (attrs) for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  for (const child of children) node.append(child);
  return node;
}

export function showNotice(node, message) {
  node.textContent = message;
  node.hidden = false;
}

export function hideNotice(node) {
  node.hidden = true;
  node.textContent = '';
}

// Runs fn now and then every POLL_MS, skipping ticks while the tab is hidden.
export function startPolling(fn) {
  let running = false;
  const tick = async () => {
    if (running) return;
    running = true;
    try {
      await fn();
    } finally {
      running = false;
    }
  };
  tick();
  setInterval(() => {
    if (!document.hidden) tick();
  }, POLL_MS);
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) tick();
  });
  return tick;
}
