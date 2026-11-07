
from fastapi import FastAPI
from database import initialize_database, client

from routes import buses, occupancy, sensors

app = FastAPI(
    title="DkIT Bus Tracker API",
    description="Backend API for the DkIT Bus Tracker IoT project",
    version="1.0.0"
)


@app.on_event("startup")
def startup_event():
    initialize_database()


@app.get("/")
def home():
    return {
        "message": "Welcome to DkIT Bus Tracker API",
        "status": "Backend is running"
    }


@app.get("/database")
def database_status():

    try:
        client.admin.command("ping")

        return {
            "message": "MongoDB connection successful",
            "database": "bus_tracker"
        }

    except Exception as e:
        return {
            "message": "MongoDB connection failed",
            "error": str(e)
        }


# Register API routes
app.include_router(buses.router)
app.include_router(occupancy.router)
app.include_router(sensors.router)
