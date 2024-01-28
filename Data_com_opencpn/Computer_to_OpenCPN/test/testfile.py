import math
import random


def generate_and_update_coordinates(coordinates, max_points=2):
    """
    Generate a new (x, y) coordinate and update the list of coordinates.
    Ensures that the list contains at most `max_points`.

    Parameters:
    coordinates (list): The current list of coordinates.
    max_points (int): The maximum number of points allowed in the list.

    Returns:
    list: The updated list of coordinates.
    """
    # Generate a new random coordinate
    new_coordinate = (random.uniform(0, 100), random.uniform(0, 100))

    # Add the new coordinate to the list
    coordinates.append(new_coordinate)

    # Ensure the list has at most `max_points` elements
    while len(coordinates) > max_points:
        coordinates.pop(0)  # Remove the oldest coordinate

    return coordinates


def get_compass_direction(angle):
    """
    Convert angle to compass direction.

    Parameters:
    angle (float): Angle in degrees.

    Returns:
    str: Compass direction.
    """
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return directions[int(round(angle / 45)) % 8]


def calculate_heading(coord1, coord2):
    """
    Calculate the heading from coord1 to coord2.

    Parameters:
    coord1 (tuple): The first coordinate (x1, y1).
    coord2 (tuple): The second coordinate (x2, y2).

    Returns:
    float: The heading in degrees from coord1 to coord2.
    """
    dx = coord2[0] - coord1[0]
    dy = coord2[1] - coord1[1]

    # Calculate the angle in radians and then convert to degrees
    angle_radians = math.atan2(dy, dx)
    angle_degrees = math.degrees(angle_radians)

    # Adjust the angle to compass heading (if North is 0 degrees)
    compass_heading = (angle_degrees + 360) % 360

    return compass_heading


def calculate_heading_with_direction(coordinates):
    """
    Calculate the heading and compass direction from a list of two coordinates.

    Parameters:
    coordinates (list): A list containing two tuples, each representing an (x, y) coordinate.

    Returns:
    tuple: The heading in degrees and the compass direction.
    """
    if len(coordinates) != 2:
        raise ValueError("The list must contain exactly two coordinates.")

    coord1, coord2 = coordinates
    heading = calculate_heading(coord1, coord2)
    direction = get_compass_direction(heading)

    return heading, direction


coordinate_list = []
coordinate_list = generate_and_update_coordinates(coordinate_list)
coordinate_list = generate_and_update_coordinates(coordinate_list)

print(calculate_heading(coordinate_list[0], coordinate_list[1]))
print(get_compass_direction(calculate_heading(coordinate_list[0], coordinate_list[1])))
