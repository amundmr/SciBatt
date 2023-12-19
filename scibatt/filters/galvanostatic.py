import pandas as pd
from scibatt.config import *

def transform_timebased(data, exp_time = True):
    x = []
    y = []
    for key, value in data.items():
        x.append((value[COLUMN_NAME_TIME]-value[COLUMN_NAME_TIME].iloc[0]).to_numpy())
        y.append(value[COLUMN_NAME_VOLTAGE1].to_numpy())
    return (x, y)

def transform_capacitybased(data, unit = "As"):
    x = []
    y = []
    z = []
    for key, df in data.items():
        # Convert to experiment time
        df[COLUMN_NAME_TIME] = df[COLUMN_NAME_TIME]-df[COLUMN_NAME_TIME].iloc[0]

        # Calculate the change in COLUMN_NAME_TIME
        df['dt'] = df[COLUMN_NAME_TIME].diff()

        # Calculate the cumulative product of "I" and "dt"
        df[COLUMN_NAME_CHARGE] = df[COLUMN_NAME_CURRENT] * df['dt'].fillna(0).cumsum()

        if unit == "mAh":
            df[COLUMN_NAME_CHARGE] = df[COLUMN_NAME_CHARGE]*1000/60/60

        x.append(df[COLUMN_NAME_CHARGE].to_numpy())
        y.append(df[COLUMN_NAME_VOLTAGE1].to_numpy())
        z.append(df[COLUMN_NAME_CURRENT].to_numpy())
    return (x, y, z)

def transform_raw(data):
    dfs = []
    for key, df in data.items():
        dfs.append(df)
    concat = pd.concat(dfs)
    return (concat[COLUMN_NAME_TIME].to_numpy(), concat[COLUMN_NAME_VOLTAGE1].to_numpy(), concat[COLUMN_NAME_CURRENT].to_numpy())