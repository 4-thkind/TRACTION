"""
Vehicle Assistant — Data Schema
Defines every sensor field, its unit, valid range, and description.
This is the single source of truth for what data the system expects.
"""

SENSOR_SCHEMA = {

    # ── Identification ───────────────────────────────────────────────────────
    "session_id":       {"type": "str",   "unit": None,    "desc": "Unique driving session ID"},
    "timestamp":        {"type": "datetime","unit": None,  "desc": "ISO timestamp of reading"},
    "trip_km":          {"type": "float", "unit": "km",    "range": (0, 9999),   "desc": "Distance covered in current trip"},

    # ── Engine ───────────────────────────────────────────────────────────────
    "engine_rpm":       {"type": "int",   "unit": "RPM",   "range": (0, 7000),   "desc": "Engine revolutions per minute"},
    "engine_temp_c":    {"type": "float", "unit": "°C",    "range": (60, 130),   "desc": "Engine coolant temperature"},
    "engine_load_pct":  {"type": "float", "unit": "%",     "range": (0, 100),    "desc": "Engine load percentage"},
    "oil_temp_c":       {"type": "float", "unit": "°C",    "range": (60, 150),   "desc": "Engine oil temperature"},
    "oil_quality_pct":  {"type": "float", "unit": "%",     "range": (0, 100),    "desc": "Oil quality remaining (100=new, 0=change now)"},
    "oil_age_days":     {"type": "int",   "unit": "days",  "range": (0, 365),    "desc": "Days since last oil change"},
    "oil_km_used":      {"type": "float", "unit": "km",    "range": (0, 15000),  "desc": "KM driven on current oil"},

    # ── Fuel (E20 — 20% ethanol blend, primary Indian fuel) ──────────────────
    "fuel_level_pct":           {"type": "float", "unit": "%",      "range": (0, 100),  "desc": "Fuel tank level percentage"},
    "fuel_type":                {"type": "str",   "unit": None,     "desc": "e20 / diesel / cng / electric"},
    "ethanol_blend_pct":        {"type": "float", "unit": "%",      "range": (0, 25),   "desc": "Actual ethanol blend % (E20 target = 20%; varies pump to pump)"},
    "fuel_consumption_instant": {"type": "float", "unit": "L/100km","range": (0, 30),   "desc": "Instantaneous consumption — E20 uses ~4% more volume vs pure petrol due to lower energy density"},
    "fuel_consumption_avg":     {"type": "float", "unit": "L/100km","range": (0, 20),   "desc": "Trip average fuel consumption"},
    "fuel_energy_efficiency":   {"type": "float", "unit": "km/MJ",  "range": (0, 5),    "desc": "Energy-normalised efficiency — removes blend-% distortion for fair comparison"},
    "fuel_quality_score":       {"type": "float", "unit": "score",  "range": (0, 100),  "desc": "E20 quality: penalises moisture absorption, phase separation, and storage age"},
    "fuel_moisture_risk":       {"type": "str",   "unit": None,     "desc": "low/medium/high — ethanol is hygroscopic; risk rises with humidity + idle days"},
    "fuel_age_days":            {"type": "int",   "unit": "days",   "range": (0, 90),   "desc": "Days since last refuel — E20 safe window ~45 days (vs ~90 for pure petrol)"},

    # ── Tyres ─────────────────────────────────────────────────────────────────
    "tyre_pressure_fl": {"type": "float", "unit": "PSI",   "range": (20, 50),    "desc": "Front-left tyre pressure"},
    "tyre_pressure_fr": {"type": "float", "unit": "PSI",   "range": (20, 50),    "desc": "Front-right tyre pressure"},
    "tyre_pressure_rl": {"type": "float", "unit": "PSI",   "range": (20, 50),    "desc": "Rear-left tyre pressure"},
    "tyre_pressure_rr": {"type": "float", "unit": "PSI",   "range": (20, 50),    "desc": "Rear-right tyre pressure"},
    "tyre_temp_avg_c":  {"type": "float", "unit": "°C",    "range": (20, 90),    "desc": "Average tyre surface temperature"},
    "tyre_tread_depth_mm": {"type": "float","unit": "mm",  "range": (0, 8),      "desc": "Estimated tread depth (new=8mm, legal min=1.6mm)"},
    "total_km_on_tyres":   {"type": "float","unit": "km",  "range": (0, 60000),  "desc": "Total km driven on current tyres"},

    # ── Speed & Motion ────────────────────────────────────────────────────────
    "speed_kmph":       {"type": "float", "unit": "km/h",  "range": (0, 200),    "desc": "Current vehicle speed"},
    "acceleration":     {"type": "float", "unit": "m/s²",  "range": (-10, 10),   "desc": "Longitudinal acceleration (neg=braking)"},
    "lateral_g":        {"type": "float", "unit": "g",     "range": (-2, 2),     "desc": "Lateral G-force (cornering)"},

    # ── Aerodynamics & Body ───────────────────────────────────────────────────
    "window_fl_pct":    {"type": "float", "unit": "%",     "range": (0, 100),    "desc": "Front-left window open percentage"},
    "window_fr_pct":    {"type": "float", "unit": "%",     "range": (0, 100),    "desc": "Front-right window open percentage"},
    "window_rl_pct":    {"type": "float", "unit": "%",     "range": (0, 100),    "desc": "Rear-left window open percentage"},
    "window_rr_pct":    {"type": "float", "unit": "%",     "range": (0, 100),    "desc": "Rear-right window open percentage"},
    "sunroof_open_pct": {"type": "float", "unit": "%",     "range": (0, 100),    "desc": "Sunroof open percentage"},
    "mirror_angle_l":   {"type": "float", "unit": "°",     "range": (-30, 30),   "desc": "Left mirror tilt angle from neutral"},
    "mirror_angle_r":   {"type": "float", "unit": "°",     "range": (-30, 30),   "desc": "Right mirror tilt angle from neutral"},
    "aero_drag_score":  {"type": "float", "unit": "score", "range": (0, 100),    "desc": "Estimated aerodynamic efficiency (100=best)"},

    # ── Drive Mode & Transmission ─────────────────────────────────────────────
    "drive_mode":       {"type": "str",   "unit": None,    "desc": "eco / normal / sport / offroad / snow"},
    "gear":             {"type": "int",   "unit": None,    "range": (0, 8),      "desc": "Current gear (0=neutral/park)"},
    "ac_on":            {"type": "bool",  "unit": None,    "desc": "AC compressor active"},
    "ac_temp_set_c":    {"type": "float", "unit": "°C",    "range": (16, 30),    "desc": "AC set temperature"},

    # ── Environment ───────────────────────────────────────────────────────────
    "ambient_temp_c":   {"type": "float", "unit": "°C",    "range": (-5, 55),    "desc": "Outside air temperature"},
    "humidity_pct":     {"type": "float", "unit": "%",     "range": (0, 100),    "desc": "Ambient humidity percentage"},
    "road_type":        {"type": "str",   "unit": None,    "desc": "city / highway / offroad / expressway"},
    "traffic_level":    {"type": "str",   "unit": None,    "desc": "free / moderate / heavy / standstill"},
    "aqi":              {"type": "int",   "unit": "AQI",   "range": (0, 500),    "desc": "Air Quality Index at current location"},

    # ── Battery & Electrical ──────────────────────────────────────────────────
    "battery_voltage":  {"type": "float", "unit": "V",     "range": (11.5, 14.8),"desc": "12V battery voltage"},
    "alternator_output":{"type": "float", "unit": "V",     "range": (13.5, 14.8),"desc": "Alternator charging voltage"},

    # ── Cabin Air ─────────────────────────────────────────────────────────────
    "cabin_temp_c":     {"type": "float", "unit": "°C",    "range": (15, 50),    "desc": "Inside cabin temperature"},
    "ac_filter_age_days":{"type": "int",  "unit": "days",  "range": (0, 365),    "desc": "Days since AC cabin filter replacement"},
    "ac_recirculation": {"type": "bool",  "unit": None,    "desc": "AC on recirculation (True) or fresh air (False)"},
}

# ── Derived / Computed Fields (not from sensors, calculated by models) ────────
COMPUTED_FIELDS = {
    "health_score":         {"unit": "score/100", "desc": "Overall vehicle health score"},
    "efficiency_score":     {"unit": "score/100", "desc": "Current driving efficiency score"},
    "aero_efficiency_loss_pct": {"unit": "%",     "desc": "% efficiency lost due to aero drag"},
    "fuel_change_due_date": {"unit": "date",      "desc": "Predicted next engine oil change date"},
    "tyre_replace_km_left": {"unit": "km",        "desc": "Estimated km until tyre replacement needed"},
    "driving_style":        {"unit": "label",     "desc": "calm / moderate / aggressive"},
}

# ── Recommended value ranges for Indian mid-range cars ───────────────────────
HEALTHY_RANGES = {
    "engine_temp_c":     (80, 95),
    "tyre_pressure_fl":  (32, 36),
    "tyre_pressure_fr":  (32, 36),
    "tyre_pressure_rl":  (32, 36),
    "tyre_pressure_rr":  (32, 36),
    "tyre_tread_depth_mm": (3.0, 8.0),    # below 1.6mm is illegal
    "oil_quality_pct":   (30, 100),
    "battery_voltage":   (12.4, 14.8),
    "fuel_quality_score":(75, 100),     # E20 threshold slightly higher — moisture degrades it faster
    "ethanol_blend_pct": (18, 22),      # acceptable E20 band; outside = pump quality issue
    "fuel_age_days":     (0, 45),       # E20 safe storage window (ethanol absorbs moisture beyond this)
    "aqi":               (0, 100),         # above 150 = switch to recirculation
}

# ── E20 specific notes ───────────────────────────────────────────────────────
E20_PROFILE = {
    "energy_density_mj_per_l": 28.5,        # vs 32.0 for pure petrol — ~11% less energy
    "consumption_penalty_pct": 4.0,          # expect ~4% more litres used vs pure petrol
    "moisture_absorption": "high",           # hygroscopic — avoid leaving tank near-empty long term
    "safe_storage_days": 45,                 # degrade threshold vs 90 days for pure petrol
    "cold_start_note": "May need slightly longer cranking in winter below 10°C",
    "compatible_cars": "All BS6 compliant cars (2020+) are E20 compatible",
    "advisory_tip": (
        "E20 gives you cleaner emissions and supports Indian farmers, "
        "but fill up at least every 6 weeks to avoid moisture build-up. "
        "Your mileage will read ~4% lower than a pure petrol car — that is normal."
    ),
}

# ── Drive mode descriptions (used by advisory layer) ─────────────────────────
DRIVE_MODE_PROFILES = {
    "eco": {
        "throttle": "gentle",
        "gearshift": "early upshift to save fuel",
        "ac": "reduced output",
        "best_for": "city driving, daily commutes",
        "fuel_saving_vs_normal": "8-12%",
    },
    "normal": {
        "throttle": "balanced",
        "gearshift": "standard mapping",
        "ac": "normal output",
        "best_for": "everyday mixed driving",
        "fuel_saving_vs_normal": "0%",
    },
    "sport": {
        "throttle": "aggressive, instant response",
        "gearshift": "holds gears longer for power",
        "ac": "may reduce to prioritise engine",
        "best_for": "overtaking, hill climbs, open highways",
        "fuel_saving_vs_normal": "-15 to -25% (uses more fuel)",
    },
    "offroad": {
        "throttle": "controlled, crawl-speed management",
        "gearshift": "low gear lock, diff lock active",
        "ac": "normal",
        "best_for": "unpaved roads, mud, rocky terrain",
        "fuel_saving_vs_normal": "-20 to -35% (high load)",
    },
    "snow": {
        "throttle": "very gentle, anti-slip priority",
        "gearshift": "starts in 2nd gear to avoid wheel spin",
        "ac": "normal",
        "best_for": "icy/snowy roads, wet surfaces",
        "fuel_saving_vs_normal": "-5 to -10%",
    },
}
