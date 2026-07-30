#!/usr/bin/env python3
"""Validate or regenerate the static screenshot-style earnings calendar data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "calendar.json"


def load_calendar() -> dict:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_calendar(data: dict) -> None:
    if data.get("title") != "한국 잠정실적발표 일정(변동 가능)":
        raise ValueError("Unexpected calendar title")

    columns = data.get("columns")

    if not isinstance(columns, list) or len(columns) != 12:
        raise ValueError("calendar.json must contain 12 date columns")

    for column in columns:
        if not column.get("label"):
            raise ValueError("Every column needs a label")

        companies = column.get("companies")

        if not isinstance(companies, list):
            raise ValueError(f"{column.get('label')} companies must be a list")

        for company in companies:
            if not company.get("name"):
                raise ValueError(f"{column.get('label')} has an empty company name")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only validate data/calendar.json.",
    )
    args = parser.parse_args()

    data = load_calendar()
    validate_calendar(data)

    if args.check:
        print("calendar.json is valid")
        return

    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {DATA_FILE}")


if __name__ == "__main__":
    main()
