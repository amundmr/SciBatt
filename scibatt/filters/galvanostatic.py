
def transform_timebased(data, exp_time = True):
    x = []
    y = []
    for key, value in data.items():
        x.append((value["t"]-value["t"].iloc[0]).to_numpy())
        y.append(value["U1"].to_numpy())
    return (x, y)

def transform_capacitybased(data, unit = "As"):
    x = []
    y = []
    z = []
    for key, df in data.items():
        # Convert to experiment time
        df["t"] = df["t"]-df["t"].iloc[0]

        # Calculate the change in "t"
        df['dt'] = df['t'].diff()

        # Calculate the cumulative product of "I" and "dt"
        df['Q'] = df['I'] * df['dt'].fillna(0).cumsum()

        if unit == "mAh":
            df["Q"] = df["Q"]*1000/60/60

        x.append(df["Q"].to_numpy())
        y.append(df["U1"].to_numpy())
        z.append(df["I"].to_numpy())
    return (x, y, z)