import pytest
import datetime as dt
from app.core import matching
from tests.test_data.invoice_df import invoice_df, invoice_columns

def test_fuzzy_match_dates_true_close_dates():
    date1 = dt.datetime(2025,1,1)
    date2 = dt.datetime(2025,1,3)
    
    is_fuzzy_match = matching.fuzzy_match_dates(date1, date2)

    assert is_fuzzy_match

def test_fuzzy_match_dates_true_month_day_swapper():
    date1 = dt.datetime(2025,6,7)
    date2 = dt.datetime(2025,7,6)
    
    is_fuzzy_match = matching.fuzzy_match_dates(date1, date2)

    assert is_fuzzy_match

def test_fuzzy_match_dates_false_not_close_dates():
    date1 = dt.datetime(2025,1,1)
    date2 = dt.datetime(2025,3,3)
    
    is_fuzzy_match = matching.fuzzy_match_dates(date1, date2)

    assert not is_fuzzy_match

def test_fuzzy_match_numbers_true_close_abs():
    num1 = 1000
    num2 = 1011

    is_fuzzy_match = matching.fuzzy_match_numbers(num1, num2)

    assert is_fuzzy_match

def test_fuzzy_match_numbers_true_one_swap():
    num1 = 1500
    num2 = 1050

    assert abs(num1 - num2) > (0.1 * max(num1, num2)) #Not true on 1st condition

    is_fuzzy_match = matching.fuzzy_match_numbers(num1, num2)

    assert is_fuzzy_match

def test_fuzzy_match_numbers_true_one_addition():
    num1 = 100
    num2 = 1000

    assert abs(num1 - num2) > (0.1 * max(num1, num2)) #Not true on 1st condition

    is_fuzzy_match = matching.fuzzy_match_numbers(num1, num2)

    assert is_fuzzy_match

def test_fuzzy_match_string_true():
    str1 = 'Abc 123'
    str2 = 'Abc123'

    is_fuzzy_match = matching.fuzzy_match_strings(str1, str2)

    assert is_fuzzy_match

def test_get_fuzzy_comparison_func():

    comparer = matching.get_fuzzy_comparison_func(invoice_df['Date'])
    assert comparer.__name__ == 'fuzzy_match_dates'

    comparer = matching.get_fuzzy_comparison_func(invoice_df['Amount'])
    assert comparer.__name__ == 'fuzzy_match_numbers'

    comparer = matching.get_fuzzy_comparison_func(invoice_df['Reference'])
    assert comparer.__name__ == 'fuzzy_match_strings'


def test_get_column_comparers():
    column_comparers = matching.get_column_comparers(invoice_df, invoice_columns)
    
    assert isinstance(column_comparers, dict)
    assert len(column_comparers.keys()) == 4
    assert column_comparers['Reference'].__name__ == 'fuzzy_match_strings'
    assert column_comparers['Amount'].__name__ == 'fuzzy_match_numbers'
    assert column_comparers['VendorName'].__name__ == 'fuzzy_match_strings'
    assert column_comparers['Date'].__name__ == 'fuzzy_match_dates'

def test_match_objects_no_match():
    object_a = invoice_df.iloc[0]
    object_b = invoice_df.iloc[1]

    column_comparers = matching.get_column_comparers(invoice_df, invoice_columns)
    is_match, relationship = matching.match_objects(object_a, object_b, 1, column_comparers)

    assert not is_match

def test_match_objects_similar_vendor_name():
    object_a = invoice_df.iloc[0]
    object_b = invoice_df.iloc[2]

    column_comparers = matching.get_column_comparers(invoice_df, invoice_columns)
    is_match, relationship = matching.match_objects(object_a, object_b, 1, column_comparers)

    assert is_match
    assert relationship == 'Similar VendorName'

def test_create_groups_graph():
    
    groups_graph = matching.create_groups_graph(invoice_df, invoice_columns, 1)
    
    assert isinstance(groups_graph, dict)
    assert len(groups_graph.keys()) == 1
    assert groups_graph.get('a')
    assert groups_graph['a'][0] == ('c', 'Similar VendorName')
