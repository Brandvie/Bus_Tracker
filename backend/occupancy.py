
def calculate_crowd_status(passengers):
    if passengers <= 10:
        return "Quiet"

    elif passengers <= 20:
        return "Normal"

    elif passengers < 25:
        return "Busy"

    else:
        return "Full"


def calculate_passenger_count(current, direction, quantity):
    if direction == "in":
        new_count = current + quantity

    elif direction == "out":
        new_count = current - quantity

    else:
        new_count = current

    
    new_count = max(0, new_count)

    
    new_count = min(25, new_count)

    return new_count
