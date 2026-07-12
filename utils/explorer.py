"""
Vehicle Assistant — Data Explorer
Quick exploratory analysis of the generated dataset.
Run this to understand your data before building ML models.
"""

import pandas as pd
import numpy as np
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "vehicle_data.csv")


def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])
    return df


def health_flag(df):
    """Add simple health flag columns based on HEALTHY_RANGES."""
    df = df.copy()
    df["flag_engine_hot"]       = df["engine_temp_c"] > 95
    df["flag_oil_low"]          = df["oil_quality_pct"] < 30
    df["flag_tyre_low_fl"]      = df["tyre_pressure_fl"] < 30
    df["flag_tyre_low_fr"]      = df["tyre_pressure_fr"] < 30
    df["flag_tyre_low_rl"]      = df["tyre_pressure_rl"] < 30
    df["flag_tyre_low_rr"]      = df["tyre_pressure_rr"] < 30
    df["flag_tyre_worn"]        = df["tyre_tread_depth_mm"] < 3.0
    df["flag_bad_fuel"]         = df["fuel_quality_score"] < 70
    df["flag_battery_low"]      = df["battery_voltage"] < 12.4
    df["flag_high_aqi"]         = df["aqi"] > 150
    df["flag_aero_inefficient"] = (df["speed_kmph"] > 60) & (
        (df["window_fl_pct"] > 20) | (df["window_fr_pct"] > 20)
    )
    return df


def summary(df):
    df = health_flag(df)

    flag_cols = [c for c in df.columns if c.startswith("flag_")]
    print("=" * 60)
    print("  VEHICLE HEALTH SUMMARY")
    print("=" * 60)
    print(f"  Total readings : {len(df):,}")
    print(f"  Date range     : {df['timestamp'].min().date()} → {df['timestamp'].max().date()}")
    print(f"  Sessions       : {df['session_id'].nunique()}")
    print(f"  Fuel type      : {df['fuel_type'].mode()[0]}")
    print()
    print("  FLAG ANALYSIS (% of readings):")
    for col in flag_cols:
        pct = df[col].mean() * 100
        bar = "█" * int(pct / 2) + "░" * (50 - int(pct / 2))
        status = "⚠️ " if pct > 10 else "✅"
        print(f"  {status} {col:<30} {pct:5.1f}%  {bar[:20]}")

    print()
    print("  AVERAGES BY ROAD TYPE:")
    print(df.groupby("road_type")[[
        "fuel_consumption_avg", "speed_kmph", "engine_temp_c", "aero_drag_score"
    ]].mean().round(2).to_string())

    print()
    print("  AVERAGES BY DRIVE MODE:")
    print(df.groupby("drive_mode")[[
        "fuel_consumption_avg", "speed_kmph", "engine_load_pct"
    ]].mean().round(2).to_string())

    print()
    print("  SEASONAL FUEL CONSUMPTION (monthly avg):")
    df["month"] = df["timestamp"].dt.month
    monthly = df.groupby("month")["fuel_consumption_avg"].mean().round(2)
    for m, val in monthly.items():
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        bar = "█" * int(val * 3)
        print(f"  {months[m-1]}  {val:.2f} L/100km  {bar}")

    return df


if __name__ == "__main__":
    df = load_data()
    df_flagged = summary(df)
    print("\n✅ Data loaded. Shape:", df.shape)
