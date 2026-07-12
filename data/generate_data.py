"""
Vehicle Assistant — Synthetic Data Generator
Generates realistic driving session data for Indian mid-range car conditions.
Covers city (Gurugram/Delhi style), highway (NH48), and mixed scenarios.
"""

import random
import math
import csv
import json
import os
from datetime import datetime, timedelta
from uuid import uuid4

random.seed(42)

# ── Config ────────────────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
NUM_SESSIONS = 180          # ~6 months of driving (1 session/day)
READINGS_PER_SESSION = 60   # 1 reading per minute → ~1 hour sessions

FUEL_TYPES = ["e20", "diesel"]   # E20 is now dominant petrol variant in India
ROAD_TYPES = ["city", "highway", "expressway", "offroad"]
DRIVE_MODES = ["eco", "normal", "sport", "offroad", "snow"]
TRAFFIC_LEVELS = ["free", "moderate", "heavy", "standstill"]

# Indian seasonal temps (monthly avg for Delhi/Gurugram area)
MONTHLY_TEMPS = {
    1: (8, 22),   2: (10, 25),  3: (15, 32),  4: (22, 40),
    5: (28, 45),  6: (28, 40),  7: (27, 36),  8: (26, 35),
    9: (24, 34),  10: (18, 33), 11: (12, 28), 12: (8, 22),
}

# ── Helper functions ──────────────────────────────────────────────────────────

def clamp(val, lo, hi):
    return max(lo, min(hi, val))

def noisy(val, noise=0.03):
    """Add small random noise to a value."""
    return val * (1 + random.uniform(-noise, noise))

def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]

def get_ambient_temp(dt):
    lo, hi = MONTHLY_TEMPS[dt.month]
    hour = dt.hour
    # Cooler at night, peak heat ~3pm
    hour_factor = math.sin(math.pi * (hour - 6) / 12) if 6 <= hour <= 18 else -0.2
    base = lo + (hi - lo) * 0.5
    return round(base + (hi - lo) * 0.3 * hour_factor + random.uniform(-2, 2), 1)

def get_aqi(dt, road_type):
    # Delhi AQI peaks Oct–Jan (pollution season), lower in monsoon
    seasonal = {1: 180, 2: 140, 3: 110, 4: 90, 5: 85, 6: 75,
                7: 60,  8: 55,  9: 65,  10: 130, 11: 200, 12: 210}
    base = seasonal[dt.month]
    road_mult = {"city": 1.2, "highway": 0.7, "expressway": 0.8, "offroad": 0.6}
    return clamp(int(base * road_mult[road_type] + random.randint(-20, 20)), 0, 500)

# ── Session-level state ────────────────────────────────────────────────────────

class VehicleState:
    """Tracks the persistent state of the vehicle across sessions."""

    def __init__(self):
        self.fuel_level = random.uniform(40, 95)
        self.oil_age_days = random.randint(0, 90)
        self.oil_km_used = random.uniform(0, 8000)
        self.total_km = random.uniform(15000, 45000)   # odometer
        self.total_km_on_tyres = random.uniform(5000, 35000)
        self.ac_filter_age_days = random.randint(0, 300)
        self.fuel_age_days = random.randint(0, 30)   # days since last refuel
        self.battery_health = random.uniform(0.80, 1.0)  # 1.0 = new
        self.fuel_type = weighted_choice(FUEL_TYPES, [0.90, 0.10])   # 90% E20 (mid-range petrol), 10% diesel

    def oil_quality(self):
        """Oil degrades with km and age. Petrol ~5000km, Diesel ~7500km interval."""
        km_limit = 5000 if self.fuel_type == "e20" else 7500
        quality = 100 - (self.oil_km_used / km_limit * 70) - (self.oil_age_days / 90 * 30)
        return clamp(round(quality, 1), 0, 100)

    def tyre_tread(self):
        """New tyre = 8mm. Wears roughly 1mm per 10,000km."""
        return clamp(round(8.0 - self.total_km_on_tyres / 10000, 2), 0, 8.0)

    def advance(self, trip_km, elapsed_days=1):
        self.fuel_level -= trip_km * random.uniform(0.008, 0.015)   # consumption
        self.fuel_level = clamp(self.fuel_level, 5, 100)
        if self.fuel_level < 15:
            self.fuel_level = random.uniform(70, 95)   # refuelled
            self.fuel_age_days = 0   # reset age on refuel
        self.oil_age_days += elapsed_days
        self.oil_km_used += trip_km
        if self.oil_km_used > 5500:                    # oil changed
            self.oil_age_days = 0
            self.oil_km_used = 0
        self.total_km += trip_km
        self.total_km_on_tyres += trip_km
        if self.total_km_on_tyres > 55000:             # tyres replaced
            self.total_km_on_tyres = random.uniform(0, 500)
        self.ac_filter_age_days += elapsed_days
        self.fuel_age_days += elapsed_days
        if self.ac_filter_age_days > 350:
            self.ac_filter_age_days = 0


# ── Per-reading generator ──────────────────────────────────────────────────────

def generate_reading(vs: VehicleState, session_meta: dict, minute: int) -> dict:
    """Generate a single sensor reading for a given minute in a session."""

    road = session_meta["road_type"]
    mode = session_meta["drive_mode"]
    traffic = session_meta["traffic_level"]
    dt = session_meta["start_time"] + timedelta(minutes=minute)
    ambient_temp = session_meta["ambient_temp"]

    # ── Speed profile based on road + traffic ──────────────────────────────
    speed_profiles = {
        ("city",       "free"):      (30, 55),
        ("city",       "moderate"):  (15, 35),
        ("city",       "heavy"):     (5,  20),
        ("city",       "standstill"):(0,  8),
        ("highway",    "free"):      (80, 120),
        ("highway",    "moderate"):  (60, 90),
        ("highway",    "heavy"):     (40, 65),
        ("expressway", "free"):      (100, 140),
        ("expressway", "moderate"):  (80, 110),
        ("expressway", "heavy"):     (60, 85),
        ("offroad",    "free"):      (15, 45),
        ("offroad",    "moderate"):  (10, 30),
    }
    lo_spd, hi_spd = speed_profiles.get((road, traffic), (20, 60))

    if mode == "sport":
        hi_spd = min(hi_spd * 1.15, 200)
    elif mode == "eco":
        hi_spd = hi_spd * 0.9
    elif mode == "offroad":
        hi_spd = min(hi_spd, 50)

    speed = round(noisy(random.uniform(lo_spd, hi_spd), 0.05), 1)

    # ── Engine ────────────────────────────────────────────────────────────
    rpm_base = 800 + speed * 25
    if mode == "sport":    rpm_base *= 1.2
    if mode == "eco":      rpm_base *= 0.88
    if mode == "offroad":  rpm_base *= 1.1
    engine_rpm = clamp(int(noisy(rpm_base, 0.08)), 700, 7000)

    engine_load = clamp(round(20 + speed * 0.4 + random.uniform(-5, 10), 1), 5, 100)
    if mode == "sport": engine_load = min(engine_load * 1.2, 100)

    # Engine warms up over first 10 minutes, then stabilises
    warm_up_factor = min(minute / 10, 1.0)
    engine_temp = clamp(round(
        (75 + engine_load * 0.2 + ambient_temp * 0.05) * warm_up_factor + 60 * (1 - warm_up_factor)
        + random.uniform(-2, 2), 1), 60, 130)

    oil_temp = clamp(round(engine_temp + random.uniform(5, 20), 1), 60, 150)

    # ── Fuel consumption ──────────────────────────────────────────────────
    base_consumption = 6.25  # L/100km baseline — E20 uses ~4% more volume vs pure petrol
    if vs.fuel_type == "diesel": base_consumption = 5.0
    if mode == "sport":    base_consumption *= 1.25
    if mode == "eco":      base_consumption *= 0.85
    if mode == "offroad":  base_consumption *= 1.35
    if traffic in ("heavy", "standstill"): base_consumption *= 1.4
    # AC load
    ac_on = ambient_temp > 26 or random.random() < 0.3
    if ac_on: base_consumption *= 1.08

    instant_consumption = clamp(round(noisy(base_consumption, 0.15), 2), 0, 30)
    avg_consumption = clamp(round(noisy(base_consumption, 0.05), 2), 0, 20)

    # E20 fuel quality: degrades faster due to ethanol moisture absorption
    # Safe window ~45 days; beyond that quality drops noticeably
    age_penalty = max(0, (vs.fuel_age_days - 45) * 0.8) if vs.fuel_type == "e20" else max(0, (vs.fuel_age_days - 90) * 0.4)
    humidity_penalty = (session_meta.get("humidity", 60) - 60) * 0.05 if vs.fuel_type == "e20" else 0
    bad_pump_penalty = random.uniform(5, 15) if random.random() < 0.08 else 0   # 8% chance of bad pump
    fuel_quality = clamp(round(97 - age_penalty - humidity_penalty - bad_pump_penalty, 1), 45, 100)

    # Ethanol blend variation (pumps vary ±2-3% from E20 target)
    ethanol_blend = clamp(round(20 + random.uniform(-2.5, 2.5), 1), 15, 23) if vs.fuel_type == "e20" else 0.0

    # Moisture risk
    if vs.fuel_type == "e20":
        if vs.fuel_age_days > 45 or session_meta.get("humidity", 60) > 75:
            moisture_risk = "high"
        elif vs.fuel_age_days > 25 or session_meta.get("humidity", 60) > 60:
            moisture_risk = "medium"
        else:
            moisture_risk = "low"
    else:
        moisture_risk = "low"

    # ── Tyres ─────────────────────────────────────────────────────────────
    base_pressure = 33.0
    tyre_temp = clamp(round(ambient_temp + 15 + speed * 0.12 + random.uniform(-2, 2), 1), 20, 90)

    def tyre_p(offset=0):
        # Natural variation + slight loss over time
        age_loss = vs.total_km_on_tyres / 50000 * 3
        return clamp(round(noisy(base_pressure + offset - age_loss, 0.02), 1), 20, 50)

    # ── Aerodynamics ──────────────────────────────────────────────────────
    # Windows: people open them at low speed in city, close on highway
    if speed < 40 and ambient_temp > 28 and not ac_on:
        window_fl = round(random.uniform(30, 80), 1)
        window_fr = round(random.uniform(20, 70), 1)
        window_rl = round(random.uniform(0, 50), 1)
        window_rr = round(random.uniform(0, 50), 1)
    elif speed > 70:
        window_fl = round(random.uniform(0, 15), 1)
        window_fr = round(random.uniform(0, 15), 1)
        window_rl = 0.0
        window_rr = 0.0
    else:
        window_fl = round(random.uniform(0, 40), 1)
        window_fr = round(random.uniform(0, 40), 1)
        window_rl = round(random.uniform(0, 20), 1)
        window_rr = round(random.uniform(0, 20), 1)

    sunroof = round(random.uniform(0, 30), 1) if ambient_temp < 35 and speed < 80 else 0.0

    # Drag score: penalise open windows at high speed
    avg_window_open = (window_fl + window_fr + window_rl + window_rr) / 4
    drag_penalty = (avg_window_open / 100) * (speed / 140) * 40  # max 40pt penalty
    aero_score = clamp(round(100 - drag_penalty, 1), 0, 100)

    # Mirror angles — slight inward tilt at high speed is better
    mirror_l = round(random.uniform(-5, 5), 1)
    mirror_r = round(random.uniform(-5, 5), 1)

    # ── Battery ───────────────────────────────────────────────────────────
    alt_output = round(noisy(14.2 * vs.battery_health, 0.02), 2)
    batt_voltage = round(noisy(12.6 * vs.battery_health + (alt_output - 12.6) * 0.3, 0.01), 2)

    # ── Cabin / AQI ──────────────────────────────────────────────────────
    cabin_temp = clamp(round(
        ambient_temp - (8 if ac_on else 0) + random.uniform(-1, 2), 1), 15, 50)
    aqi = get_aqi(dt, road)
    ac_recirc = aqi > 150   # auto recirculation on bad air days

    # ── Driving behaviour ─────────────────────────────────────────────────
    accel = round(random.uniform(-3, 3) if traffic != "standstill" else random.uniform(-1, 1), 2)
    lateral = round(random.uniform(-0.4, 0.4) if road != "offroad" else random.uniform(-0.8, 0.8), 2)
    if mode == "sport":
        accel = round(accel * 1.5, 2)
        lateral = round(lateral * 1.4, 2)

    # ── Gear estimation ───────────────────────────────────────────────────
    if speed < 10:   gear = 1
    elif speed < 25: gear = 2
    elif speed < 45: gear = 3
    elif speed < 65: gear = 4
    elif speed < 90: gear = 5
    else:            gear = 6

    trip_km_so_far = round(sum([
        random.uniform(0.3, 1.2) for _ in range(minute)
    ]), 2)

    return {
        "session_id":               session_meta["session_id"],
        "timestamp":                dt.strftime("%Y-%m-%d %H:%M:%S"),
        "trip_km":                  trip_km_so_far,
        "engine_rpm":               engine_rpm,
        "engine_temp_c":            engine_temp,
        "engine_load_pct":          engine_load,
        "oil_temp_c":               oil_temp,
        "oil_quality_pct":          vs.oil_quality(),
        "oil_age_days":             vs.oil_age_days,
        "oil_km_used":              round(vs.oil_km_used, 1),
        "fuel_level_pct":           round(vs.fuel_level, 1),
        "fuel_type":                vs.fuel_type,
        "ethanol_blend_pct":        ethanol_blend,
        "fuel_consumption_instant": instant_consumption,
        "fuel_consumption_avg":     avg_consumption,
        "fuel_energy_efficiency":   round(clamp(100 / (avg_consumption * 34.2 / 28.5 if vs.fuel_type == "e20" else avg_consumption * 34.2), 0, 5), 3),
        "fuel_quality_score":       fuel_quality,
        "fuel_moisture_risk":       moisture_risk,
        "fuel_age_days":            vs.fuel_age_days,
        "tyre_pressure_fl":         tyre_p(0),
        "tyre_pressure_fr":         tyre_p(0.3),
        "tyre_pressure_rl":         tyre_p(-0.2),
        "tyre_pressure_rr":         tyre_p(0.1),
        "tyre_temp_avg_c":          tyre_temp,
        "tyre_tread_depth_mm":      vs.tyre_tread(),
        "total_km_on_tyres":        round(vs.total_km_on_tyres, 1),
        "speed_kmph":               speed,
        "acceleration":             accel,
        "lateral_g":                lateral,
        "window_fl_pct":            window_fl,
        "window_fr_pct":            window_fr,
        "window_rl_pct":            window_rl,
        "window_rr_pct":            window_rr,
        "sunroof_open_pct":         sunroof,
        "mirror_angle_l":           mirror_l,
        "mirror_angle_r":           mirror_r,
        "aero_drag_score":          aero_score,
        "drive_mode":               mode,
        "gear":                     gear,
        "ac_on":                    ac_on,
        "ac_temp_set_c":            round(random.uniform(18, 24), 1) if ac_on else None,
        "ambient_temp_c":           ambient_temp,
        "humidity_pct":             round(random.uniform(30, 90), 1),
        "road_type":                road,
        "traffic_level":            traffic,
        "aqi":                      aqi,
        "battery_voltage":          batt_voltage,
        "alternator_output":        alt_output,
        "cabin_temp_c":             cabin_temp,
        "ac_filter_age_days":       vs.ac_filter_age_days,
        "ac_recirculation":         ac_recirc,
    }


# ── Main generator ─────────────────────────────────────────────────────────────

def generate_dataset(num_sessions=NUM_SESSIONS):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    vs = VehicleState()
    all_rows = []

    start_date = datetime(2024, 6, 1, 7, 30)

    for day_num in range(num_sessions):
        session_dt = start_date + timedelta(days=day_num)
        ambient = get_ambient_temp(session_dt)

        # Realistic Indian driving week: weekday = city commute, weekend = mixed
        is_weekend = session_dt.weekday() >= 5
        if is_weekend:
            road = weighted_choice(["city", "highway", "expressway", "offroad"],
                                   [0.3, 0.35, 0.25, 0.1])
        else:
            road = weighted_choice(["city", "highway", "expressway", "offroad"],
                                   [0.55, 0.25, 0.18, 0.02])

        traffic = weighted_choice(
            ["free", "moderate", "heavy", "standstill"],
            [0.15, 0.30, 0.35, 0.20] if road == "city" else [0.40, 0.35, 0.20, 0.05]
        )

        mode = weighted_choice(
            ["eco", "normal", "sport", "offroad"],
            [0.25, 0.50, 0.20, 0.05] if road != "offroad" else [0.05, 0.20, 0.10, 0.65]
        )

        lo_t, hi_t = MONTHLY_TEMPS[session_dt.month]
        # Monsoon months (Jun-Sep) have high humidity
        humidity_base = 80 if session_dt.month in (6,7,8,9) else 45
        session_humidity = clamp(humidity_base + random.randint(-10, 10), 20, 95)

        session_meta = {
            "session_id":   str(uuid4())[:8],
            "start_time":   session_dt,
            "road_type":    road,
            "traffic_level": traffic,
            "drive_mode":   mode,
            "ambient_temp": ambient,
            "humidity":     session_humidity,
            "day_num":      day_num,
        }

        trip_km = 0
        for minute in range(READINGS_PER_SESSION):
            row = generate_reading(vs, session_meta, minute)
            trip_km += random.uniform(0.3, 1.2)
            all_rows.append(row)

        vs.advance(trip_km, elapsed_days=1)

    # Write CSV
    csv_path = os.path.join(OUTPUT_DIR, "vehicle_data.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
        writer.writeheader()
        writer.writerows(all_rows)

    # Write a small sample as JSON for inspection
    json_path = os.path.join(OUTPUT_DIR, "sample_10.json")
    with open(json_path, "w") as f:
        json.dump(all_rows[:10], f, indent=2)

    print(f"✅ Generated {len(all_rows):,} readings across {num_sessions} sessions")
    print(f"   → {csv_path}")
    print(f"   → {json_path} (sample)")
    return csv_path


if __name__ == "__main__":
    generate_dataset()
