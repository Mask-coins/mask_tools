import pytest
import pandas as pd
import numpy as np
import math
from src.mask_tools import mask_small_kits as msk

def set_data_Greedy():
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

def test_Greedy():
    k = 5
    user_id,candidate1,candidate2 = set_data_Greedy()
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



if __name__ == '__main__':
    test_Greedy()
    test_TargetVectorSimilarity()


