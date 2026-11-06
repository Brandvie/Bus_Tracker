
from fastapi import FastAPI
from database import client, database

app = FastAPI(title="DkIT Bus Tracker API")


@app.get("/")
def home():
    return {"message": "Bus Tracker API is running"}


@app.get("/database")
def test_database():
    try:
        client.admin.command("ping")

        return {
            "message": "MongoDB connected successfully",
            "database": database.name
        }

    except Exception as e:
        return {"error": str(e)}
