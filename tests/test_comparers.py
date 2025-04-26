import pytest
from numpy import ndarray
from app.core import comparers
import tests.test_data.testing_series as ts

def test_date_fuzzy():
    date_fuzzy = comparers.DateFuzzy('columns', 7)
    c = date_fuzzy._compute_vectorized(ts.date_series_left, ts.date_series_right)

    assert isinstance(c, ndarray)
    assert all((c == 1) | (c == 0))

def test_date_fuzzy_month_day_swapper_true():
    date_fuzzy = comparers.DateFuzzy('columns', 7)
    c = date_fuzzy._compute_vectorized(ts.month_day_swapped_left, ts.month_day_swapped_right)

    assert all(c==1)

def test_date_fuzzy_within_max_diff_true():
    date_fuzzy = comparers.DateFuzzy('columns', 7)
    c = date_fuzzy._compute_vectorized(ts.within_7_days_left, ts.within_7_days_right)

    assert all(c==1)

def test_date_fuzzy_large_diff():
    date_fuzzy = comparers.DateFuzzy('columns', 7)
    #Does not raise overflow error
    c = date_fuzzy._compute_vectorized(ts.large_difference_left, ts.large_difference_right)

def test_string_fuzzy():
    string_fuzzy = comparers.StringFuzzy('any', [], ts.company_suffixes)
    c = string_fuzzy._compute_vectorized(ts.company_names_left, ts.company_names_right)

    assert isinstance(c, ndarray)
    assert all((c == 1) | (c == 0))

def test_string_fuzzy_clean_string():
    string_fuzzy = comparers.StringFuzzy('any', [], ts.company_suffixes)
    clean_strings = string_fuzzy._clean_strings(ts.company_names_left)
    for suf in ts.company_suffixes:
        assert all([~clean_strings[i].endswith(suf) for i in range(len(clean_strings))])
    


    

    