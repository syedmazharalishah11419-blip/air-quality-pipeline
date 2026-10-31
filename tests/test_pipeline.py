import pytest

from src.pipeline import validate_data, clean_data, create_summary


def sample_rows():
    return [
        {
            "city": "peshawar",
            "date": "2026-10-25",
            "pm25": "45",
            "pm10": "80",
            "no2": "25"
        },
        {
            "city": "islamabad",
            "date": "2026-10-25",
            "pm25": "30",
            "pm10": "60",
            "no2": "18"
        }
    ]


def test_validate_data():
    assert validate_data(sample_rows()) is True


def test_clean_data():
    result = clean_data(sample_rows())
    assert result[0]["city"] == "Peshawar"


def test_create_summary():
    result = create_summary(clean_data(sample_rows()))
    assert result["total_records"] == 2


def test_empty_data():
    with pytest.raises(ValueError):
        validate_data([])


def test_negative_values():
    rows = sample_rows()
    rows[0]["pm25"] = "-10"

    with pytest.raises(ValueError):
        validate_data(rows)