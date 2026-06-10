# TRACTION
Telemetry-based Real-time Automotive Condition Tracking, Intelligence, Optimization &amp; Navigation

# 🚗 Vehicle Intelligence Assistant
### An ML-powered co-pilot for Indian mid-range car drivers

---

## What This Does
Translates raw vehicle sensor data into plain, actionable advice for everyday drivers —
covering fuel, tyres, engine health, aerodynamics, drive modes, cabin air quality, and more.

---

## Project Structure

```
vehicle_assistant/
│
├── config/
│   └── schema.py           ← All sensor fields, units, healthy ranges, drive mode profiles
│
├── data/
│   ├── generate_data.py    ← Synthetic Indian driving data generator
│   ├── vehicle_data.csv    ← Generated dataset (10,800 readings / 180 sessions)
│   └── sample_10.json      ← First 10 readings for quick inspection
│
├── models/                 ← (Phase 2) ML models go here
│   ├── fuel_model.py
│   ├── tyre_model.py
│   ├── engine_model.py
│   └── health_score.py
│
├── advisory/               ← (Phase 3) Plain-language advisory engine
│   ├── rules.py
│   └── llm_advisor.py
│
├── dashboard/              ← (Phase 4) Streamlit dashboard
│   └── app.py
│
└── utils/
    └── explorer.py         ← EDA / health flag analysis tool
```

---

## Phase Status

| Phase | What | Status |
|-------|------|--------|
| 1 | Data Schema + Synthetic Generator | ✅ Complete |
| 2 | ML Models (fuel, tyres, engine, health) | 🔜 Next |
| 3 | Advisory Language Layer | 🔜 Upcoming |
| 4 | Dashboard + Calendar Sync | 🔜 Upcoming |

---

## Dataset Overview

- **10,800 readings** across 180 driving sessions (~6 months)
- **47 sensor fields** per reading
- Simulates realistic Indian driving: Gurugram/Delhi city, NH48 highway, expressway, off-road
- Seasonal temperature and AQI variation (Delhi pollution season modelled)
- Covers: city commutes, weekend highway runs, off-road sessions
- Drive modes: eco, normal, sport, offroad

### Key Sensor Groups
| Group | Fields |
|-------|--------|
| Engine | rpm, temp, load, oil quality/age/km |
| Fuel | level, type, instant/avg consumption, quality score |
| Tyres | pressure x4, temperature, tread depth, total km |
| Aerodynamics | windows x4, sunroof, mirror angles, drag score |
| Environment | ambient temp, humidity, AQI, road type, traffic |
| Cabin | cabin temp, AC state, filter age, recirculation |
| Electrical | battery voltage, alternator output |

---

## Quick Start

```bash
# 1. Install dependencies
pip install pandas numpy scikit-learn

# 2. Regenerate data (optional)
python data/generate_data.py

# 3. Explore the data
python utils/explorer.py
```

---

## Design Principles

- **Plain language first** — every ML output must translate to a sentence a non-mechanic understands
- **Indian context** — AQI thresholds, fuel adulteration patterns, seasonal temps, traffic patterns
- **Actionable** — every alert must include a recommended action, not just a warning number
- **Non-alarmist** — distinguish between "fix today" and "keep an eye on this"
