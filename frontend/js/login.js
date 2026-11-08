import { login, getMe, safeNext } from './api.js';

const form = document.getElementById('login-form');
const errorBox = document.getElementById('login-error');
const button = document.getElementById('login-btn');

function homeFor(user) {
  return safeNext() || (user.role === 'driver' ? 'driver.html' : 'index.html');
}

// Already signed in? Skip the form.
getMe().then((user) => location.replace(homeFor(user))).catch(() => {});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  errorBox.hidden = true;
  const username = form.username.value.trim();
  const password = form.password.value;
  if (!username || !password) {
    errorBox.textContent = 'Enter your username and password.';
    errorBox.hidden = false;
    return;
  }
  button.disabled = true;
  try {
    const user = await login(username, password);
    location.replace(homeFor(user));
  } catch (err) {
    errorBox.textContent =
      err.name === 'AuthError' ? 'Wrong username or password.' : 'Could not reach the server. Try again.';
    errorBox.hidden = false;
    form.password.value = '';
  } finally {
    button.disabled = false;
  }
});
