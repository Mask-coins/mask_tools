import pytest
import pandas as pd
import numpy as np
import math
from src.mask_tools import mask_small_kits as msk
from scipy.sparse import  csr_matrix

def set_data_Greedy_Dataframe():
    user_id = [1,6,3,9,2,4,7,3]
    reward1 = [1,1,3,6,3,5,7,7]
    reward2 = [4,2,6,8,6,3,2,6]
    candidate1 = [user_id,reward1]
    candidate2 = [user_id,reward2]
    candidate1 = pd.DataFrame(candidate1)
    candidate2 = pd.DataFrame(candidate2)
    candidate1 = candidate1.T
    candidate2 = candidate2.T
    return user_id,candidate1,candidate2

def set_data_Greedy_Series():
    user_id = [1,6,3,9,2,4,7,3]
    reward1 = [10,10,30,60,30,50,70,70]
    reward2 = [400,200,600,800,600,300,200,600]
    candidate1 = pd.Series(data=reward1, index=user_id)
    candidate2 = pd.Series(data=reward2, index=user_id)
    candidate1 = candidate1.T
    candidate2 = candidate2.T
    return user_id,candidate1,candidate2

def test_Greedy_Dataframe():
    k = 5
    user_id,candidate1,candidate2 = set_data_Greedy_Dataframe()
    b = msk.ChooseGreedy(k, 0.1, tuple(user_id))
    b.set_rule(0.4, candidate1)
    with pytest.raises(ValueError):
        b.set_rule(0.6, candidate2)
    b = msk.ChooseGreedy(5, 0.0, tuple(user_id))
    b.set_rule(0.5, candidate1)
    b.set_rule(0.5, candidate2)
    u = b.choose()
    # print(u)
    assert len(u) == k

def test_Greedy_Series():
    k = 5
    user_id,candidate1,candidate2 = set_data_Greedy_Series()
    b = msk.ChooseGreedy(k, 0.1, tuple(user_id))
    b.set_rule(0.4, candidate1)
    with pytest.raises(ValueError):
        b.set_rule(0.6, candidate2)
    b = msk.ChooseGreedy(5, 0.0, tuple(user_id))
    b.set_rule(0.5, candidate1)
    b.set_rule(0.5, candidate2)
    u = b.choose(print_status=True)
    print(u)
    assert len(u) == k
    for _ in range(10000):
        b = msk.ChooseGreedy(5,1.0,tuple(user_id))
        u = b.choose(print_status=True)


def test_TargetVectorSimilarity():
    sp = msk.TargetVectorSimilarity(np.array([0,0,1,1,3,4]))
    t = np.array([1,2,4,0,3,4])
    d = 0
    at = 0
    asp = 0
    for i in range(len(t)):
        d += sp.t[i] * t[i]
        at += t[i] * t[i]
        asp += sp.t[i] * sp.t[i]
    assert abs(sp.cos(t) - d/math.sqrt(at*asp)) < 0.0001
    sp = msk.TargetVectorSimilarity(np.array([0,0,1,1,3,4]))
    t = csr_matrix([[1,2,4,0,3,4],[0,0,1,0,2,0]])
    ans = sp.cos_samples(t)
    assert abs(ans[0] - d/math.sqrt(at*asp)) < 0.0001


def test_data_frame_column_updater():
    q = msk.DataFrameColumnUpdater(index=[10,20,30])
    s = pd.Series([3,6],index=[10,20])
    q.update(s)
    s = pd.Series([3,6],index=[10,20])
    f = pd.Series([1,0,1], index=[10,20,30])
    q.update_chosen(s,f)
    assert (q.get_accumulated().values - np.array([6.0, 6.0, 0.0])).sum() == 0


if __name__ == '__main__':
    test_Greedy_Dataframe()
    test_Greedy_Series()
    test_TargetVectorSimilarity()
    test_data_frame_column_updater()



