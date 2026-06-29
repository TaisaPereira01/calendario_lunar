"""
Gera o arquivo moon_calendar.json

Uso:

python generate_moon_calendar.py

ou

python generate_moon_calendar.py --year 2026
"""

from datetime import date, timedelta
from pathlib import Path
import argparse
import json

from skyfield.api import load
from skyfield import almanac

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"

DATABASE_DIR = ROOT / "database"

OUTPUT = ROOT / "data" / "moon_calendar.json"


PHASES = {
    0: "Lua Nova",
    1: "Lua Crescente",
    2: "Lua Cheia",
    3: "Lua Minguante",
}


def build_calendar(year: int):

    ts = load.timescale()

    eph = load("de421.bsp")

    start = ts.utc(year, 1, 1)

    end = ts.utc(year + 1, 1, 1)

    phase_function = almanac.moon_phases(eph)

    times, phases = almanac.find_discrete(
        start,
        end,
        phase_function,
    )

    change_dates = []

    for t, p in zip(times, phases):
        change_dates.append(
            (
                t.utc_datetime().date(),
                PHASES[int(p)],
            )
        )

    calendar = []

    current_phase = change_dates[0][1]
    idx = 0

    current_day = date(year, 1, 1)
    last_day = date(year, 12, 31)

    while current_day <= last_day:

        while (
            idx + 1 < len(change_dates)
            and current_day >= change_dates[idx + 1][0]
        ):
            idx += 1
            current_phase = change_dates[idx][1]

        calendar.append(
            {
                "date": current_day.isoformat(),
                "phase": current_phase,
            }
        )

        current_day += timedelta(days=1)

    return calendar


def save(calendar):

    OUTPUT.parent.mkdir(exist_ok=True)

    with open(
        OUTPUT,
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(
            calendar,
            fp,
            ensure_ascii=False,
            indent=4,
        )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--year",
        type=int,
        default=date.today().year,
    )

    args = parser.parse_args()

    calendar = build_calendar(args.year)

    save(calendar)

    print(
        f"{len(calendar)} dias gerados."
    )

    print(OUTPUT.resolve())


if __name__ == "__main__":
    main()