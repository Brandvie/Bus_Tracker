
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import check_database_connection

from routes import buses
from routes import occupancy
from routes import sensors

app = FastAPI(
    title="DkIT Bus Tracker API",
    description="Backend API for the DkIT IoT Bus Tracker Alpha",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(buses.router)
app.include_router(occupancy.router)
app.include_router(sensors.router)


@app.get("/")
def home():

    return {
        "message": "Welcome to DkIT Bus Tracker API"
    }


@app.get("/database")
def database_status():

    if check_database_connection():

        return {
            "message": "MongoDB connected successfully"
        }

    return {
        "message": "MongoDB connection failed"
    }
