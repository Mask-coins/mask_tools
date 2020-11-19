import random
import pandas


class ChooseGreedy(object):
    def __init__(self,k,epsilon,user_list:tuple):
        self.epsilon = [epsilon]
        self.esum = epsilon
        r = ChooseGreedy.RandRule()
        r.set_candidate(user_list)
        self.rule = [r]  # type:list[ChooseGreedy.Rule]
        self.chosen = None  # type:set[int]
        self.K = k  # type:int

    class Rule:
        def __init__(self):
            self.candidate = None # type:pandas.DataFrame
            self.picked = 0

        def set_candidate(self,candidate:pandas.DataFrame):
            self.candidate = candidate
            self.sort()

        def sort(self):
            self.candidate.sort_values(1, ascending=False, inplace=True)
            self.candidate.reset_index()

        def pick(self):
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
        if self.esum > 1:
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

    def choose(self):
        if self.esum > 1:
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
        # self.print()
        for r in self.rule:
            r.reset()
        return self.chosen

    def print(self):
        for r in self.rule:
            if type(r) == ChooseGreedy.RandRule:
                continue
            print('pick num : ' + str(r.picked))
            print(r.candidate.T)




