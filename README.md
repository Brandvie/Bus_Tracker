# Bus Tracker – IoT Project

## Overview
Bus Tracker is an IoT system that monitors bus occupancy in real time. It uses door sensors and a Raspberry Pi to count passengers boarding and leaving the bus. It alerts the driver when the bus reaches or exceeds its capacity and allows passengers to check how crowded a bus is.

## Technologies
- **Hardware:** Raspberry Pi Zero 2 W, IR break-beam sensors, Motion sensor
- **Programming:** Python
- **Messaging:** MQTT over TLS
- **Backend:** FastAPI
- **Database:** SQLite
- **Frontend:** HTML, CSS and JavaScript
- **Version Control:** Git and GitHub

## Main Features
- Automatic passenger counting
- Live bus occupancy and crowd-level display
- Overcrowding alarm
- Recent boarding and alighting activity
- Wheelchair-space availability indicator

## Project Structure
```text
bus-tracker/
├── raspberry-pi/
├── backend/
├── frontend/
├── docs/
├── README.md
└── .gitignore
```

## Project Status
Currently in development as part of a Scrum-based student project at Dundalk Institute of Technology (DkIT).

## Privacy
The system counts passenger movements without identifying individual passengers.
