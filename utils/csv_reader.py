import pandas as pd
from const import csv_path


def get_all_train_user_by_time():
    return pd.read_csv(open(csv_path.TRAIN_USER_CSV_PATH, 'r'),
                       parse_dates=['time'],
                       index_col=['time'],
                       date_parser=lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H'),
                       chunksize=500000)
