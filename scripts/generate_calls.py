import pandas as pd
import random
from faker import Faker

fake = Faker("en_IN")

customers = pd.read_csv("dataset/customers.csv")
vehicles = pd.read_csv("dataset/vehicles.csv")
agents = pd.read_csv("dataset/agents.csv")

complaint_issues = [
    "Engine Overheating",
    "Exhaust Heating",
    "Battery Issue",
    "Battery Drain",
    "Brake Noise",
    "Brake Failure",
    "Oil Leakage",
    "Fuel Leakage",
    "Suspension Noise",
    "Chain Noise",
    "Electrical Fault",
    "Headlight Failure",
    "Self Start Problem",
    "Vehicle Not Starting",
    "Low Mileage",
    "Engine Vibration",
    "Clutch Issue",
    "Gear Shift Problem",
    "Tyre Wear",
    "Wheel Alignment Issue"
]

service_issues = [
    "Periodic Service",
    "Oil Change",
    "Brake Inspection",
    "Battery Check",
    "Wheel Alignment",
    "Chain Adjustment",
    "Engine Inspection",
    "General Checkup"
]

followup_issues = [
    "Previous Complaint Follow Up",
    "Repair Status Check",
    "Service Status Check",
    "Escalation Follow Up"
]

general_queries = [
    "Warranty Information",
    "Service Cost Inquiry",
    "Spare Parts Availability",
    "Service Center Location",
    "Roadside Assistance",
    "AMC Plan Details"
]

issue_notes = {
    "Engine Overheating": [
        "Customer reports engine overheating during long rides.",
        "Engine temperature rises significantly in traffic conditions.",
        "Vehicle becoming excessively hot after continuous usage."
    ],
    "Exhaust Heating": [
        "Customer reports excessive heat near exhaust area.",
        "Exhaust section becoming unusually hot during rides.",
        "Customer concerned about heat from exhaust assembly."
    ],
    "Battery Issue": [
        "Battery not retaining charge properly.",
        "Customer reports reduced battery performance.",
        "Battery discharge observed frequently."
    ],
    "Battery Drain": [
        "Battery draining overnight.",
        "Customer reports frequent battery discharge.",
        "Battery losing charge within short periods."
    ],
    "Brake Noise": [
        "Brake squeaking sound observed during usage.",
        "Noise heard while applying brakes.",
        "Customer reports unusual brake sound."
    ],
    "Brake Failure": [
        "Customer reports brake performance concerns.",
        "Braking response reduced unexpectedly.",
        "Brake functionality requires inspection."
    ],
    "Oil Leakage": [
        "Oil leakage observed beneath vehicle.",
        "Customer reports oil dripping after parking.",
        "Engine oil leakage suspected."
    ],
    "Fuel Leakage": [
        "Customer noticed fuel leakage smell.",
        "Fuel dripping observed near fuel line.",
        "Possible fuel system leakage reported."
    ],
    "Suspension Noise": [
        "Suspension producing noise on rough roads.",
        "Customer reports unusual suspension sound.",
        "Noise noticed while crossing speed breakers."
    ],
    "Chain Noise": [
        "Chain noise reported during riding.",
        "Abnormal sound from chain assembly.",
        "Chain requires inspection."
    ],
    "Electrical Fault": [
        "Electrical system malfunction reported.",
        "Customer reports intermittent electrical issues.",
        "Vehicle experiencing electrical irregularities."
    ],
    "Headlight Failure": [
        "Headlight not functioning properly.",
        "Customer reports lighting issue.",
        "Headlamp requires inspection."
    ],
    "Self Start Problem": [
        "Self start mechanism not responding consistently.",
        "Customer reports difficulty starting vehicle.",
        "Self start system requires checking."
    ],
    "Vehicle Not Starting": [
        "Vehicle fails to start intermittently.",
        "Customer unable to start vehicle.",
        "Starting issue reported."
    ],
    "Low Mileage": [
        "Customer dissatisfied with fuel efficiency.",
        "Mileage lower than expected.",
        "Fuel consumption concern raised."
    ],
    "Engine Vibration": [
        "Excessive engine vibration observed.",
        "Customer reports unusual vibration while riding.",
        "Engine vibration requires inspection."
    ],
    "Clutch Issue": [
        "Clutch response not smooth.",
        "Customer reports clutch operation issue.",
        "Clutch assembly inspection requested."
    ],
    "Gear Shift Problem": [
        "Difficulty shifting gears reported.",
        "Gear transition not smooth.",
        "Customer reports gear shifting concern."
    ],
    "Tyre Wear": [
        "Uneven tyre wear observed.",
        "Customer concerned about tyre condition.",
        "Tyre replacement may be required."
    ],
    "Wheel Alignment Issue": [
        "Vehicle pulling to one side.",
        "Wheel alignment inspection requested.",
        "Customer reports alignment concern."
    ]
}

calls = []
call_id = 1

for _, customer in customers.iterrows():

    num_calls = random.randint(1, 5)

    customer_vehicles = vehicles[
        vehicles["customer_id"] == customer["customer_id"]
    ]

    branch_agents = agents[
        agents["branch"] == customer["branch"]
    ]

    for _ in range(num_calls):

        vehicle = customer_vehicles.sample(1).iloc[0]
        agent = branch_agents.sample(1).iloc[0]

        call_type = random.choices(
            ["Complaint", "Service Inquiry", "Follow Up", "General Query"],
            weights=[60, 20, 10, 10],
            k=1
        )[0]

        vehicle_age = vehicle["vehicle_age"]

        if call_type == "Complaint":

            issue = random.choice(complaint_issues)

            if vehicle_age >= 6:
                issue = random.choice([
                    "Battery Issue",
                    "Battery Drain",
                    "Oil Leakage",
                    "Engine Overheating",
                    "Low Mileage",
                    "Tyre Wear"
                ])

            notes = random.choice(
                issue_notes.get(
                    issue,
                    ["Customer reported issue."]
                )
            )

            if issue in [
                "Brake Failure",
                "Fuel Leakage",
                "Engine Overheating"
            ]:
                priority = "High"

            elif issue in [
                "Battery Issue",
                "Brake Noise",
                "Oil Leakage"
            ]:
                priority = "Medium"

            else:
                priority = "Low"

        elif call_type == "Service Inquiry":

            issue = random.choice(service_issues)

            notes = (
                f"Customer contacted branch regarding "
                f"{issue.lower()}."
            )

            priority = random.choice(
                ["Low", "Medium"]
            )

        elif call_type == "Follow Up":

            issue = random.choice(followup_issues)

            notes = (
                f"Customer requested update regarding "
                f"{issue.lower()}."
            )

            priority = "Medium"

        else:

            issue = random.choice(general_queries)

            notes = (
                f"Customer requested information regarding "
                f"{issue.lower()}."
            )

            priority = "Low"

        calls.append({
            "call_id": call_id,
            "customer_id": customer["customer_id"],
            "vehicle_id": vehicle["vehicle_id"],
            "agent_id": agent["agent_id"],
            "branch": customer["branch"],
            "call_date": fake.date_between(
                start_date="-2y",
                end_date="today"
            ),
            "call_type": call_type,
            "issue_category": issue,
            "priority": priority,
            "call_duration_mins": random.randint(2, 25),
            "call_notes": notes
        })

        call_id += 1

df = pd.DataFrame(calls)

df.to_csv(
    "dataset/calls.csv",
    index=False
)

print(f"{len(df)} calls generated.")