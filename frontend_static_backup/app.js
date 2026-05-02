const API_BASE_URL = "http://127.0.0.1:5000";

async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const errorMsg = document.getElementById("errorMsg");

  errorMsg.innerText = "";

  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok) {
      errorMsg.innerText = data.message || "Login failed";
      return;
    }

    localStorage.setItem("token", data.token);
    window.location.href = "dashboard.html";
  } catch (error) {
    errorMsg.innerText = "Unable to connect to backend server";
  }
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}

async function loadDevices() {
  const token = localStorage.getItem("token");

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  const grid = document.getElementById("devicesGrid");
  const errorMsg = document.getElementById("errorMsg");

  grid.innerHTML = "";
  errorMsg.innerText = "";

  try {
    const response = await fetch(`${API_BASE_URL}/api/devices`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const data = await response.json();

    if (!response.ok) {
      errorMsg.innerText = data.message || "Failed to load devices";
      return;
    }

    data.devices.forEach(device => {
      grid.innerHTML += renderDeviceCard(device);
    });
  } catch (error) {
    errorMsg.innerText = "Unable to load devices";
  }
}

function renderDeviceCard(device) {
  let extraFields = "";

  if (device.type === "AC") {
    extraFields = `
      <div class="field">Temperature: <strong id="temp-${device.id}">${device.temperature}</strong> °C</div>
      <div class="controls">
        <input id="tempInput-${device.id}" type="number" placeholder="16-30" />
        <button onclick="updateTemperature(${device.id})">Set Temp</button>
      </div>
    `;
  }

  if (device.type === "TV") {
    extraFields = `
      <div class="field">Volume: <strong id="volume-${device.id}">${device.volume}</strong></div>
      <div class="controls">
        <input id="volumeInput-${device.id}" type="number" placeholder="0-100" />
        <button onclick="updateVolume(${device.id})">Set Volume</button>
      </div>
    `;
  }

  if (device.type === "REFRIGERATOR") {
    extraFields = `
      <div class="field">Fridge Temp: <strong>${device.temperature}</strong> °C</div>
      <div class="field">Freezer Temp: <strong>${device.freezer_temperature}</strong> °C</div>
    `;
  }

  if (device.type === "WASHING_MACHINE") {
    extraFields = `
      <div class="field">Cycle: <strong>${device.cycle_status}</strong></div>
      <div class="field">Water Level: <strong>${device.water_level}</strong></div>
    `;
  }

  return `
    <div class="card" data-testid="device-card-${device.id}">
      <h3>${device.name}</h3>
      <span class="badge">${device.status}</span>
      <div class="field">Type: <strong>${device.type}</strong></div>
      <div class="field">Power: <strong id="power-${device.id}">${device.power}</strong></div>
      <div class="field">Mode: <strong>${device.mode}</strong></div>
      <div class="field">Firmware: <strong>${device.firmware_version}</strong></div>

      <div class="controls">
        <button onclick="updatePower(${device.id}, 'ON')">Power ON</button>
        <button onclick="updatePower(${device.id}, 'OFF')">Power OFF</button>
      </div>

      ${extraFields}
    </div>
  `;
}

async function updatePower(deviceId, power) {
  const token = localStorage.getItem("token");
  clearMessages();

  const response = await fetch(`${API_BASE_URL}/api/devices/${deviceId}/power`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ power })
  });

  const data = await response.json();

  if (!response.ok) {
    showError(data.message);
    return;
  }

  showMessage(data.message);
  loadDevices();
}

async function updateTemperature(deviceId) {
  const token = localStorage.getItem("token");
  const temperature = Number(document.getElementById(`tempInput-${deviceId}`).value);
  clearMessages();

  const response = await fetch(`${API_BASE_URL}/api/devices/${deviceId}/temperature`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ temperature })
  });

  const data = await response.json();

  if (!response.ok) {
    showError(data.message);
    return;
  }

  showMessage(data.message);
  loadDevices();
}

async function updateVolume(deviceId) {
  const token = localStorage.getItem("token");
  const volume = Number(document.getElementById(`volumeInput-${deviceId}`).value);
  clearMessages();

  const response = await fetch(`${API_BASE_URL}/api/devices/${deviceId}/volume`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ volume })
  });

  const data = await response.json();

  if (!response.ok) {
    showError(data.message);
    return;
  }

  showMessage(data.message);
  loadDevices();
}

function showMessage(message) {
  document.getElementById("message").innerText = message;
}

function showError(message) {
  document.getElementById("errorMsg").innerText = message;
}

function clearMessages() {
  document.getElementById("message").innerText = "";
  document.getElementById("errorMsg").innerText = "";
}