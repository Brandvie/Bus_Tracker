def calculate_occupancy(passenger_count):
    capacity = 25

    if passenger_count < 0:
        passenger_count = 0

    if passenger_count > capacity:
        passenger_count = capacity

    if passenger_count <= 10:
        status = "Quiet"

    elif passenger_count <= 20:
        status = "Normal amount"

    elif passenger_count < 25:
        status = "Busy"

    else:
        status = "Full"

    return {
        "current_passengers": passenger_count,
        "capacity": capacity,
        "crowd_status": status,
        "available_spaces": capacity - passenger_count
    }