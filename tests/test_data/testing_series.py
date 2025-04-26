from pandas import Series, merge
import random
import datetime as dt

def get_left_right_series(series:Series):
    pairs = merge(series, series, how='cross', suffixes=['_left', '_right'])
    s_left, s_right = pairs[f'{series.name}_left'], pairs[f'{series.name}_right']
    return s_left, s_right

#Date Series
date_series_left, date_series_right = get_left_right_series(
    Series(
        name='Dates',
        data=[dt.datetime(2025, 1, random.randint(1, 30)) for _ in range(10)]
    ))

month_day_swapped_left, month_day_swapped_right = get_left_right_series(
    Series(
        name='Dates',
        data=[dt.datetime(2025, 1, 2), dt.datetime(2025, 2, 1)]
    ))

within_7_days_left, within_7_days_right = get_left_right_series(
    Series(
        name='Dates',
        data=[dt.datetime(2025, 1, random.randint(4, 7)) for _ in range(10)]
    )
)

large_difference_left, large_difference_right = get_left_right_series(
    Series(
        name='Dates',
        data=[dt.datetime(random.randint(1950, 1970), 1, 1) for _ in range(10)] + [dt.datetime(random.randint(2040, 2080), 1, 1) for _ in range(10)] 
    )
)

#String Series
company_suffixes = ['', ' Limited', ' Ltd', ' ltd', ' Plc']
company_names = ['Google', 'Apple', 'Gooogle', 'Microsft', 'Microsoft', 'Mapple']
company_names_left, company_names_right = get_left_right_series(
    Series(
        name='Dates',
        data=[random.choice(company_names)+random.choice(company_suffixes) for _ in range(2)]
    )
)


