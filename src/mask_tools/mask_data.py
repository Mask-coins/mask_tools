from typing import Union, Sequence
import numpy as np
import pandas as pd


class DataFrameColumnAccumulateUpdater(object):
    def __init__(self, index, name='table_name'):
        self.name = name
        self.poz = -1
        self.present = pd.DataFrame(index=index)
        self.accumulated = pd.DataFrame(index=index)
        self.ones = pd.Series(np.ones(len(index)), index=index)
        self.zeros = pd.Series(np.zeros(len(index)), index=index)

    def update(self, s:Union[pd.Series,np.ndarray]) -> None:
        self.poz += 1
        self.present[self.poz] = s.mul(self.ones, fill_value=0)
        if self.poz == 0:
            self.accumulated[self.poz] = self.present[self.poz]
        else:
            self.accumulated[self.poz] = self.accumulated[self.poz-1] + self.present[self.poz]

    def update_chosen(self, s:Union[pd.Series,np.ndarray], chosen_series:Union[pd.Series,np.ndarray]) -> None:
        self.poz += 1
        self.present[self.poz] = s.mul(chosen_series, fill_value=0)
        if self.poz == 0:
            self.accumulated[self.poz] = self.present[self.poz]
        else:
            self.accumulated[self.poz] = self.accumulated[self.poz-1] + self.present[self.poz]

    def get_present(self) -> pd.Series:
        return self.present[self.poz]

    def get_prev(self) -> pd.Series:
        return self.present[self.poz-1]

    def get_accumulated(self) -> pd.Series:
        if self.poz == 0:
            return self.zeros
        return self.accumulated[self.poz]

    def get_accumulated_prev(self) -> pd.Series:
        if self.poz == 0:
            return self.zeros
        return self.accumulated[self.poz-1]

    def print(self):
        print(self.name+' : present')
        print(self.present)
        print(self.name+' : accumulated')
        print(self.accumulated)


class SeriesAccumulateUpdater(object):
    def __init__(self, length , name='series'):
        self.name = name
        self.poz = -1
        self.len = length
        self.present = pd.Series(name=name+'present', index=range(self.len))
        self.accumulated = pd.Series(name=name+'accumulated', index=range(self.len))

    def update(self, s) -> None:
        self.poz += 1
        self.present[self.poz] = s
        if self.poz == 0:
            self.accumulated[self.poz] = s
        else:
            self.accumulated[self.poz] = s+self.accumulated[self.poz-1]

    def get_present(self):
        return self.present[self.poz]

    def get_prev(self) -> pd.Series:
        return self.present[self.poz-1]

    def get_accumulated(self):
        if self.poz == 0:
            return 0
        return self.accumulated[self.poz]

    def get_accumulated_prev(self):
        if self.poz == 0:
            return 0
        return self.accumulated[self.poz-1]

    def print(self):
        print(self.present.name)
        print(self.present)
        print(self.accumulated.name)
        print(self.accumulated)


def dataframe_to_dict(p,index:Sequence, drop_group_column=True):
    if len(index) == 0:
        return p
    g = p.groupby(index[0])
    if drop_group_column:
        return {x: dataframe_to_dict(g.get_group(x).drop(index[0], axis=1),index[1:], drop_group_column=True) for x in g.groups}
    return {x: dataframe_to_dict(g.get_group(x).drop(index[0], axis=1),index[1:], drop_group_column=False) for x in g.groups}





