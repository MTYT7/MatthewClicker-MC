const state = {
  clicks: 0,
  clickPower: 1,
  autoPerSecond: 0,
  rebirthBonus: 1,
  rebirthRequirement: 1000000,
  upgrades: [],
  questClicks: 0,
  questGoal: 100,
  rebirths: 0,
  crystals: 0,
};

let lastTick = Date.now();

const scoreEl = document.getElementById("score");
const rateEl = document.getElementById("rate");
const statusEl = document.getElementById("status");
const meterFillEl = document.getElementById("meterFill");
const meterLabelEl = document.getElementById("meterLabel");
const rebirthButton = document.getElementById("rebirthButton");
const achievementEl = document.getElementById("achievement");
const upgradeListEl = document.getElementById("upgradeList");
const upgradeModal = document.getElementById("upgradeModal");

function formatNumber(value) {
  if (value >= 1000000000) return `${(value / 1000000000).toFixed(2)}B`;
  if (value >= 1000000) return `${(value / 1000000).toFixed(2)}M`;
  if (value >= 1000) return `${(value / 1000).toFixed(2)}K`;
  return Math.floor(value).toLocaleString();
}

function renderUpgrades() {
  upgradeListEl.innerHTML = "";

  state.upgrades.forEach((upgrade, index) => {
    const row = document.createElement("div");
    row.className = "upgrade-item";

    const copy = document.createElement("div");
    copy.className = "upgrade-copy";

    const name = document.createElement("span");
    name.className = "upgrade-name";
    name.textContent = `${upgrade.name} (Lvl ${upgrade.level})`;

    const meta = document.createElement("span");
    meta.className = "upgrade-meta";
    meta.textContent = `${upgrade.description} • Cost: ${formatNumber(upgrade.cost)}`;

    copy.appendChild(name);
    copy.appendChild(meta);

    const button = document.createElement("button");
    button.className = "buy-button";
    button.textContent = "Buy";
    button.addEventListener("click", () => buyUpgrade(index));

    row.appendChild(copy);
    row.appendChild(button);
    upgradeListEl.appendChild(row);
  });
}

function render() {
  scoreEl.textContent = `${formatNumber(state.clicks)} Mathew Points`;
  rateEl.textContent = `${formatNumber(state.clickPower * state.rebirthBonus)} per click | ${formatNumber(state.autoPerSecond)} per second`;

  const percent = Math.min((state.clicks / state.rebirthRequirement) * 100, 100);
  meterFillEl.style.width = `${percent}%`;
  meterLabelEl.textContent = `${formatNumber(state.clicks)} / ${formatNumber(state.rebirthRequirement)}`;
  rebirthButton.disabled = state.clicks < state.rebirthRequirement;

  if (state.questClicks >= state.questGoal) {
    achievementEl.textContent = `Quest complete! Next goal: ${state.questGoal}`;
  } else {
    achievementEl.textContent = `Quest: ${state.questClicks}/${state.questGoal} clicks | Crystals: ${state.crystals}`;
  }
}

async function fetchState() {
  const response = await fetch("/api/state");
  const data = await response.json();
  state.clicks = data.clicks;
  state.clickPower = data.click_power;
  state.autoPerSecond = data.auto_per_second;
  state.rebirthBonus = data.rebirth_bonus;
  state.rebirthRequirement = data.rebirth_requirement;
  state.upgrades = data.upgrades;
  state.questClicks = data.quest_clicks;
  state.questGoal = data.quest_goal;
  state.rebirths = data.rebirths;
  state.crystals = data.crystals;
  render();
  renderUpgrades();
}

async function doClick() {
  const response = await fetch("/api/click", { method: "POST" });
  const data = await response.json();

  if (data.message) {
    statusEl.textContent = data.message;
  } else {
    statusEl.textContent = `Combo x${data.combo} • +${formatNumber(data.amount)}`;
  }

  state.clicks = data.clicks;
  await fetchState();
}

async function buyUpgrade(index) {
  const response = await fetch("/api/buy-upgrade", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ index }),
  });

  const data = await response.json();
  if (response.ok) {
    state.clicks = data.state.clicks;
    state.clickPower = data.state.click_power;
    state.autoPerSecond = data.state.auto_per_second;
    state.rebirthBonus = data.state.rebirth_bonus;
    state.rebirthRequirement = data.state.rebirth_requirement;
    state.upgrades = data.state.upgrades;
    state.questClicks = data.state.quest_clicks;
    state.questGoal = data.state.quest_goal;
    render();
    renderUpgrades();
  } else {
    statusEl.textContent = data.error || "Purchase failed";
  }
}

async function doRebirth() {
  const response = await fetch("/api/rebirth", { method: "POST" });
  const data = await response.json();

  if (response.ok) {
    state.clicks = data.state.clicks;
    state.clickPower = data.state.click_power;
    state.autoPerSecond = data.state.auto_per_second;
    state.rebirthBonus = data.state.rebirth_bonus;
    state.rebirthRequirement = data.state.rebirth_requirement;
    state.upgrades = data.state.upgrades;
    state.questClicks = data.state.quest_clicks;
    state.questGoal = data.state.quest_goal;
    state.rebirths = data.state.rebirths;
    state.crystals = data.state.crystals;
    statusEl.textContent = "REBIRTH COMPLETE!";
    render();
    renderUpgrades();
  } else {
    statusEl.textContent = data.error || "Rebirth failed";
  }
}

async function saveGame() {
  await fetch("/api/save", { method: "POST" });
}

async function tickClient() {
  const now = Date.now();
  const dt = (now - lastTick) / 1000;
  lastTick = now;

  try {
    const response = await fetch("/api/tick", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dt }),
    });
    const data = await response.json();
    state.clicks = data.state.clicks;
    state.clickPower = data.state.click_power;
    state.autoPerSecond = data.state.auto_per_second;
    state.rebirthBonus = data.state.rebirth_bonus;
    state.rebirthRequirement = data.state.rebirth_requirement;
    state.upgrades = data.state.upgrades;
    state.questClicks = data.state.quest_clicks;
    state.questGoal = data.state.quest_goal;
    state.rebirths = data.state.rebirths;
    state.crystals = data.state.crystals;
    render();
  } catch (error) {
    console.log(error);
  }
}

function openUpgrades() {
  renderUpgrades();
  upgradeModal.classList.remove("hidden");
}

function closeUpgrades() {
  upgradeModal.classList.add("hidden");
}

window.addEventListener("load", async () => {
  await fetchState();
  render();
  renderUpgrades();
  setInterval(tickClient, 1000);
  setInterval(saveGame, 15000);
});

document.getElementById("clickButton").addEventListener("click", doClick);
document.getElementById("rebirthButton").addEventListener("click", doRebirth);
document.getElementById("saveButton").addEventListener("click", saveGame);
document.getElementById("upgradesButton").addEventListener("click", openUpgrades);
document.getElementById("statsButton").addEventListener("click", () => {
  alert(`Current points: ${formatNumber(state.clicks)}\nRebirths: ${state.rebirths}\nCrystals: ${state.crystals}`);
});
document.getElementById("closeModalButton").addEventListener("click", closeUpgrades);

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeUpgrades();
});
