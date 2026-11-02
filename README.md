# Bus Tracker – IoT Project

## Overview
Bus Tracker is an IoT-based application that allows passengers to check whether a bus is full or has available space before boarding. The application also displays bus stop locations on a map using Google Maps API.

The system uses two sensors connected to a Raspberry Pi installed on the bus to detect passengers entering and leaving. The Raspberry Pi calculates the current passenger count and sends the data to a backend system, where it is stored in MongoDB.

The driver will receive a notification or alert when the bus reaches its maximum capacity, allowing them to monitor overcrowding.


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
