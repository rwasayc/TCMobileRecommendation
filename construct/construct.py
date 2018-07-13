import pandas as pd
from const import csv_path, behavior, time
from utils import csv_reader as cr


# 按周期切割数据并存入csv文件
def build_train_and_test():
    batch = 0
    df = cr.get_all_train_user_by_time()

    col = ['user_id', 'item_id', 'behavior_type', 'item_category']

    targets = [
        {'train_time': time.TRAIN_DATA_FIRST, 'test_time': time.TEST_DATA_FIRST,
         'train_save': csv_path.TRAIN_USER_CSV_FIRST_DATA, 'test_save': csv_path.TRAIN_USER_CSV_FIRST_TEST},
        {'train_time': time.TRAIN_DATA_SECOND, 'test_time': time.TEST_DATA_SECOND,
         'train_save': csv_path.TRAIN_USER_CSV_SECOND_DATA, 'test_save': csv_path.TRAIN_USER_CSV_SECOND_TEST},
        {'train_time': time.TRAIN_DATA_THIRD, 'train_save': csv_path.TRAIN_USER_CSV_THIRD_DATA},
    ]

    for data in df:
        try:
            for target in targets:
                train_data = data[target['train_time']['start_time']:target['train_time']['end_time']]
                train_data.to_csv(target['train_save'], columns=col, header=False, mode='a')

                if 'test_time' in target.keys():
                    test_data = data[target['test_time']['time']]
                    test_data.to_csv(target['test_save'], columns=col, header=False, mode='a')

            batch += 1
            print('chunk 【%d】 done.' % batch)

        except StopIteration:
            print("slice finish.")
            break


def build_label():
    targets = [
        {'train_save': csv_path.TRAIN_USER_CSV_FIRST_DATA, 'test_save': csv_path.TRAIN_USER_CSV_FIRST_TEST,
         'label_save': csv_path.TRAIN_USER_CSV_FIRST_LABEL},
        {'train_save': csv_path.TRAIN_USER_CSV_FIRST_DATA, 'test_save': csv_path.TRAIN_USER_CSV_SECOND_TEST,
         'label_save': csv_path.TRAIN_USER_CSV_SECOND_LABEL}
    ]
    col = ['time', 'user_id', 'item_id', 'behavior_type', 'item_category']

    for target in targets:
        train_file = open(target['train_save'], 'r')
        try:
            df_train = pd.read_csv(train_file, index_col=False)
            df_train.columns = col
        finally:
            train_file.close()

        uic_data = df_train.drop_duplicates(['user_id', 'item_id', 'item_category'])[
            ['user_id', 'item_id', 'item_category']]

        test_file = open(target['test_save'], 'r')
        try:
            df_test = pd.read_csv(test_file, index_col=False, parse_dates=[0])
            df_test.columns = col
        finally:
            test_file.close()

        label_data = df_test[df_test['behavior_type'] == behavior.BUY][
            ['user_id', 'item_id', 'item_category']]
        label_data.drop_duplicates(['user_id', 'item_id'], 'last', inplace=True)
        label_data['label'] = 1
        uic_label = pd.merge(uic_data, label_data,
                             on=['user_id', 'item_id', 'item_category'],
                             how='left').fillna(0).astype('int')

        uic_label.to_csv(target['label_save'], index=False)

# csv_path.init_path()
# build_train_and_test()
# build_label()
