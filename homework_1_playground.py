"""testing grounds"""

import math
import os

import pandas as pd


def main() -> None:
    """main"""
    COLUMN_NAMES = {
        "timestamp": "timestamp",
        "LinearAccelerometerSensor": "Linear_Acc",
        "AccX": "Acc_X",
        "AccY": "Acc_Y",
        "AccZ": "Acc_Z",
    }
    arduino_df = pd.read_csv(
        os.path.join(os.curdir, "data", "ie5640_assignment_1.csv"),
        dtype={col: (int if col == "Timestamp" else float) for col in COLUMN_NAMES},
    )[[s for s in COLUMN_NAMES]]
    timestamps = arduino_df["timestamp"] // 1000
    print(
        {
            len(timestamps[(timestamps >= unix_int) & (timestamps < unix_int + 1)])
            for unix_int in timestamps.iloc[20:-20]
        }
    )  # prints {15}


if __name__ == "__main__":
    main()
