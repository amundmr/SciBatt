# -*- coding: utf-8 -*-
"""Data-readers for Gamry"""

import gamry_parser
import pandas as pd
from scibatt.config import COLUMN_NAMES, CURRENT_ZERO_TOLERANCE


REGULAR_EXP_HEADER_NAMES = ["T", "Vf", "Im"]
REGULAR_EXP_TYPES = ["PWR800_CHARGE", "PWR800_DISCHARGE", "PWR800_READVOLTAGE"]
EIS_EXP_TYPE = "GALVEIS"



def read_dta(filepath):
    gp = gamry_parser.GamryParser(filename=filepath)
    gp.load()
    data = {}

    if gp.get_experiment_type() in REGULAR_EXP_TYPES:
        #gp._convert_T_to_Timestamp() # This tries to check if day is first in the string, but the check fails.
        # The following is my own implementation, simply always assuming day first.

        start_time = pd.to_datetime(
            gp.header["DATE"] + " " + gp.header["TIME"],
            dayfirst=True,
        )
        for curve in gp.curves:
            curve["T"] = start_time + pd.to_timedelta(curve["T"], "s")

        for curve_num in range(gp.curve_count):
            df = gp.curves[curve_num].rename(columns={
                "T":COLUMN_NAMES["TIME"], 
                "Vf":COLUMN_NAMES["VOLTAGE1"], 
                "Im":COLUMN_NAMES["CURRENT"]},
                )
            df = df[[COLUMN_NAMES["TIME"], COLUMN_NAMES["VOLTAGE1"], COLUMN_NAMES["CURRENT"]]]
            df[COLUMN_NAMES["TIME"]] = df[COLUMN_NAMES["TIME"]].apply(lambda x: x.timestamp())
            df = df.sort_values("t")

            mean_current = df[COLUMN_NAMES["CURRENT"]].mean()
            timestamp = df[COLUMN_NAMES["TIME"]].iloc[0]

            if -CURRENT_ZERO_TOLERANCE < mean_current < CURRENT_ZERO_TOLERANCE:
                data[f"{timestamp}_cycling_p000.000A"] = df
            elif mean_current > CURRENT_ZERO_TOLERANCE:
                data[f"{timestamp}_cycling_p{mean_current:08.4f}A"] = df
            elif mean_current < CURRENT_ZERO_TOLERANCE:
                data[f"{timestamp}_cycling_n{mean_current:08.4f}A"] = df

    return data
    