import csv
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data/sample/air_quality.csv"
OUTPUT_FILE = BASE_DIR / "data/processed/summary.json"

REQUIRED_COLUMNS = ["city", "date", "pm25", "pm10", "no2"]


def validate_data(rows):
    if not rows:
        raise ValueError("CSV file is empty")

    for row in rows:
        for column in REQUIRED_COLUMNS:
            if column not in row or not row[column]:
                raise ValueError(f"Missing value: {column}")

        try:
            datetime.strptime(row["date"], "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format")

        for column in ["pm25", "pm10", "no2"]:
            value = float(row[column])
            if value < 0:
                raise ValueError(f"Negative value: {column}")

    return True


def clean_data(rows):
    cleaned = []

    for row in rows:
        cleaned_row = {
            "city": row["city"].strip().title(),
            "date": row["date"].strip(),
            "pm25": float(row["pm25"]),
            "pm10": float(row["pm10"]),
            "no2": float(row["no2"])
        }

        cleaned.append(cleaned_row)

    return cleaned


def create_summary(rows):
    cities = sorted(set(row["city"] for row in rows))

    summary = {
        "total_records": len(rows),
        "cities": cities,
        "average_pm25": round(
            sum(row["pm25"] for row in rows) / len(rows), 2
        ),
        "average_pm10": round(
            sum(row["pm10"] for row in rows) / len(rows), 2
        ),
        "average_no2": round(
            sum(row["no2"] for row in rows) / len(rows), 2
        )
    }

    return summary


def run_pipeline(input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    with open(input_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV headers are missing")

        if not set(REQUIRED_COLUMNS).issubset(reader.fieldnames):
            raise ValueError("Required columns are missing")

        rows = list(reader)

    validate_data(rows)

    cleaned = clean_data(rows)

    summary = create_summary(cleaned)

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    return summary


if __name__ == "__main__":
    result = run_pipeline()

    print("Pipeline completed successfully!")

    print(json.dumps(result, indent=4))