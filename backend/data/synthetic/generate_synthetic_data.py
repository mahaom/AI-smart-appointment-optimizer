import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

APPT_TYPES = ["primary_care", "dental", "cardiology", "dermatology", "lab", "physio"]
PROVIDERS = [f"prov_{i:02d}" for i in range(1, 11)]
CLINICS = ["clinic_north", "clinic_central", "clinic_west"]

def simulate_no_show(lead_time_days: int, prior_no_shows: int, hour: int, appt_type: str) -> int:
    risk = 0.10
    risk += 0.04 * min(prior_no_shows, 5)
    risk += 0.01 * min(lead_time_days, 30)
    if hour < 9:
        risk += 0.03
    if appt_type in ["lab", "physio"]:
        risk += 0.02
    return 1 if random.random() < min(risk, 0.75) else 0

def main(rows: int = 800, out_path: str = "data/synthetic/appointments.csv"):
    start = datetime.now() - timedelta(days=120)
    end = datetime.now() + timedelta(days=30)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "clinic_id","provider_id","appt_datetime","appt_type",
            "lead_time_days","prior_no_shows","prior_shows","dow","hour_of_day","no_show_label"
        ])

        for _ in range(rows):
            appt_type = random.choice(APPT_TYPES)
            clinic_id = random.choice(CLINICS)
            provider_id = random.choice(PROVIDERS)

            appt_datetime = fake.date_time_between(start_date=start, end_date=end)
            lead_time_days = random.randint(0, 30)
            prior_no_shows = random.randint(0, 4)
            prior_shows = random.randint(prior_no_shows, prior_no_shows + random.randint(0, 12))

            dow = appt_datetime.weekday()
            hour = appt_datetime.hour

            label = simulate_no_show(lead_time_days, prior_no_shows, hour, appt_type)

            w.writerow([
                clinic_id, provider_id, appt_datetime.isoformat(), appt_type,
                lead_time_days, prior_no_shows, prior_shows, dow, hour, label
            ])

if __name__ == "__main__":
    main()
