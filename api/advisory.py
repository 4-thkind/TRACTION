import pandas as pd
from typing import Dict, Any

def get_engine_data(row: pd.Series) -> Dict[str, Any]:
    temp = row.get("engine_temp_c", 88)
    load = row.get("engine_load_pct", 38)
    rpm = row.get("engine_rpm", 820)
    
    if 80 <= temp <= 95:
        tagline = 'Running healthy · Coolant temp normal'
        heroBg = 'linear-gradient(135deg,#f0fdf4,#dcfce7)'
        badgeTxt = 'Normal range'
        badgeBg = '#dcfce7'
        badgeCol = '#15803d'
        insight = '<strong>Healthy operating range is 80–95°C.</strong> E20 fuel burns slightly cooler than pure petrol — the temperature reading is normal and expected.'
        body = f'Engine load at {load:.0f}% is comfortable for current driving. Coolant is circulating correctly. No overheating risk detected.'
    elif temp > 95:
        tagline = 'Running hot · Coolant temp high'
        heroBg = 'linear-gradient(135deg,#fff5f5,#ffe8e8)'
        badgeTxt = 'Overheating Risk'
        badgeBg = '#ffe4e4'
        badgeCol = '#dc2626'
        insight = '<strong>Temperature is above healthy range (80–95°C).</strong> Pull over safely and let the engine cool down. Check coolant levels if possible.'
        body = f'Engine load is at {load:.0f}%. The coolant temperature of {temp:.0f}°C exceeds safe limits. Running at this temperature can damage the engine.'
    else:
        tagline = 'Running cool · Engine warming up'
        heroBg = 'linear-gradient(135deg,#f0f7ff,#dbeafe)'
        badgeTxt = 'Warming up'
        badgeBg = '#dbeafe'
        badgeCol = '#1d4ed8'
        insight = '<strong>Engine is below optimal temp (80–95°C).</strong> Avoid aggressive acceleration until it warms up.'
        body = f'Engine load is at {load:.0f}%. The coolant temperature is {temp:.0f}°C, which is typical for cold starts.'

    return {
        "name": 'Engine',
        "icon": '🔥',
        "tagline": tagline,
        "heroBg": heroBg,
        "badgeTxt": badgeTxt,
        "badgeBg": badgeBg,
        "badgeCol": badgeCol,
        "metrics": [
            {"l": 'Coolant Temp', "v": f'{temp:.0f}°C', "c": '#ef4444' if temp > 95 else '#22c55e'},
            {"l": 'Engine Load', "v": f'{load:.0f}%', "c": '#22c55e'},
            {"l": 'RPM', "v": f'{rpm:.0f}', "c": '#22c55e'},
            {"l": 'Throttle Pos', "v": '22%', "c": '#22c55e'}
        ],
        "insight": insight,
        "body": body,
        "actions": [{"l": 'Engine Health Report', "p": True}, {"l": 'View Temp History', "p": False}]
    }

def get_fuel_data(row: pd.Series) -> Dict[str, Any]:
    level = row.get("fuel_level_pct", 63)
    age = row.get("fuel_age_days", 38)
    blend = row.get("ethanol_blend_pct", 19.8)
    score = row.get("fuel_quality_score", 81)

    if age > 45:
        tagline = 'Warning · Ethanol blend is old'
        heroBg = 'linear-gradient(135deg,#fff5f5,#ffe8e8)'
        badgeTxt = f'Aged — {age:.0f} days'
        badgeBg = '#ffe4e4'
        badgeCol = '#dc2626'
        insight = '<strong>Refuel immediately.</strong> E20 ethanol absorbs moisture from air — safe window is ~45 days. The fuel is past its safe storage window.'
    elif age > 30:
        tagline = 'Watch · Ethanol blend approaching age limit'
        heroBg = 'linear-gradient(135deg,#fffbef,#fef3c7)'
        badgeTxt = f'Watch — {age:.0f} days'
        badgeBg = '#fef3c7'
        badgeCol = '#d97706'
        insight = '<strong>Refuel within 7 days.</strong> E20 ethanol absorbs moisture from air — safe window is ~45 days. Humidity is accelerating degradation.'
    else:
        tagline = 'Healthy · Fuel quality is good'
        heroBg = 'linear-gradient(135deg,#f0fdf4,#dcfce7)'
        badgeTxt = 'Good Quality'
        badgeBg = '#dcfce7'
        badgeCol = '#15803d'
        insight = '<strong>Fuel is fresh.</strong> E20 ethanol is within its 45-day safe storage window. No moisture risk detected.'

    return {
        "name": 'E20 Fuel',
        "icon": '⛽',
        "tagline": tagline,
        "heroBg": heroBg,
        "badgeTxt": badgeTxt,
        "badgeBg": badgeBg,
        "badgeCol": badgeCol,
        "metrics": [
            {"l": 'Fuel Level', "v": f'{level:.0f}%', "c": '#f59e0b' if level < 20 else '#22c55e'},
            {"l": 'Fuel Age', "v": f'{age:.0f} days', "c": '#ef4444' if age > 45 else ('#f59e0b' if age > 30 else '#22c55e')},
            {"l": 'Ethanol Blend', "v": f'{blend:.1f}%', "c": '#22c55e'},
            {"l": 'Quality Score', "v": f'{score:.0f}/100', "c": '#22c55e'}
        ],
        "insight": insight,
        "body": f'Tank is {level:.0f}% full. E20 blend is {age:.0f} days old — ethanol is hygroscopic and begins absorbing moisture beyond 45 days. Mileage reading ~4% lower than pure petrol is normal — it is the lower energy density of ethanol, not a fault.',
        "actions": [{"l": 'Find Nearest Pump', "p": True}, {"l": 'Set Refuel Reminder', "p": False}]
    }

def get_oil_data(row: pd.Series) -> Dict[str, Any]:
    quality = row.get("oil_quality_pct", 74)
    age = row.get("oil_age_days", 42)
    km = row.get("oil_km_used", 3820)
    temp = row.get("oil_temp_c", 96)

    if quality < 30:
        tagline = f'{quality:.0f}% quality remaining · Change required immediately'
        heroBg = 'linear-gradient(135deg,#fff5f5,#ffe8e8)'
        badgeTxt = 'Change Urgent'
        badgeBg = '#ffe4e4'
        badgeCol = '#dc2626'
        insight = '<strong>Immediate oil change recommended.</strong> E20 petrol engines use a 5,000 km / 90-day interval — your oil is severely degraded.'
    elif quality < 60:
        tagline = f'{quality:.0f}% quality remaining · Change coming up'
        heroBg = 'linear-gradient(135deg,#fff7ed,#ffedd5)'
        badgeTxt = 'Change Soon'
        badgeBg = '#ffedd5'
        badgeCol = '#c2410c'
        insight = f'<strong>Oil change recommended soon.</strong> You are at km {km:,.0f} and day {age:.0f} out of the 5,000 km / 90-day interval for E20 engines.'
    else:
        tagline = f'{quality:.0f}% quality remaining · Healthy condition'
        heroBg = 'linear-gradient(135deg,#f0fdf4,#dcfce7)'
        badgeTxt = 'Oil Healthy'
        badgeBg = '#dcfce7'
        badgeCol = '#15803d'
        insight = '<strong>Oil is in good condition.</strong> E20 engines require changes every 5,000 km / 90 days. You have plenty of life left.'

    return {
        "name": 'Engine Oil',
        "icon": '🛢️',
        "tagline": tagline,
        "heroBg": heroBg,
        "badgeTxt": badgeTxt,
        "badgeBg": badgeBg,
        "badgeCol": badgeCol,
        "metrics": [
            {"l": 'Oil Quality', "v": f'{quality:.0f}%', "c": '#ea580c' if quality < 60 else '#22c55e'},
            {"l": 'Oil Age', "v": f'{age:.0f} days', "c": '#f59e0b' if age > 75 else '#22c55e'},
            {"l": 'Km on Oil', "v": f'{km:,.0f}', "c": '#22c55e'},
            {"l": 'Oil Temp', "v": f'{temp:.0f}°C', "c": '#22c55e'}
        ],
        "insight": insight,
        "body": f'Oil quality index at {quality:.0f}% — the system flags below 60% as urgent. Oil temperature at {temp:.0f}°C is normal. No metal particle contamination detected.',
        "actions": [{"l": 'Schedule Oil Change', "p": True}, {"l": 'View Oil History', "p": False}]
    }

def get_tyres_data(row: pd.Series) -> Dict[str, Any]:
    fl = row.get("tyre_pressure_fl", 33.1)
    fr = row.get("tyre_pressure_fr", 33.4)
    rl = row.get("tyre_pressure_rl", 32.9)
    rr = row.get("tyre_pressure_rr", 33.2)
    depth = row.get("tyre_tread_depth_mm", 4.2)
    
    low_pressure = any(p < 30 for p in [fl, fr, rl, rr])
    worn = depth < 3.0

    if worn:
        tagline = 'Tyres worn · Replacement required'
        heroBg = 'linear-gradient(135deg,#fff5f5,#ffe8e8)'
        badgeTxt = 'Replace Tyres'
        badgeBg = '#ffe4e4'
        badgeCol = '#dc2626'
        insight = f'<strong>Tread depth is critically low at {depth:.1f}mm.</strong> Legal minimum in India is 1.6mm, but below 3mm drastically reduces monsoon grip. Replace soon.'
    elif low_pressure:
        tagline = 'Check Pressure · One or more tyres are low'
        heroBg = 'linear-gradient(135deg,#fff7ed,#ffedd5)'
        badgeTxt = 'Pressure Low'
        badgeBg = '#ffedd5'
        badgeCol = '#c2410c'
        insight = '<strong>Tyre pressure is below recommended 32–36 PSI.</strong> Low pressure reduces E20 mileage and increases wear. Top up at the next pump.'
    else:
        tagline = 'All four healthy · Pressure normal'
        heroBg = 'linear-gradient(135deg,#f0fdf4,#dcfce7)'
        badgeTxt = 'All four good'
        badgeBg = '#dcfce7'
        badgeCol = '#15803d'
        insight = '<strong>Rotation in ~5,000 km.</strong> Rotating front-to-rear evens wear and extends tyre life by up to 20%.'

    return {
        "name": 'Tyres',
        "icon": '🛞',
        "tagline": tagline,
        "heroBg": heroBg,
        "badgeTxt": badgeTxt,
        "badgeBg": badgeBg,
        "badgeCol": badgeCol,
        "metrics": [
            {"l": 'FL / FR', "v": f'{fl:.1f} / {fr:.1f}', "c": '#ef4444' if (fl<30 or fr<30) else '#22c55e'},
            {"l": 'RL / RR', "v": f'{rl:.1f} / {rr:.1f}', "c": '#ef4444' if (rl<30 or rr<30) else '#22c55e'},
            {"l": 'Tread Depth', "v": f'{depth:.1f} mm', "c": '#ef4444' if worn else '#22c55e'},
            {"l": 'Est. Life Left', "v": '~20k km', "c": '#22c55e'}
        ],
        "insight": insight,
        "body": f'Pressures are around ~{int(fl)} PSI — recommended is 32–36 PSI. Tread depth {depth:.1f}mm is healthy (new = 8mm, legal minimum India = 1.6mm).',
        "actions": [{"l": 'Set Rotation Reminder', "p": True}, {"l": 'Tyre Wear History', "p": False}]
    }

def get_aero_data(row: pd.Series) -> Dict[str, Any]:
    score = row.get("aero_drag_score", 91)
    speed = row.get("speed_kmph", 52)
    win_fl = row.get("window_fl_pct", 25)
    win_fr = row.get("window_fr_pct", 0)
    
    avg_win = (win_fl + win_fr) / 2
    high_drag = speed > 60 and avg_win > 20

    if high_drag:
        tagline = 'High drag · Inefficient at current speed'
        heroBg = 'linear-gradient(135deg,#fff7ed,#ffedd5)'
        badgeTxt = f'Score {score:.0f}/100'
        badgeBg = '#ffedd5'
        badgeCol = '#c2410c'
        insight = '<strong>Above 70 km/h:</strong> open windows create heavy drag. Close windows and use AC — it is more fuel-efficient at this speed.'
    else:
        tagline = 'Low drag · Efficient at current speed'
        heroBg = 'linear-gradient(135deg,#f0f7ff,#dbeafe)'
        badgeTxt = f'Score {score:.0f}/100'
        badgeBg = '#dbeafe'
        badgeCol = '#1d4ed8'
        insight = '<strong>Aerodynamics look good.</strong> Mirror angles are neutral and windows are appropriately managed for the current speed.'

    return {
        "name": 'Aerodynamics',
        "icon": '💨',
        "tagline": tagline,
        "heroBg": heroBg,
        "badgeTxt": badgeTxt,
        "badgeBg": badgeBg,
        "badgeCol": badgeCol,
        "metrics": [
            {"l": 'Aero Score', "v": f'{score:.0f}/100', "c": '#3b82f6'},
            {"l": 'Speed', "v": f'{speed:.0f} km/h', "c": '#7c3aed'},
            {"l": 'Windows Open', "v": f'{avg_win:.0f}%', "c": '#f59e0b'},
            {"l": 'Efficiency Loss', "v": '1.2%', "c": '#22c55e'}
        ],
        "insight": insight,
        "body": f'At {speed:.0f} km/h with windows {avg_win:.0f}% open, drag impact varies. Above 70 km/h, open windows create drag equivalent to 8–10 kg, cutting mileage by up to 6%.',
        "actions": [{"l": 'Enable Auto-close Windows', "p": True}, {"l": 'Optimise Mirror Angles', "p": False}]
    }

def process_row(row: pd.Series) -> Dict[str, Any]:
    return {
        "engine": get_engine_data(row),
        "fuel": get_fuel_data(row),
        "oil": get_oil_data(row),
        "tyres": get_tyres_data(row),
        "aero": get_aero_data(row)
    }
