"""
utils/cars.py


Creates some face cars in sqlite db just for testing purspose
"""

import sqlite3
from enum import Enum
from typing import List, Tuple
from data_schemas import CarBodyType, FuelType, CarColor, CarProperties


# Generated records with cars
cars_data = [
    ('Toyota', 'Corolla', CarBodyType.SEDAN.value, FuelType.GAS.value, CarColor.WHITE.value),
    ('Tesla', 'Model 3', CarBodyType.SEDAN.value, FuelType.ELECTRIC.value, CarColor.RED.value),
    ('Ford', 'Escape', CarBodyType.SUV.value, FuelType.BIOFUEL.value, CarColor.BLUE.value),
    ('Chevrolet', 'Bolt', CarBodyType.HATCHBACK.value, FuelType.ELECTRIC.value, CarColor.SILVER.value),
    ('Honda', 'Civic', CarBodyType.SEDAN.value, FuelType.GAS.value, CarColor.BLACK.value),
    ('BMW', 'M3', CarBodyType.SPORTS_CAR.value, FuelType.GAS.value, CarColor.GREY.value),
    ('Ferrari', '488 Spider', CarBodyType.CONVERTIBLE.value, FuelType.GAS.value, CarColor.RED.value),
    ('Lamborghini', 'Huracán', CarBodyType.ROADSTER.value, FuelType.GAS.value, CarColor.YELLOW.value),
    ('Jeep', 'Wrangler', CarBodyType.SUV.value, FuelType.GAS.value, CarColor.GREEN.value),
    ('Toyota', 'Land Cruiser', CarBodyType.SUV.value, FuelType.DIESEL.value, CarColor.BEIGE.value),
    ('Ford', 'F-150', CarBodyType.PICKUP.value, FuelType.GAS.value, CarColor.BLUE.value),
    ('Dodge', 'Charger', CarBodyType.MUSCLE_CAR.value, FuelType.GAS.value, CarColor.BLACK.value),
    ('Mazda', 'MX-5', CarBodyType.CONVERTIBLE.value, FuelType.GAS.value, CarColor.RED.value),
    ('Nissan', 'Leaf', CarBodyType.HATCHBACK.value, FuelType.ELECTRIC.value, CarColor.WHITE.value),
    ('Volkswagen', 'Golf', CarBodyType.HATCHBACK.value, FuelType.DIESEL.value, CarColor.SILVER.value),
    ('Subaru', 'Outback', CarBodyType.WAGON.value, FuelType.GAS.value, CarColor.GREEN.value),
    ('Porsche', '911', CarBodyType.COUPE.value, FuelType.GAS.value, CarColor.GOLD.value),
    ('Chevrolet', 'Camaro', CarBodyType.MUSCLE_CAR.value, FuelType.GAS.value, CarColor.ORANGE.value),
    ('Hyundai', 'Ioniq 5', CarBodyType.CROSSOVER.value, FuelType.ELECTRIC.value, CarColor.GREY.value),
]


# SQLite in-memory
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE cars (
        make TEXT,
        model TEXT,
        body_type TEXT,
        fuel_type TEXT,
        color TEXT
    )
''')

cursor.executemany('INSERT INTO cars VALUES (?, ?, ?, ?, ?)', cars_data)


CARS_DB_CONN = conn

# Query and display
# cursor.execute('SELECT * FROM cars')
# for row in cursor.fetchall():
#     print(row)

# conn.close()



def find_cars_by_properties(car_properties: CarProperties) -> list[tuple]:
    """Find available cars from the retailer database.

    Args:
        car_properties : properties that will filter the result
    
    Example:

    """
    cursor = conn.cursor()

    query = "SELECT * FROM cars WHERE 1=1"
    params = []

    if car_properties.make:
        query += " AND make = ?"
        params.append(car_properties.make)
    if car_properties.model:
        query += " AND model = ?"
        params.append(car_properties.model)
    if car_properties.body_type:
        query += " AND body_type = ?"
        params.append(car_properties.body_type.value)
    if car_properties.fuel_type:
        query += " AND fuel_type = ?"
        params.append(car_properties.fuel_type.value)
    if car_properties.color:
        query += " AND color = ?"
        params.append(car_properties.color.value)

    cursor.execute(query, params)
    return cursor.fetchall()


props = CarProperties(
    fuel_type=FuelType.ELECTRIC,
    body_type=CarBodyType.SEDAN
)

props = CarProperties(
    color=CarColor.RED
)


matches = filter_cars_by_properties(props)

print(props)

for car in matches:
    print(car)
