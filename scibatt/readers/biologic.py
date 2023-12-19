# -*- coding: utf-8 -*-
"""Data-readers for BioLogic"""

from galvani import BioLogic
import pandas as pd
import datetime
from scibatt.config import *

def read_mpr(filepath):

    mpr_file = BioLogic.MPRfile(filepath)
    print(mpr_file.__dir__())

    df = pd.DataFrame(mpr_file.data)

    # Modifying time
    def convert_timestamp_to_unix_epoch(time, start_timestamp):
        datetime_obj = start_timestamp + datetime.timedelta(seconds=time)
        return datetime_obj.timestamp()  # Returns unix epoch float

    df[COLUMN_NAME_TIME] = df["time/s"].apply(lambda x: convert_timestamp_to_unix_epoch(x, mpr_file.timestamp))
    df[COLUMN_NAME_CURRENT] = df["control/V/mA"].apply(lambda x: x/1000)    # Convert to Amperes

    # Rename columns to match spec
    df.rename(
        columns={
            "Ewe/V": COLUMN_NAME_VOLTAGE1,
        },
        inplace=True,
    )

    # Group by step to separate steps
    groups_step = df.groupby("Ns")

    # Scan groups and add to return dict
    data = {}
    tol = CURRENT_ZERO_TOLERANCE
    for num, group_df in groups_step:
        mean_current = group_df[COLUMN_NAME_CURRENT].mean()
        timestamp = group_df[COLUMN_NAME_TIME].iloc[0]

        # Remove columns we don't want
        required_columns = [COLUMN_NAME_TIME, COLUMN_NAME_CURRENT, COLUMN_NAME_VOLTAGE1]
        group_df = group_df.drop(columns=[col for col in df if col not in required_columns])

        if -tol < mean_current < tol:
            data[f"{timestamp}_cycling_p000.000A"] = group_df
        elif mean_current > tol:
            data[f"{timestamp}_cycling_p{mean_current:08.4f}A"] = group_df
        elif mean_current < tol:
            data[f"{timestamp}_cycling_n{mean_current:08.4f}A"] = group_df

    return data