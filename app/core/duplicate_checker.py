from recordlinkage.base import BaseCompareFeature
from recordlinkage.compare import Exact
from recordlinkage import Compare, Index
from pandas import DataFrame

"""
The indexer makes the candidate links
You then pass these candidate links to the comparer

Based on the search pattern the duplicate checkers needs to create the candidate links and the 
"""

class DuplicateChecker():
    def __init__(self, df:DataFrame):
        """
        df is the dataframe which we want to find duplicates in
        This class is responsible for taking a list of comparer and efficiently finding duplicate groups
        """
        self.df = df
    
    def find_duplicates(self, pattern_name:str, pattern:list[BaseCompareFeature])->DataFrame:
        candidate_links = self._create_candidate_links(pattern)
        identified_duplicates = self._find_duplicate_pairs(candidate_links, pattern)
        ...
    
    def _create_candidate_links(self, pattern:list[BaseCompareFeature])->DataFrame:
        """
        uses the search patterns to create the candidate links dataframe.
        Specifically creates blocks for exact comparers
        """
        index = Index()
        for comparer in pattern:
            if isinstance(comparer, Exact):
                index.block(comparer.column)
        
        candidate_links = index.index(self.df)
        
        return candidate_links
    
    def _find_duplicate_pairs(self, candidate_links:DataFrame, pattern:list[BaseCompareFeature])->DataFrame:
        compare = Compare()
        for comparer in pattern:
            compare.add(compare)
        
        features = compare.compute(candidate_links, self.df)
        identified_duplicates = features[features.sum(axis=1) == len(features.columns)].index #All features are 1
        
        return identified_duplicates

    def _create_duplicate_group(self):
        ...
        
    



    

    
    
