from pandas import DataFrame, Series
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype, is_string_dtype
from collections import defaultdict 
from typing import Callable
import datetime as dt

def fuzzy_match_dates(date1:dt.datetime, date2:dt.datetime)->bool:
    ...

def fuzzy_match_numbers(num1:float|int, num2:float|int)->bool:
    ...

def fuzzy_match_strings(str1:str, str2:str)->bool:
    ...

def get_fuzzy_comparison_func(x)->Callable:
    if is_datetime64_any_dtype(x):
        return fuzzy_match_dates
    elif is_numeric_dtype(x):
        return fuzzy_match_numbers
    elif is_string_dtype(x):
        return fuzzy_match_strings

    return None



def match_objects(object_a:Series, object_b:Series, max_non_exact_matches:int) -> tuple[bool, str]:
    relationship = 'EXACT'
    is_match = True
    non_exact_matches = 0
    for column in object_a.index:
        if object_a[column] == object_b[column]:
            continue
        else:
            #TODO: Derive column dtypes in another function your doing it for every object here it only needs to be done once on the whole table!!!
            func = get_fuzzy_comparison_func(object_a[column])

            if func:
                is_fuzzy_match = func(object_a[column], object_b[column])

                if is_fuzzy_match:
                    relationship = f'SIMILAR {column}'
                    non_exact_matches += 1
            else:
                raise ValueError(f'{column} type was not recognised. Type must be str, int, float, or datetime')
            
            if non_exact_matches > max_non_exact_matches:
                is_match = False
                break
    
    return is_match, relationship


def create_groups_graph(object_df:DataFrame, columns:list[str], max_non_exact_matches:int)->dict:
    """
    This function creates a graph where the nodes are objects and the 
    edges represent duplicate relationship.

    Objects are compared in pairs. If they are flagged as a match (potential dupe)
    then an edge is created between the objects in the graph.

    A set of connected nodes represents a duplicate group.
    """
    groups_graph = defaultdict(list)

    reduced_object_df = object_df[columns]

    for i in range(len(reduced_object_df)):
        object_a = object_df.iloc[i]
        for j in range(i+1, len(reduced_object_df)):
            object_b = object_df.iloc[j]
            is_match, relationship = match_objects(object_a, object_b, max_non_exact_matches)

            if is_match:
                groups_graph[object_a['ID']].append((object_b['ID'], relationship))
    
    return groups_graph



