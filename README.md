# 🏎️ TRACTION
> **T**elemetry-based **R**eal-time **A**utomotive **C**ondition **T**racking, **I**ntelligence, **O**ptimization & **N**avigation

### An ML-Powered Co-Pilot for Indian Mid-Range Car Drivers

TRACTION is a vehicle intelligence assistant that translates raw telemetry and sensor data into actionable advice for everyday drivers. Instead of presenting raw metrics or cryptic error codes, the system processes data—such as E20 fuel degradation, aerodynamic drag, and tyre wear—and outputs straightforward recommendations to keep the vehicle running efficiently.

---

## Key Features

- **Engine Health:** Real-time monitoring of coolant temperatures, load, and RPMs to detect overheating and cold-start inefficiencies.
- **E20 Fuel Intelligence:** Tracks ethanol blend aging (hygroscopic moisture absorption) and advises on optimal refueling windows.
- **Tyre & Aero Optimization:** Calculates aerodynamic drag based on vehicle speed and window positions. Monitors tread depth and pressure tailored specifically for Indian road conditions.
- **Oil Life Tracking:** Predicts engine oil degradation using driven kilometers, oil age, and operating temperatures.
- **Dashboard UI:** A responsive, dark-themed dashboard featuring real-time data updates and targeted driver insights.

---

## Architecture & Tech Stack

TRACTION is built on a lightweight, high-performance web stack:

- **Backend:** FastAPI (Python)
- **Data Processing:** Pandas (handles telemetry processing and advisory logic)
- **Frontend:** Vanilla HTML5, CSS3, and JavaScript
- **Data Source:** Synthetic Indian driving dataset generator (10,800 readings across 180 sessions)

---

## Quick Start

You can get the TRACTION dashboard running locally in a few steps.

### 1. Prerequisites
Ensure you have Python 3.8 or higher installed on your system.

```bash
# Clone the repository
git clone https://github.com/4-thkind/TRACTION.git
cd TRACTION

# Install required Python packages
pip install fastapi "uvicorn[standard]" pandas numpy
```

### 2. Run the Server
Launch the FastAPI backend server:

```bash
uvicorn api.main:app --reload
```

### 3. Open the Dashboard
Navigate to [http://localhost:8000](http://localhost:8000) in your web browser. 

> **Note:** The frontend automatically simulates a live vehicle data feed by polling the `/api/status` endpoint to update the dashboard in real-time.

---

## Project Structure

```text
TRACTION/
├── api/
│   ├── main.py             # FastAPI server and route definitions
│   └── advisory.py         # Core business logic and health evaluation engine
├── data/
│   ├── generate_data.py    # Script to generate synthetic Indian driving data
│   ├── vehicle_data.csv    # The generated telemetry dataset
│   └── sample_10.json      # Fallback data sample
├── utils/
│   └── explorer.py         # CLI tool for Exploratory Data Analysis (EDA)
├── TRACTION.html           # Main dashboard layout
├── TRACTION.css            # Custom design system and styling
└── TRACTION.js             # Frontend logic and API integration
```

---

## Design Principles

1. **Plain Language First:** Every sensor reading is translated into a sentence a non-mechanic can immediately understand.
2. **Indian Context:** The advisory engine is tuned for local conditions, including E20 fuel availability, monsoon tyre grip, AQI thresholds, and high ambient temperatures.
3. **Actionable Insights:** Alerts include direct recommendations, such as "Roll up windows above 70km/h to reduce drag," rather than just reporting the drag coefficient.
4. **Non-Alarmist:** The system distinguishes clearly between critical issues that require immediate attention and minor issues to keep an eye on.
