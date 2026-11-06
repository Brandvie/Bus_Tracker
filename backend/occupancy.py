
def calculate_occupancy(passenger_count, capacity):

    if capacity <= 0:
        raise ValueError("Capacity must be greater than zero")

    if passenger_count < 0:
        raise ValueError("Passenger count cannot be negative")

    if passenger_count > capacity:
        raise ValueError("Passenger count cannot exceed capacity")

    percentage = (passenger_count / capacity) * 100

    available_seats = capacity - passenger_count

    if percentage < 50:
        status = "Quiet"

    elif percentage < 100:
        status = "Busy"

    else:
        status = "Full"

    return {
        "passenger_count": passenger_count,
        "capacity": capacity,
        "occupancy_percentage": round(percentage),
        "available_seats": available_seats,
        "status": status
    }
