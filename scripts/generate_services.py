import pandas as pd
import random
from datetime import timedelta

calls = pd.read_csv("dataset/calls.csv")

service_types = {
    "Engine Overheating": "Engine Inspection",
    "Exhaust Heating": "Exhaust Inspection",
    "Battery Issue": "Battery Replacement",
    "Battery Drain": "Battery Check",
    "Brake Noise": "Brake Inspection",
    "Brake Failure": "Brake Repair",
    "Oil Leakage": "Oil Seal Replacement",
    "Fuel Leakage": "Fuel Line Repair",
    "Suspension Noise": "Suspension Service",
    "Chain Noise": "Chain Adjustment",
    "Electrical Fault": "Electrical Diagnosis",
    "Headlight Failure": "Electrical Repair",
    "Self Start Problem": "Starter Inspection",
    "Vehicle Not Starting": "Starting System Diagnosis",
    "Low Mileage": "Engine Tuning",
    "Engine Vibration": "Engine Mount Inspection",
    "Clutch Issue": "Clutch Service",
    "Gear Shift Problem": "Gearbox Inspection",
    "Tyre Wear": "Tyre Replacement",
    "Wheel Alignment Issue": "Wheel Alignment",

    "Periodic Service": "Periodic Service",
    "Oil Change": "Oil Change",
    "Brake Inspection": "Brake Inspection",
    "Battery Check": "Battery Check",
    "Wheel Alignment": "Wheel Alignment",
    "Chain Adjustment": "Chain Adjustment",
    "Engine Inspection": "Engine Inspection",
    "General Checkup": "General Checkup"
}

service_costs = {
    "Engine Inspection": (1200, 2500),
    "Exhaust Inspection": (800, 1800),
    "Battery Replacement": (2000, 4500),
    "Battery Check": (300, 800),
    "Brake Inspection": (400, 1000),
    "Brake Repair": (1500, 4000),
    "Oil Seal Replacement": (800, 2500),
    "Fuel Line Repair": (1000, 3500),
    "Suspension Service": (1200, 5000),
    "Electrical Diagnosis": (500, 2000),
    "Electrical Repair": (1000, 3500),
    "Starter Inspection": (500, 1500),
    "Starting System Diagnosis": (800, 2500),
    "Engine Tuning": (1000, 3000),
    "Engine Mount Inspection": (700, 1800),
    "Clutch Service": (1500, 4500),
    "Gearbox Inspection": (1200, 3500),
    "Tyre Replacement": (2500, 7000),
    "Wheel Alignment": (500, 1200),
    "Periodic Service": (1200, 3000),
    "Oil Change": (600, 1500),
    "General Checkup": (300, 1000),
    "Chain Adjustment": (300, 800)
}

services = []

service_id = 1

for _, call in calls.iterrows():

    create_service = False

    if call["call_type"] == "Complaint":
        create_service = random.random() < 0.80

    elif call["call_type"] == "Service Inquiry":
        create_service = random.random() < 0.60

    if not create_service:
        continue

    if call["priority"] == "High":
        resolution_days = random.randint(5, 15)

    elif call["priority"] == "Medium":
        resolution_days = random.randint(2, 7)

    else:
        resolution_days = random.randint(1, 5)

    status = random.choice([
        "Resolved",
        "Resolved",
        "Resolved",
        "Resolved",
        "In Progress",
        "Open"
    ])

    service_date = (
        pd.to_datetime(call["call_date"])
        + timedelta(days=random.randint(0, 3))
    )

    service_type = service_types.get(
        call["issue_category"],
        "General Service"
    )

    if service_type in service_costs:
        min_cost, max_cost = service_costs[service_type]
        service_cost = random.randint(min_cost, max_cost)
    else:
        service_cost = random.randint(500, 2000)

    services.append({
        "service_id": service_id,
        "call_id": call["call_id"],
        "vehicle_id": call["vehicle_id"],
        "service_type": service_type,
        "service_date": service_date.date(),
        "resolution_days": resolution_days,
        "service_cost": service_cost,
        "status": status
    })

    service_id += 1

df = pd.DataFrame(services)

df.to_csv(
    "dataset/services.csv",
    index=False
)

print(f"{len(df)} services generated.")