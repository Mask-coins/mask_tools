import random
import pandas
from typing import List,Set,Union
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class ChooseGreedy(object):
    def __init__(self,k,epsilon,user_list:tuple):
        self.epsilon = [epsilon]
        self.esum = epsilon
        r = ChooseGreedy.RandRule()
        r.set_candidate(user_list)
        self.rule = [r]  # type:List[ChooseGreedy.Rule]
        self.chosen = None  # type:Set[int]
        self.K = k  # type:int

    class Rule:
        def __init__(self):
            self.candidate = None  # type:Union[pandas.DataFrame,pandas.Series]
            self.picked = 0

        def set_candidate(self,candidate:Union[pandas.DataFrame,pandas.Series]):
            self.candidate = candidate
            self.sort()

        def sort(self):
            if isinstance(self.candidate, pandas.Series):
                self.candidate=self.candidate.sample(frac=1)
                self.candidate.sort_values(ascending=False, inplace=True)
            elif isinstance(self.candidate,pandas.DataFrame):
                self.candidate=self.candidate.sample(frac=1)
                self.candidate.sort_values(1, ascending=False, inplace=True)
                self.candidate.reset_index()

        def pick(self):
            if isinstance(self.candidate, pandas.Series):
                user_id = self.candidate.index[self.picked]
            elif isinstance(self.candidate,pandas.DataFrame):
                user_id = self.candidate.iat[self.picked, 0]
            self.picked += 1
            return user_id

        def reset(self):
            self.picked = 0

    class RandRule(Rule):
        def __init__(self):
            super().__init__()
            self.candidate = None  # type:tuple

        def set_candidate(self,candidate:tuple):
            self.candidate = candidate

        def pick(self):
            r = random.randrange(0,len(self.candidate))
            user_id = self.candidate[r]
            return user_id

    def set_rule(self, epsilon ,candidate:pandas.DataFrame):
        self.epsilon.append(epsilon)
        rule = ChooseGreedy.Rule()
        rule.set_candidate(candidate)
        self.rule.append(rule)
        self.esum += epsilon
        if self.esum > 1.0001:
            raise ValueError('確率の合計値が1ではありません')

    def select_rule(self):
        rand = random.random()
        rule_poz = 0
        s = 0
        for e in self.epsilon:
            s += e
            if s > rand:
                return rule_poz
            rule_poz += 1
        return rule_poz

    def choose(self, print_status=False):
        if self.esum > 1.0001:
            raise ValueError('確率の合計値が1ではありません')
        self.chosen = set()
        k = 0
        while k < self.K:
            rule_poz = self.select_rule()
            user_id = self.rule[rule_poz].pick()
            # print('r='+str(rule_poz)+' : '+'u='+str(user_id))
            if user_id in self.chosen:
                continue
            self.chosen.add(user_id)
            k+=1
        if print_status:
            self.print()
        for r in self.rule:
            r.reset()
        return self.chosen

    def print(self):
        for r in self.rule:
            if type(r) == ChooseGreedy.RandRule:
                continue
            print('pick num : ' + str(r.picked))
            if isinstance(r.candidate,pandas.Series):
                print(r.candidate.index)
            if isinstance(r.candidate,pandas.DataFrame):
                print(r.candidate.T)


class TargetVectorSimilarity(object):
    def __init__(self,target):
        self.t = target
        self.m = target.reshape((1,-1))
        self.n = np.linalg.norm(target)

    def cos(self,t):
        return np.dot(self.t,t)/(np.linalg.norm(t)*self.n)

    def cos_samples(self,t):
        return cosine_similarity(self.m,t)[0]


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

    def get_present(self) -> pd.Series:
        return self.present[self.poz]

    def get_prev(self) -> pd.Series:
        return self.present[self.poz-1]

    def get_accumulated(self) -> pd.Series:
        if self.poz == 0:
            return 0
        return self.accumulated[self.poz]

    def get_accumulated_prev(self) -> pd.Series:
        if self.poz == 0:
            return 0
        return self.accumulated[self.poz-1]

    def print(self):
        print(self.present.name)
        print(self.present)
        print(self.accumulated.name)
        print(self.accumulated)



