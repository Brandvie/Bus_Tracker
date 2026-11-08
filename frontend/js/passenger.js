import {
  getBuses, logout, requireLogin, occupancy, STATUS_LABEL, el,
  showNotice, hideNotice, startPolling, redirectToLogin, goToLogin, AuthError, timeAgo,
} from './api.js';

const busesBox = document.getElementById('buses');
const otherSection = document.getElementById('other-section');
const otherList = document.getElementById('other-list');
const notice = document.getElementById('notice');
const updated = document.getElementById('updated');
let lastOk = null;

function detailText(o) {
  if (o.status === 'unknown') return 'No capacity set';
  if (o.atCapacity) return 'No places left';
  return `${o.placesLeft} places left`;
}

function busCard(bus) {
  const o = occupancy(bus);
  const head = el('div', { className: 'bus-card-head' },
    el('h2', { text: `${bus.route ? bus.route + ' - ' : ''}${bus.name || bus.id}` }));
  if (bus.eta_minutes != null) head.append(el('p', { className: 'eta', text: `${bus.eta_minutes} min` }));

  const block = el('div', { className: 'status-block' },
    el('p', { className: 'status-word', text: STATUS_LABEL[o.status] }),
    el('p', { className: 'status-detail', text: detailText(o) }));

  const fill = el('div', { className: 'bar-fill' });
  fill.style.width = `${o.pct}%`;
  const bar = el('div', { className: 'bar', attrs: { 'aria-hidden': 'true' } }, fill);

  let wheelchair = 'Unknown';
  if (bus.wheelchair_free === true) wheelchair = 'Space free';
  if (bus.wheelchair_free === false) wheelchair = 'Space taken';

  const card = el('article', { className: `bus-card status-${o.status}` }, head, block, bar,
    el('div', { className: 'fact-row' }, el('span', { text: 'Passengers' }),
      el('strong', { text: `${o.count} of ${o.capacity}` })),
    el('div', { className: 'fact-row' }, el('span', { text: 'Wheelchair space' }),
      el('strong', { text: wheelchair })));
  return card;
}

function otherRow(bus) {
  const o = occupancy(bus);
  return el('li', { className: `bus-row status-${o.status}` },
    el('span', { text: `${bus.route ? bus.route + ' - ' : ''}${bus.name || bus.id}` }),
    el('span', { className: 'pill', text: STATUS_LABEL[o.status] }));
}

function render(buses) {
  busesBox.replaceChildren();
  otherList.replaceChildren();
  if (!buses.length) {
    busesBox.append(el('p', { className: 'empty-state', text: 'No buses are reporting right now.' }));
    otherSection.hidden = true;
    return;
  }
  const [first, ...rest] = buses;
  busesBox.append(busCard(first));
  rest.forEach((b) => otherList.append(otherRow(b)));
  otherSection.hidden = rest.length === 0;
}

async function refresh() {
  try {
    render(await getBuses());
    lastOk = Date.now();
    hideNotice(notice);
  } catch (err) {
    if (err instanceof AuthError) return redirectToLogin();
    showNotice(notice, 'Cannot reach the server. Showing the last known data.');
  }
  updated.textContent = lastOk ? `Updated ${timeAgo(Date.now() - lastOk)}` : 'No data yet';
}

document.getElementById('logout').addEventListener('click', async () => {
  try { await logout(); } catch { /* ignore, we leave anyway */ }
  goToLogin();
});

requireLogin().then((user) => {
  if (!user) return;
  if (user.role === 'guest') document.getElementById('logout').hidden = true;
  const tick = startPolling(refresh);
  document.getElementById('refresh').addEventListener('click', tick);
  setInterval(() => {
    if (lastOk) updated.textContent = `Updated ${timeAgo(Date.now() - lastOk)}`;
  }, 1000);
});
