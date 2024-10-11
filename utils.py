"""shared functions for multiple hoemworks"""

import pandas as pd


def normalize_df(
    _dataframe: pd.DataFrame, *cols: str, rescale: bool = False
) -> pd.DataFrame:
    """normalizes a dataframe

    args:
        - _dataframe (pd.DataFrame)
        - *cols: cols that are normalized, default: ALL
        - rescale (bool) \n
    returns:
        - `pd.DataFrame`
    """

    _to_drop = [
        col
        for col in _dataframe.columns
        if not pd.api.types.is_numeric_dtype(_dataframe[col])
        or (cols and col not in cols)
    ]
    _cleaned_df = _dataframe.drop(columns=_to_drop)
    _norm_df: pd.DataFrame
    if rescale:
        _norm_df = (_cleaned_df - _cleaned_df.min()) / (
            _cleaned_df.max() - _cleaned_df.min()
        )
    else:
        _norm_df = (_cleaned_df - _cleaned_df.mean()) / _cleaned_df.std()

    return _dataframe[_to_drop].merge(
        _norm_df, "left", left_index=True, right_index=True
    )
