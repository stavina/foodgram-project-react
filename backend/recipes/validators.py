import datetime as dt


def validate_year(year):
    """Валидатор соответствия года."""
    now_year = dt.date.today()
    if year > now_year.year:
        raise ValueError(f'Некорректный год {year}')
