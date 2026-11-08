import {
  getBuses, resetCount, CAPACITY_EDITABLE, setCapacity, logout, requireLogin, occupancy,
  STATUS_LABEL, el, showNotice, hideNotice, startPolling, redirectToLogin, goToLogin, AuthError,
  formatTime, timeAgo,
} from './api.js';

const $ = (id) => document.getElementById(id);
const notice = $('notice');
let busId = null;
let currentCapacity = 0;
let lastOk = null;
let lastCount = null;
const activity = []; // the back end has no events route, so we note count changes ourselves

function render(bus, events) {
  const o = occupancy(bus);
  currentCapacity = o.capacity;
  $('bus-title').textContent = `Driver view${bus.name ? ' - ' + bus.name : ''}`;
  $('route-line').textContent = bus.route ? `Route ${bus.route}` : '';
  $('count').textContent = o.count;
  $('capacity').textContent = `of ${o.capacity}`;

  const block = $('status');
  block.className = `status-block status-${o.status}`;
  $('bar-fill').className = `bar-fill status-${o.status}`;
  $('bar-fill').style.width = `${o.pct}%`;
  $('status-word').textContent = STATUS_LABEL[o.status];
  $('status-detail').textContent =
    o.status === 'unknown' ? 'Set a capacity' : o.atCapacity ? 'No places left' : `${o.placesLeft} places left`;

  $('alarm').hidden = !o.atCapacity;
  if (!$('alarm').hidden) {
    $('alarm').textContent = o.over > 0
      ? `Over capacity by ${o.over} - do not let more passengers board.`
      : 'Bus is full - do not let more passengers board.';
  }

  const list = $('activity-list');
  list.replaceChildren();
  events.forEach((e) => {
    const isIn = String(e.type).toUpperCase() === 'IN';
    list.append(el('li', {},
      el('span', { text: isIn ? 'Passenger boarded' : 'Passenger left' }),
      el('time', { text: formatTime(e.time), attrs: { datetime: e.time } })));
  });
  $('activity-empty').hidden = events.length > 0;
}

async function refresh() {
  try {
    const buses = await getBuses();
    if (!buses.length) {
      showNotice(notice, 'No bus is assigned to you yet.');
      return;
    }
    const bus = buses.find((b) => b.id === busId) || buses[0];
    busId = bus.id;
    if (lastCount !== null && bus.count !== lastCount) {
      const diff = bus.count - lastCount;
      const type = diff > 0 ? 'IN' : 'OUT';
      for (let i = 0; i < Math.min(Math.abs(diff), 5); i += 1) {
        activity.unshift({ type, time: new Date().toISOString() });
      }
      activity.length = Math.min(activity.length, 5);
    }
    lastCount = bus.count;
    render(bus, activity);
    lastOk = Date.now();
    hideNotice(notice);
  } catch (err) {
    if (err instanceof AuthError) return redirectToLogin();
    showNotice(notice, 'Cannot reach the server. The numbers on screen may be out of date.');
  }
  $('updated').textContent = lastOk ? `Updated ${timeAgo(Date.now() - lastOk)}` : 'No data yet';
}

// ----- reset
const resetDialog = $('reset-dialog');
$('reset-btn').addEventListener('click', () => resetDialog.showModal());
resetDialog.addEventListener('close', async () => {
  if (resetDialog.returnValue !== 'ok' || !busId) return;
  try {
    await resetCount(busId);
    await tick();
  } catch (err) {
    if (err instanceof AuthError) return redirectToLogin();
    showNotice(notice, 'Reset failed. Try again.');
  }
});

// ----- capacity
const capDialog = $('capacity-dialog');
const capInput = $('capacity-input');
const capError = $('capacity-error');
$('capacity-btn').addEventListener('click', () => {
  capInput.value = currentCapacity || '';
  capError.hidden = true;
  capDialog.showModal();
  capInput.select();
});
$('capacity-form').addEventListener('submit', async (event) => {
  if (event.submitter && event.submitter.value === 'cancel') return; // dialog closes itself
  event.preventDefault();
  const value = Number(capInput.value);
  if (!Number.isInteger(value) || value < 1 || value > 200) {
    capError.textContent = 'Enter a whole number from 1 to 200.';
    capError.hidden = false;
    return;
  }
  try {
    await setCapacity(busId, value);
    capDialog.close();
    await tick();
  } catch (err) {
    if (err instanceof AuthError) return redirectToLogin();
    capError.textContent = 'Could not save. Try again.';
    capError.hidden = false;
  }
});

$('logout').addEventListener('click', async () => {
  try { await logout(); } catch { /* leave anyway */ }
  goToLogin();
});

let tick = () => {};
requireLogin().then((user) => {
  if (!user) return;
  if (user.role === 'passenger') { location.replace('index.html'); return; }
  if (user.role === 'guest') $('logout').hidden = true;
  $('capacity-btn').hidden = !CAPACITY_EDITABLE;
  tick = startPolling(refresh);
  setInterval(() => {
    if (lastOk) $('updated').textContent = `Updated ${timeAgo(Date.now() - lastOk)}`;
  }, 1000);
});
