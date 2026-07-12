import os
import random
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .advisory import process_row

app = FastAPI()

# Get the absolute path to the project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT_DIR, 'data', 'vehicle_data.csv')

# Load dataset into memory at startup
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    # fallback to sample_10.json if csv is not there
    df = pd.read_json(os.path.join(ROOT_DIR, 'data', 'sample_10.json'))

@app.get("/api/status")
def get_status():
    # Pick a random row to simulate "live" data changing
    row = df.sample(1).iloc[0]
    return process_row(row)

# Serve the main HTML file directly
@app.get("/")
def read_index():
    return FileResponse(os.path.join(ROOT_DIR, 'TRACTION.html'))

@app.get("/TRACTION.html")
def read_html():
    return FileResponse(os.path.join(ROOT_DIR, 'TRACTION.html'))

@app.get("/TRACTION.css")
def read_css():
    return FileResponse(os.path.join(ROOT_DIR, 'TRACTION.css'))

@app.get("/TRACTION.js")
def read_js():
    return FileResponse(os.path.join(ROOT_DIR, 'TRACTION.js'))

@app.get("/car.png")
def read_car_png():
    return FileResponse(os.path.join(ROOT_DIR, 'car.png'))
