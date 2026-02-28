from __future__ import annotations

from datetime import date, datetime, time as dt_time, timedelta, timezone

UTC_MINUS_5 = timezone(timedelta(hours=-5))


def now_utc_minus_5() -> datetime:
    return datetime.now(UTC_MINUS_5)


def ensure_utc_minus_5(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC_MINUS_5)
    return value.astimezone(UTC_MINUS_5)


def combine_date(value: date, t: dt_time) -> datetime:
    return datetime.combine(value, t, tzinfo=UTC_MINUS_5)


def start_of_day(value: date) -> datetime:
    return combine_date(value, dt_time.min)


def end_of_day(value: date) -> datetime:
    return combine_date(value, dt_time.max)
