from const import csv_path, behavior, time
import pandas as pd
import numpy as np


def get_u_b_count():
    col = ['time', 'user_id', 'item_id', 'behavior_type', 'item_category']
    targets = [
        {'train_save': csv_path.TRAIN_USER_CSV_FIRST_DATA, 'save_path': csv_path.FEATURE_U_FIRST,
         'test_date': time.TEST_DATA_FIRST},
        {'train_save': csv_path.TRAIN_USER_CSV_SECOND_DATA, 'save_path': csv_path.FEATURE_U_SECOND,
         'test_date': time.TEST_DATA_SECOND},
        {'train_save': csv_path.TRAIN_USER_CSV_THIRD_DATA, 'save_path': csv_path.FEATURE_U_THIRD,
         'test_date': time.TEST_DATA_THIRD},
    ]

    days = [6, 3, 1]
    for target in targets:
        train_file = open(target['train_save'], 'r')
        try:
            df_train_data = pd.read_csv(train_file, index_col=False, parse_dates=[0])
            df_train_data.columns = col
        finally:
            train_file.close()

        all_days_u_b_count = None
        for day in days:
            df_day_train_data = df_train_data[df_train_data['time'] >= np.datetime64(target['test_date']['time']) - day]
            df_day_train_data['cumcount'] = df_day_train_data.groupby(['user_id', 'behavior_type']).cumcount()

            u_b_count = df_day_train_data.drop_duplicates(['user_id', 'behavior_type'], 'last')[
                ['user_id', 'behavior_type', 'cumcount']]
            u_b_count['cumcount'] += 1

            u_b_count = pd.get_dummies(u_b_count['behavior_type']).join(
                u_b_count[['user_id', 'cumcount']])
            u_b_count.rename(columns={behavior.BROWSE: 'browse',
                                      behavior.COLLECT: 'collect',
                                      behavior.SHOPPING_CART: 'shopping_cart',
                                      behavior.BUY: 'buy'}, inplace=True)

            u_b_count['browse_in_%d' % day] = u_b_count['browse'] * u_b_count['cumcount']
            u_b_count['collect_in_%d' % day] = u_b_count['collect'] * u_b_count['cumcount']
            u_b_count['shopping_cart_in_%d' % day] = u_b_count['shopping_cart'] * u_b_count['cumcount']
            u_b_count['buy_in_%d' % day] = u_b_count['buy'] * u_b_count['cumcount']

            u_b_count = u_b_count.groupby('user_id').agg({'browse_in_%s' % day: np.sum,
                                                          'collect_in_%s' % day: np.sum,
                                                          'shopping_cart_in_%s' % day: np.sum,
                                                          'buy_in_%s' % day: np.sum})
            u_b_count.reset_index(inplace=True)
            u_b_count['all_in_%d' % day] = u_b_count[
                ['browse_in_%s' % day, 'collect_in_%s' % day, 'shopping_cart_in_%s' % day, 'buy_in_%s' % day]].apply(
                lambda x: x.sum(),
                axis=1)

            if all_days_u_b_count is None:
                all_days_u_b_count = u_b_count
            else:
                all_days_u_b_count = pd.merge(all_days_u_b_count, u_b_count, on=['user_id']).fillna(0)

        all_days_u_b_count.to_csv(target['save_path'], index=False)
        print("Finish target")


# get_u_b_count()
