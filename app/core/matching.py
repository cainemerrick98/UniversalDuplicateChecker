from pandas import DataFrame, Series
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype, is_string_dtype
from collections import defaultdict, deque
from typing import Callable
import datetime as dt


def fuzzy_match_dates(date1:dt.datetime, date2:dt.datetime)->bool:
    """
    Checks if dates are close together or if the months and days have been swapped
    """
    if abs((date1 - date2).days) <= 7:
        return True
    if date1.month == date2.day and date1.day == date2.month:
        return True
    
    return False 


def fuzzy_match_numbers(num1:float|int, num2:float|int)->bool:
    """
    Checks if there is a small absolute difference given the size of the numbers, 
    if there is a one adjacent swap between the two numbers and if there is a one addition 
    or deletion distance between the two numbers
    """
    if abs(num1 - num2) < (0.1 * max(num1, num2)): #difference is 10% of the max of num1 and num2
        return True

    if string_is_one_swap(str(num1), str(num2)):
        return True

    if string_is_one_addition_or_deletion(str(num1), str(num2)):
        return True

    return False


def string_is_one_swap(str1:str, str2:str)->bool:
    if len(str1) != len(str2):
        return False
    
    for i in range(len(str1)-1):
        str1_list = list(str1)    
        str1_list[i], str1_list[i+1]  = str1_list[i+1], str1_list[i]
        str1_oneswap = "".join(str1_list)

        if str1_oneswap == str2:
            return True
        

    return False


def string_is_one_addition_or_deletion(str1:str, str2:str)->bool:
    """
    The idea here is that if the two strings can be made the same with one addition
    or deletion and the difference in their absolute length is 1 then the smaller string 
    must be a substring
    """
    if abs(len(str1) - len(str2)) != 1:
        return False
    
    if len(str1) > len(str2):
        return str2 in str1
    
    return str1 in str2
    

def fuzzy_match_strings(str1:str, str2:str)->bool:
    """
    Returns True if the cleaned versions of the strings match exactly.
    TODO: Expand with more nuanced fuzzy logic (e.g., Levenshtein distance).
    """
    c_str1 = clean_string(str1)
    c_str2 = clean_string(str2)

    if c_str1 == c_str2:
        return True
    
    #TODO: Add more logic here
    
    return False


def clean_string(x:str):
    """
    Removes all non alphanumeric characters from the string
    """
    return "".join([i for i in x if i.isalnum()])


def get_fuzzy_comparison_func(column:Series)->Callable:
    if is_datetime64_any_dtype(column):
        return fuzzy_match_dates
    elif is_numeric_dtype(column):
        return fuzzy_match_numbers
    elif is_string_dtype(column):
        return fuzzy_match_strings

    return None

def get_column_comparers(object_df:DataFrame, columns:list[str]) -> dict[str:Callable]:
    """
    Returns a dictionary mapping columns to the appropiate comparison function
    """
    columns_comparer = {}
    for column in columns:
        comparer = get_fuzzy_comparison_func(object_df[column])
        if comparer:
            columns_comparer[column] = comparer
        
        else:
            raise ValueError(f'{column} type was not compatible. Type must be str, int, float, or datetime')
        
    return columns_comparer

def match_objects(object_a:Series, object_b:Series, max_non_exact_matches:int, column_comparers:dict[str:str]) -> tuple[bool, str]:
    """
    Returns True of False depending on whether the two objects are a match
    """
    relationship = 'Exact'
    is_match = True
    non_exact_matches = 0
    
    for column in column_comparers.keys():
        if object_a[column] == object_b[column]:
            continue
        else: 
            
            is_fuzzy_match = column_comparers[column](object_a[column], object_b[column])

            if is_fuzzy_match:
                relationship = f'Similar {column}'
                non_exact_matches += 1
            else:
                is_match = False
                break

            
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
    column_comparers = get_column_comparers(object_df, columns)

    for i in range(len(reduced_object_df)):
        object_a = object_df.iloc[i]
        for j in range(i+1, len(reduced_object_df)):
            object_b = object_df.iloc[j]
            is_match, relationship = match_objects(object_a, object_b, max_non_exact_matches, column_comparers)
            
            if is_match:
                groups_graph[object_a['ID']].append((object_b['ID'], relationship))
    
    return groups_graph

def parse_groups_graph(groups_graph:dict)->list[tuple]:
    """
    The function transform the groups graph into sets of connected ids and the group relationship type.
    Each of these sets can be considered as a duplicate group.
    We search for connected sets of objects using BFS, removing the nodes from the ids
    to search as we find them.
    """
    duplicate_groups = []
    ids_to_search = deque(groups_graph.keys())
    ids_searched = set()

    while ids_to_search:

        entry_point = ids_to_search.popleft()
        if entry_point in ids_searched:
            continue

        ids_searched.add(entry_point)
        connected_objects = deque(groups_graph[entry_point])

        relationships = set()
        group_object_ids = [entry_point]
        while connected_objects:
            object_id, relationship = connected_objects.popleft()
            
            relationships.add(relationship)
            group_object_ids.append(object_id)

            ids_searched.add(object_id)
            
            connected_objects.extend(groups_graph[object_id])
        
        if len(relationships) == 1:
            relationship_type = relationships.pop()
        
        elif len(relationships) == 2:
            relationships.pop()
            relationship_type = relationships.pop()

        else:
            relationship_type = 'Multiple'

        duplicate_groups.append((group_object_ids, relationship_type))
    
    return duplicate_groups
            







