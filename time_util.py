import re
from datetime import date, timedelta


def convert_datetime(string_date: str) -> date:
    t = list(map(int, re.findall("\d+", string_date)))

    return date(t[0], t[1], t[2])


def get_start_and_end_of_this_week() -> (date, date):
    current = date.today()
    start_date = current - timedelta(days=current.weekday())
    end_date = start_date + timedelta(days=6)

    return start_date, end_date
