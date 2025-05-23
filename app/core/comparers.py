from recordlinkage.compare import( 
    Exact, 
    String,
    BaseCompareFeature
)
from pandas import Series
import numpy as np
import regex as re

#TODO: Add Different Comparer

class ExactMatch(Exact):
    def __init__(self, column:str):
        super().__init__(column, column, label=column)
        self.column = column

class DateFuzzy(BaseCompareFeature):
    def __init__(self, column, max_day_diff:int=7):
        super().__init__(column, column, label=column)
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
    #TODO: look how the parent uses the threshold variable
    def __init__(self, column:str, prefixes_to_remove:list[str]=[], suffixes_to_remove:list[str]=[], threshold:float=0.9):
        super().__init__(column, column, threshold=threshold, label=column)
        self.threshold = threshold
        self.prefixes_to_remove = prefixes_to_remove
        self.suffixes_to_remove = suffixes_to_remove

    #TODO: you dont need to check the threshold here    
    def _compute_vectorized(self, s_left, s_right):
        s_left = self._clean_strings(s_left)
        s_right = self._clean_strings(s_right)
        c = super()._compute_vectorized(s_left, s_right)
        return (c >= self.threshold).to_numpy(dtype=np.int64)
    
    #TODO: data preprocessing should happen before comparing (maybe move to a seperate module)
    def _clean_strings(self, s:Series):
        for prefix in self.prefixes_to_remove:
            s = s.str.removeprefix(prefix)
        for suffix in self.suffixes_to_remove:
            s = s.str.removesuffix(suffix)
        
        s = s.str.lower()
        s = s.apply(lambda x: re.sub(r'[^a-zA-Z0-9]', '', x) if isinstance(x, str)  else x)

        return s

class NumericFuzzy(BaseCompareFeature):
    def __init__(self, column:str, max_value_diff:float=0):
        super().__init__(column, column, label=column)
        self.max_value_diff = max_value_diff

    def _compute_vectorized(self, s_left:Series, s_right:Series):
        c = np.zeros(shape=(1, len(s_left)))

        #Exact match
        c[s_left == s_right] = 1

        #Within Value Threshold
        c[(s_left - s_right).abs() < self.max_value_diff]
        #TODO: Add funcs for fuzzy match

        return c

        



        

