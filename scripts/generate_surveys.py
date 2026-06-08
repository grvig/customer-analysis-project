import pandas as pd
import random

services = pd.read_csv("dataset/services.csv")

feedback_map = {
    5: [
        "Excellent service experience.",
        "Issue resolved quickly and professionally.",
        "Very satisfied with the service provided.",
        "Staff were helpful and courteous."
    ],

    4: [
        "Service was good overall.",
        "Issue resolved satisfactorily.",
        "Reasonably happy with the service.",
        "Good experience with the service center."
    ],

    3: [
        "Service was acceptable.",
        "Issue eventually resolved.",
        "Average service experience.",
        "Could have been handled better."
    ],

    2: [
        "Resolution took longer than expected.",
        "Not fully satisfied with the service.",
        "Communication could be improved.",
        "Service experience was below expectations."
    ],

    1: [
        "Issue still not resolved.",
        "Very dissatisfied with the service.",
        "Poor service experience.",
        "Would not recommend this service center."
    ]
}

surveys = []

survey_id = 1

for _, service in services.iterrows():

    rating = 5

    if service["status"] == "Resolved":

        if service["resolution_days"] <= 3:
            rating = random.choice([4, 5, 5])

        elif service["resolution_days"] <= 7:
            rating = random.choice([3, 4, 4, 5])

        else:
            rating = random.choice([2, 3, 4])

    elif service["status"] == "In Progress":

        rating = random.choice([2, 3, 3, 4])

    else:

        rating = random.choice([1, 1, 2])

    if service["service_cost"] > 5000:
        rating = max(1, rating - 1)

    if service["service_type"] in [
        "Engine Inspection",
        "Fuel Line Repair",
        "Brake Repair"
    ]:
        if random.random() < 0.30:
            rating = max(1, rating - 1)

    will_return = "Yes" if rating >= 4 else "No"

    recommend_service = "Yes" if rating >= 4 else "No"

    feedback = random.choice(
        feedback_map[rating]
    )

    surveys.append({
        "survey_id": survey_id,
        "service_id": service["service_id"],
        "customer_rating": rating,
        "will_return": will_return,
        "recommend_service": recommend_service,
        "feedback": feedback
    })

    survey_id += 1

df = pd.DataFrame(surveys)

df.to_csv(
    "dataset/surveys.csv",
    index=False
)

print(f"{len(df)} surveys generated.")