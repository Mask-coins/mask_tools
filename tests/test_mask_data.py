from src.mask_tools import mask_data as md
import pandas as pd
import numpy as np

def test_data_frame_column_accumulate_updater():
    q = md.DataFrameColumnAccumulateUpdater(index=[10, 20, 30])
    s = pd.Series([3,6],index=[10,20])
    q.update(s)
    s = pd.Series([3,6],index=[10,20])
    f = pd.Series([1,0,1], index=[10,20,30])
    q.update_chosen(s,f)
    assert (q.get_accumulated().values - np.array([6.0, 6.0, 0.0])).sum() == 0


def test_series_accumulate_updater():
    q = md.SeriesAccumulateUpdater(5)
    q.update(3)
    q.update(6)
    q.update(12)
    q.print()

def test_dataframe_to_dict():
    df = pd.DataFrame([
        [1,1,1,1],
        [1,1,1,2],
        [1,2,2,3],
        [1,2,2,4],
        [2,3,3,5],
        [2,3,3,6],
        [2,4,4,7],
        [2,4,4,8]] ,index=[10,20,30,40,50,60,70,80], columns=['c1','c2','c3','c4'])
    print(md.dataframe_to_dict(df, index=['c1','c2','c3']))
    print(md.dataframe_to_dict(df, index=['c1','c2','c3'], drop_group_column=False))


if __name__ == '__main__':
    test_data_frame_column_accumulate_updater()
    test_series_accumulate_updater()
    test_dataframe_to_dict()
