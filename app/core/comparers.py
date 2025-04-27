from recordlinkage.compare import( 
    Exact, 
    String,
    BaseCompareFeature
)
from pandas import Series
import numpy as np
import regex as re


class DateFuzzy(BaseCompareFeature):
    def __init__(self, column, max_day_diff:int=7):
        super().__init__(column, column)
        self.max_day_diff = max_day_diff
    
    
    def _compute_vectorized(self, s_left:Series, s_right:Series):
        if s_left.dtype != "datetime64[ns]" or s_right.dtype != "datetime64[ns]":
            raise ValueError('Non datetime series passed to date fuzzy match')
        c = np.zeros(shape=(len(s_left), 1)) 

        #exact match
        c[s_left == s_right] = 1

        #Within specified date threshold
        c[abs(s_left - s_right).dt.days <= self.max_day_diff] = 1

        #Day month swapped
        c[(s_left.dt.year == s_right.dt.year) & (s_left.dt.month == s_right.dt.day) & (s_right.dt.month == s_left.dt.day)] = 1

        return c

class StringFuzzy(String):
    def __init__(self, column:str, prefixes_to_remove:list[str]=[], suffixes_to_remove:list[str]=[]):
        super().__init__(column, column, threshold=0.9)
        self.threshold = 0.9
        self.prefixes_to_remove = prefixes_to_remove
        self.suffixes_to_remove = suffixes_to_remove

    #TODO: you dont need to check the threshold here    
    def _compute_vectorized(self, s_left, s_right):
        s_left = self._clean_strings(s_left)
        s_right = self._clean_strings(s_right)
        c = super()._compute_vectorized(s_left, s_right)
        return (c >= self.threshold).to_numpy(dtype=np.int64)
    
    def _clean_strings(self, s:Series):
        for prefix in self.prefixes_to_remove:
            s = s.str.removeprefix(prefix)
        for suffix in self.suffixes_to_remove:
            s = s.str.removesuffix(suffix)
    
        s = s.apply(lambda x: re.sub(r'[^a-zA-Z0-9]', '', x))

        return s

class NumericFuzzy(BaseCompareFeature):
    def __init__(self, column:str):
        super().__init__(column, column)

    def _compute_vectorized(self, s_left:Series, s_right:Series):
        c = np.zeros(shape=(1, len(s_left)))

        #Exact match
        c[s_left == s_right] = 1

        #TODO: Add funcs for fuzzy match

        return c

        



        

