import random


def generate_and_update_coordinates(coordinates, max_points=2):
    new_coordinate = (random.uniform(0, 100), random.uniform(0, 100))

    coordinates.append(new_coordinate)

    while len(coordinates) > max_points:
        coordinates.pop(0)

    return coordinates


coordinate_list = [(10, 20)]
coordinate_list = generate_and_update_coordinates(coordinate_list)
print(coordinate_list)
coordinate_list = generate_and_update_coordinates(coordinate_list)
print(coordinate_list)
