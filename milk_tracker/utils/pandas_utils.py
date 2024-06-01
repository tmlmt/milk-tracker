import pandas as pd


def prepend_series_to_df(series: pd.Series, df: pd.DataFrame) -> pd.DataFrame:
    """Prepend a Series to a Dataframe.

    As a Series in the other axis and can't be transposed, using concat
    requires a double transpose. This takes more time than prepending
    the series to the existing DataFrame.
    Source: https://stackoverflow.com/questions/68471583/concating-series-returned-from-iloc0-with-an-existing-dataframe

    Args:
    ----
        series (pd.Series): the series to prepend
        df (pd.DataFrame): the DataFrame to extend

    Returns:
    -------
        pd.DataFrame: resulting DataFrame

    """
    data = df.values.tolist()
    data.insert(0, series.tolist())
    return pd.DataFrame(data, columns=df.columns)


def append_series_to_df(series: pd.Series, df: pd.DataFrame) -> pd.DataFrame:
    """Append a Series to a DataFrame.

    As a Series in the other axis and can't be transposed, using concat
    requires a double transpose. This takes more time than prepending
    the series to the existing DataFrame.
    Source: https://stackoverflow.com/questions/68471583/concating-series-returned-from-iloc0-with-an-existing-dataframe

    Args:
    ----
        series (pd.Series): the series to append
        df (pd.DataFrame): the DataFrame to extend

    Returns:
    -------
        pd.DataFrame: resulting DataFrame

    """
    df.loc[len(df)] = series.tolist()
    return df
