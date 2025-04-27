from recordlinkage.datasets import load_febrl1
from app.core.comparers import DateFuzzy, ExactMatch, NumericFuzzy, StringFuzzy
from app.core.duplicate_checker import DuplicateChecker
from tests.test_data.people_df import people_df

df_febrl1 = load_febrl1()

test_search_patterns = {
    'SIMILAR_SURNAME':[ExactMatch('given_name'), StringFuzzy('surname', threshold=0.65)]
}

def test_initialise_class():
    dupe_checker = DuplicateChecker(df_febrl1)

def test_create_canditate_links():
    from pandas import MultiIndex

    dupe_checker = DuplicateChecker(df_febrl1)
    candidate_links = dupe_checker._create_candidate_links(test_search_patterns['SIMILAR_SURNAME'])
    
    assert isinstance(candidate_links, MultiIndex)

def test_find_duplicate_pairs():
    dupe_checker = DuplicateChecker(df_febrl1)
    candidate_links = dupe_checker._create_candidate_links(test_search_patterns['SIMILAR_SURNAME'])
    pairs = dupe_checker._find_duplicate_pairs(candidate_links, test_search_patterns['SIMILAR_SURNAME'])
    
    assert isinstance(pairs, list)
    assert isinstance(pairs[0], tuple)

def test_create_groups():
    dupe_checker = DuplicateChecker(df_febrl1)
    candidate_links = dupe_checker._create_candidate_links(test_search_patterns['SIMILAR_SURNAME'])
    pairs = dupe_checker._find_duplicate_pairs(candidate_links, test_search_patterns['SIMILAR_SURNAME'])
    groups = dupe_checker._create_duplicate_groups(pairs)

def test_create_one_groups_people_df_simple_test_case():
    dupe_checker = DuplicateChecker(people_df)

    candidate_links = dupe_checker._create_candidate_links(test_search_patterns['SIMILAR_SURNAME'])
    assert len(candidate_links) == 3

    pairs = dupe_checker._find_duplicate_pairs(candidate_links, test_search_patterns['SIMILAR_SURNAME'])
    assert len(pairs) == 3

    groups = dupe_checker._create_duplicate_groups(pairs)
    assert len(groups) == 1 #Forms one group as they're all pairs