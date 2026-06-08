from faker import Faker
import pandas as pd
import random

fake = Faker("en_IN")

cities = [
    "Chennai",
    "Coimbatore",
    "Madurai",
    "Salem",
    "Tiruchirappalli"
]

branches = {
    "Chennai": [
        "Anna Nagar",
        "Velachery",
        "Tambaram",
        "Porur",
        "T Nagar"
    ],
    "Coimbatore": [
        "Gandhipuram",
        "RS Puram",
        "Peelamedu",
        "Saibaba Colony",
        "Singanallur"
    ],
    "Madurai": [
        "KK Nagar",
        "Anna Nagar Madurai",
        "Mattuthavani",
        "Thirunagar",
        "Tallakulam"
    ],
    "Salem": [
        "Fairlands",
        "Hasthampatti",
        "Ammapet",
        "Suramangalam",
        "Omalur"
    ],
    "Tiruchirappalli": [
        "Srirangam",
        "Thillai Nagar",
        "Cantonment",
        "Woraiyur",
        "KK Nagar Trichy"
    ]
}

rows = []

for cid in range(1, 5001):

    city = random.choice(cities)
    branch = random.choice(branches[city])

    first_digit = random.choice(["6", "7", "8", "9"])

    phone = (
        first_digit +
        str(random.randint(100000000, 999999999))
    )

    rows.append({
        "customer_id": cid,
        "customer_name": fake.name(),
        "phone_number": phone,
        "email": fake.email(),
        "city": city,
        "branch": branch,
        "registration_date": fake.date_between(
            start_date="-5y",
            end_date="today"
        )
    })

df = pd.DataFrame(rows)

df.to_csv(
    "dataset/customers.csv",
    index=False
)

print(f"{len(df)} customers generated.")