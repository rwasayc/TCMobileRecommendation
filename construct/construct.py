import pandas as pd
from const import csv_path, behavior


# 按周期切割数据并存入csv文件
def build_df_part():
    batch = 0
    dfs = pd.read_csv(open(csv_path.TRAIN_USER_CSV_PATH, 'r'),
                      parse_dates=['time'],
                      index_col=['time'],
                      date_parser=lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H'),
                      chunksize=500000)

    col = ['user_id', 'item_id', 'behavior_type', 'item_category']

    for df in dfs:
        try:
            df_part_1 = df['2014-11-22':'2014-11-27']
            df_part_1_test = df['2014-11-28']

            df_part_2 = df['2014-11-29':'2014-12-04']
            df_part_2_test = df['2014-12-05']

            df_part_3 = df['2014-12-13':'2014-12-18']

            df_part_1.to_csv(csv_path.TRAIN_USER_DF_CSV_ONE, columns=col, header=False, mode='a')
            df_part_1_test.to_csv(csv_path.TRAIN_USER_DF_CSV_ONE_VERIFICATION, columns=col, header=False, mode='a')

            df_part_2.to_csv(csv_path.TRAIN_USER_DF_CSV_TWO, columns=col, header=False, mode='a')
            df_part_2_test.to_csv(csv_path.TRAIN_USER_DF_CSV_TWO_VERIFICATION, columns=col, header=False, mode='a')

            df_part_3.to_csv(csv_path.TRAIN_USER_DF_CSV_THREE, columns=col, header=False, mode='a')

            batch += 1
            print('chunk 【%d】 done.' % batch)

        except StopIteration:
            print("slice finish.")
            break


def build_df_label():
    all_part_paths = [
        [csv_path.TRAIN_USER_DF_CSV_ONE, csv_path.TRAIN_USER_DF_CSV_ONE_VERIFICATION,
         csv_path.TRAIN_USER_DF_CSV_ONE_LABEL],
        [csv_path.TRAIN_USER_DF_CSV_TWO, csv_path.TRAIN_USER_DF_CSV_TWO_VERIFICATION,
         csv_path.TRAIN_USER_DF_CSV_TWO_LABEL],
    ]
    col = ['time', 'user_id', 'item_id', 'behavior_type', 'item_category']
    index = 1
    for paths in all_part_paths:
        df_file = open(paths[0], 'r')
        try:
            df_part = pd.read_csv(df_file, index_col=False)
            df_part.columns = col
        finally:
            df_file.close()
        print("df_file done index:", index)

        df_part_uic = df_part.drop_duplicates(['user_id', 'item_id', 'item_category'])[
            ['user_id', 'item_id', 'item_category']]

        ver_file = open(paths[1], 'r')
        try:
            df_part_v = pd.read_csv(ver_file, index_col=False, parse_dates=[0])
            df_part_v.columns = col
        finally:
            ver_file.close()
        print("ver_file done index:", index)

        df_part_label_1 = df_part_v[df_part_v['behavior_type'] == behavior.CONST_BUY][
            ['user_id', 'item_id', 'item_category']]
        df_part_label_1.drop_duplicates(['user_id', 'item_id'], 'last', inplace=True)
        df_part_label_1['label'] = 1
        df_part_uic_label = pd.merge(df_part_uic,
                                     df_part_label_1,
                                     on=['user_id', 'item_id', 'item_category'],
                                     how='left').fillna(0).astype('int')
        df_part_uic_label.to_csv(paths[2], index=False)

        print("path done index:", index)
        index += 1

    df_file = open(csv_path.TRAIN_USER_DF_CSV_THREE, 'r')
    try:
        df_part = pd.read_csv(df_file, index_col=False)
        df_part.columns = col
    finally:
        df_file.close()

    df_part_uic = df_part.drop_duplicates(['user_id', 'item_id', 'item_category'])[
        ['user_id', 'item_id', 'item_category']]
    df_part_uic.to_csv(csv_path.TRAIN_USER_DF_CSV_THREE_UIC, index=False)


# csv_path.init_path()
# build_df_part()

# build_df_label()
