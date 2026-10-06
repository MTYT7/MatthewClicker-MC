from flask import Flask, jsonify, render_template, request
import json
import math
import os
import time

app = Flask(__name__)
SAVE_FILE = "game_save.json"

UPGRADES = [
    {"name": "Lucky Finger", "base_cost": 25, "power": 1, "kind": "click", "description": "+1 click per tap"},
    {"name": "Gooner Edward Scumpi Hand", "base_cost": 120, "power": 3, "kind": "click", "description": "+3 clicks per tap"},
    {"name": "Edward gooning skills", "base_cost": 600, "power": 10, "kind": "click", "description": "+10 clicks per tap"},
    {"name": "Mathew balls", "base_cost": 3000, "power": 35, "kind": "click", "description": "+35 clicks per tap"},
    {"name": "Turbo Finger", "base_cost": 15000, "power": 120, "kind": "click", "description": "+120 clicks per tap"},
    {"name": "Edward Scumpi's gooning laptop", "base_cost": 75000, "power": 400, "kind": "click", "description": "+400 clicks per tap"},
    {"name": "Pum pum power", "base_cost": 350000, "power": 1500, "kind": "click", "description": "+1,500 clicks per tap"},
    {"name": "Tung tung time", "base_cost": 1500000, "power": 6000, "kind": "click", "description": "+6,000 clicks per tap"},
    {"name": "Mathew Mode", "base_cost": 7000000, "power": 25000, "kind": "click", "description": "+25,000 clicks per tap"},
    {"name": "Ultimate Click", "base_cost": 30000000, "power": 100000, "kind": "click", "description": "+100,000 clicks per tap"},
    {"name": "Mathew Fan Club", "base_cost": 100, "power": 1, "kind": "auto", "description": "+1 click per second"},
    {"name": "Snack Assistant", "base_cost": 500, "power": 4, "kind": "auto", "description": "+4 clicks per second"},
    {"name": "Enrique Factory", "base_cost": 2500, "power": 15, "kind": "auto", "description": "+15 clicks per second"},
    {"name": "Mathew Stream", "base_cost": 12000, "power": 55, "kind": "auto", "description": "+55 clicks per second"},
    {"name": "Chicken Sandwich", "base_cost": 60000, "power": 200, "kind": "auto", "description": "+200 clicks per second"},
    {"name": "Mathew Merch Shop", "base_cost": 300000, "power": 750, "kind": "auto", "description": "+750 clicks per second"},
    {"name": "Mathwew Robot", "base_cost": 1500000, "power": 3000, "kind": "auto", "description": "+3,000 clicks per second"},
    {"name": "Mathew Empire", "base_cost": 7000000, "power": 12000, "kind": "auto", "description": "+12,000 clicks per second"},
    {"name": "Moon Base", "base_cost": 35000000, "power": 50000, "kind": "auto", "description": "+50,000 clicks per second"},
    {"name": "Mathew Multiverse", "base_cost": 175000000, "power": 200000, "kind": "auto", "description": "+200,000 clicks per second"},
]

DEFAULT_STATE = {
    "clicks": 0.0,
    "total_clicks": 0.0,
    "manual_clicks": 0.0,
    "auto_clicks": 0.0,
    "rebirths": 0,
    "crystals": 0,
    "crystal_click_level": 0,
    "crystal_auto_level": 0,
    "combo": 0,
    "last_click_time": 0.0,
    "quest_clicks": 0,
    "quest_goal": 100,
    "levels": [0] * len(UPGRADES),
    "costs": [item["base_cost"] for item in UPGRADES],
    "last_saved": time.time(),
}

game_state = DEFAULT_STATE.copy()


def compute_click_power():
    power = 1
    for idx, upgrade in enumerate(UPGRADES):
        if upgrade["kind"] == "click":
            power += game_state["levels"][idx] * upgrade["power"]
    return power


def compute_rebirth_bonus():
    return 1 + game_state["rebirths"] * 0.25 + game_state["crystal_click_level"] * 0.05


def compute_auto_per_second():
    total = 0
    for idx, upgrade in enumerate(UPGRADES):
        if upgrade["kind"] == "auto":
            total += game_state["levels"][idx] * upgrade["power"]
    return total * compute_rebirth_bonus() * (1 + game_state["crystal_auto_level"] * 0.05)


def rebirth_requirement():
    return 1_000_000 * (10 ** game_state["rebirths"])


def save_game():
    game_state["last_saved"] = time.time()
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(game_state, file)


def load_game():
    global game_state
    if not os.path.exists(SAVE_FILE):
        return

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            loaded = json.load(file)
        if not isinstance(loaded, dict):
            return

        base = DEFAULT_STATE.copy()
        base.update(loaded)
        if "levels" not in base or len(base["levels"]) != len(UPGRADES):
            base["levels"] = [0] * len(UPGRADES)
        if "costs" not in base or len(base["costs"]) != len(UPGRADES):
            base["costs"] = [item["base_cost"] for item in UPGRADES]
        game_state = base
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        game_state = DEFAULT_STATE.copy()


def state_payload():
    return {
        "clicks": game_state["clicks"],
        "total_clicks": game_state["total_clicks"],
        "manual_clicks": game_state["manual_clicks"],
        "auto_clicks": game_state["auto_clicks"],
        "rebirths": game_state["rebirths"],
        "crystals": game_state["crystals"],
        "crystal_click_level": game_state["crystal_click_level"],
        "crystal_auto_level": game_state["crystal_auto_level"],
        "quest_clicks": game_state["quest_clicks"],
        "quest_goal": game_state["quest_goal"],
        "click_power": compute_click_power(),
        "auto_per_second": compute_auto_per_second(),
        "rebirth_bonus": compute_rebirth_bonus(),
        "rebirth_requirement": rebirth_requirement(),
        "upgrades": [
            {
                "name": upgrade["name"],
                "kind": upgrade["kind"],
                "description": upgrade["description"],
                "level": game_state["levels"][idx],
                "cost": game_state["costs"][idx],
            }
            for idx, upgrade in enumerate(UPGRADES)
        ],
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state", methods=["GET"])
def api_state():
    return jsonify(state_payload())


@app.route("/api/click", methods=["POST"])
def api_click():
    now = time.time()
    if now - game_state["last_click_time"] < 0.65:
        game_state["combo"] = min(game_state["combo"] + 1, 50)
    else:
        game_state["combo"] = 1
    game_state["last_click_time"] = now

    combo_bonus = 1 + game_state["combo"] * 0.02
    amount = compute_click_power() * compute_rebirth_bonus() * combo_bonus
    game_state["clicks"] += amount
    game_state["total_clicks"] += amount
    game_state["manual_clicks"] += amount
    game_state["quest_clicks"] += 1

    if game_state["quest_clicks"] >= game_state["quest_goal"]:
        reward = max(game_state["quest_goal"] * compute_click_power() * compute_rebirth_bonus(), 1000)
        game_state["clicks"] += reward
        game_state["total_clicks"] += reward
        game_state["quest_clicks"] = 0
        game_state["quest_goal"] = int(game_state["quest_goal"] * 1.5)
        message = f"Quest complete! +{int(reward):,} points"
    else:
        message = ""

    save_game()
    return jsonify({
        "amount": amount,
        "clicks": game_state["clicks"],
        "combo": game_state["combo"],
        "message": message,
    })


@app.route("/api/buy-upgrade", methods=["POST"])
def api_buy_upgrade():
    payload = request.get_json(silent=True) or {}
    index = int(payload.get("index", -1))
    if index < 0 or index >= len(UPGRADES):
        return jsonify({"error": "Invalid upgrade index"}), 400

    cost = game_state["costs"][index]
    if game_state["clicks"] < cost:
        return jsonify({"error": "Not enough points"}), 400

    game_state["clicks"] -= cost
    game_state["levels"][index] += 1
    game_state["costs"][index] = max(game_state["costs"][index] + 1, int(game_state["costs"][index] * 1.18))
    save_game()
    return jsonify({"success": True, "state": state_payload()})


@app.route("/api/rebirth", methods=["POST"])
def api_rebirth():
    required = rebirth_requirement()
    if game_state["clicks"] < required:
        return jsonify({"error": "Not enough points for rebirth"}), 400

    game_state["rebirths"] += 1
    game_state["crystals"] += 1
    game_state["clicks"] = 0
    game_state["total_clicks"] += required
    game_state["combo"] = 0
    game_state["levels"] = [0] * len(UPGRADES)
    game_state["costs"] = [item["base_cost"] for item in UPGRADES]
    save_game()
    return jsonify({"success": True, "state": state_payload()})


@app.route("/api/tick", methods=["POST"])
def api_tick():
    payload = request.get_json(silent=True) or {}
    dt = max(0.0, float(payload.get("dt", 1.0)))
    gained = compute_auto_per_second() * dt
    if gained > 0:
        game_state["clicks"] += gained
        game_state["total_clicks"] += gained
        game_state["auto_clicks"] += gained
        save_game()
    return jsonify({"gained": gained, "clicks": game_state["clicks"], "state": state_payload()})


@app.route("/api/save", methods=["POST"])
def api_save():
    save_game()
    return jsonify({"success": True})


load_game()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)






































