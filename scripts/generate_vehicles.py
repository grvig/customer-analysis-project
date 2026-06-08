import pandas as pd
import random
from datetime import datetime

customers = pd.read_csv("dataset/customers.csv")

vehicle_models = {
    "TVS": [
        "Jupiter",
        "NTorq 125",
        "Apache RTR 160",
        "Apache RTR 200",
        "Raider 125",
        "Ronin",
        "Sport",
        "XL100"
    ],
    "Honda": [
        "Activa 6G",
        "Shine",
        "Unicorn",
        "SP125",
        "Dio",
        "Hornet 2.0",
        "CB200X",
        "Livo"
    ],
    "Hero": [
        "Splendor Plus",
        "HF Deluxe",
        "Passion Pro",
        "Glamour",
        "Xtreme 160R",
        "Xpulse 200",
        "Super Splendor",
        "Destini 125"
    ],
    "Bajaj": [
        "Pulsar 125",
        "Pulsar 150",
        "Pulsar N160",
        "Pulsar NS200",
        "Platina",
        "CT110",
        "Avenger Street",
        "Dominar 400"
    ],
    "Yamaha": [
        "FZ S",
        "R15 V4",
        "MT15",
        "Fascino",
        "RayZR",
        "FZ X",
        "Aerox 155",
        "R3"
    ],
    "Suzuki": [
        "Access 125",
        "Burgman Street",
        "Avenis",
        "Gixxer",
        "Gixxer SF",
        "V Strom SX",
        "Hayate",
        "Gixxer 250"
    ]
}

def generate_vehicle_number():
    districts = [
        "01", "02", "03", "04", "05",
        "09", "10", "18", "22", "28",
        "33", "37", "38", "45", "58", "59"
    ]

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    return (
        "TN"
        + random.choice(districts)
        + random.choice(letters)
        + random.choice(letters)
        + str(random.randint(1000, 9999))
    )

vehicles = []

vehicle_id = 1
current_year = datetime.now().year

for _, customer in customers.iterrows():

    r = random.random()

    if r < 0.70:
        num_vehicles = 1
    elif r < 0.95:
        num_vehicles = 2
    else:
        num_vehicles = 3

    for _ in range(num_vehicles):

        make = random.choice(list(vehicle_models.keys()))
        model = random.choice(vehicle_models[make])

        year = random.randint(2017, current_year)

        vehicles.append({
            "vehicle_id": vehicle_id,
            "customer_id": customer["customer_id"],
            "vehicle_number": generate_vehicle_number(),
            "make": make,
            "model": model,
            "year": year,
            "vehicle_age": current_year - year,
            "purchase_date": f"{year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        })

        vehicle_id += 1

df = pd.DataFrame(vehicles)

df.to_csv(
    "dataset/vehicles.csv",
    index=False
)

print(f"{len(df)} vehicles generated.")