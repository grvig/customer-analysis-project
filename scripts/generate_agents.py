import pandas as pd
import random
from faker import Faker

fake = Faker("en_IN")

branches = [
    "Anna Nagar",
    "Velachery",
    "Tambaram",
    "Porur",
    "T Nagar",
    "Gandhipuram",
    "RS Puram",
    "Peelamedu",
    "Saibaba Colony",
    "Singanallur",
    "KK Nagar",
    "Anna Nagar Madurai",
    "Mattuthavani",
    "Thirunagar",
    "Tallakulam",
    "Fairlands",
    "Hasthampatti",
    "Ammapet",
    "Suramangalam",
    "Omalur",
    "Srirangam",
    "Thillai Nagar",
    "Cantonment",
    "Woraiyur",
    "KK Nagar Trichy"
]

agents = []

agent_id = 1

for branch in branches:

    num_agents = random.randint(8, 15)

    for _ in range(num_agents):

        experience = random.randint(1, 12)

        if experience >= 7:
            designation = "Senior Agent"
        elif experience >= 4:
            designation = "Agent"
        else:
            designation = "Junior Agent"

        agents.append({
            "agent_id": agent_id,
            "agent_name": fake.name(),
            "branch": branch,
            "experience_years": experience,
            "designation": designation
        })

        agent_id += 1

df = pd.DataFrame(agents)

df.to_csv(
    "dataset/agents.csv",
    index=False
)

print(f"{len(df)} agents generated.")