import os

TRAIN_USER_CSV_PATH = '../source/fresh_comp_offline/tianchi_fresh_comp_train_user.csv'
TRAIN_ITEM_CSV_PATH = '../Tianchi-BigData/data/fresh_comp_offline/tianchi_fresh_comp_train_item.csv'


SAVE_BASE_PATH = '../data'

TRAIN_USER_CSV_FIRST_DATA = '%s/train/p1_user_data.csv' % SAVE_BASE_PATH
TRAIN_USER_CSV_FIRST_TEST = '%s/train/p1_user_test.csv' % SAVE_BASE_PATH
TRAIN_USER_CSV_FIRST_LABEL = '%s/train/p1_user_label.csv' % SAVE_BASE_PATH

TRAIN_USER_CSV_SECOND_DATA = '%s/train/p2_user_data.csv' % SAVE_BASE_PATH
TRAIN_USER_CSV_SECOND_TEST = '%s/train/p2_user_test.csv' % SAVE_BASE_PATH
TRAIN_USER_CSV_SECOND_LABEL = '%s/train/p2_user_label.csv' % SAVE_BASE_PATH

TRAIN_USER_CSV_THIRD_DATA = '%s/train/p3_user_data.csv' % SAVE_BASE_PATH
TRAIN_USER_CSV_THIRD_LABEL = '%s/train/p3_user_data.csv' % SAVE_BASE_PATH


FEATURE_U_FIRST = '%s/feature/u_1.csv' % SAVE_BASE_PATH
FEATURE_U_SECOND = '%s/feature/u_2.csv' % SAVE_BASE_PATH
FEATURE_U_THIRD = '%s/feature/u_3.csv' % SAVE_BASE_PATH

FEATURE_I_FIRST = '%s/feature/i_1.csv' % SAVE_BASE_PATH
FEATURE_I_SECOND = '%s/feature/i_2.csv' % SAVE_BASE_PATH
FEATURE_I_THIRD = '%s/feature/i_3.csv' % SAVE_BASE_PATH

FEATURE_C_FIRST = '%s/feature/c_1.csv' % SAVE_BASE_PATH
FEATURE_C_SECOND = '%s/feature/c_2.csv' % SAVE_BASE_PATH
FEATURE_C_THIRD = '%s/feature/c_3.csv' % SAVE_BASE_PATH

FEATURE_IC_FIRST = '%s/feature/ic_1.csv' % SAVE_BASE_PATH
FEATURE_IC_SECOND = '%s/feature/ic_2.csv' % SAVE_BASE_PATH
FEATURE_IC_THIRD = '%s/feature/ic_3.csv' % SAVE_BASE_PATH

FEATURE_UI_FIRST = '%s/feature/ui_1.csv' % SAVE_BASE_PATH
FEATURE_UI_SECOND = '%s/feature/ui_2.csv' % SAVE_BASE_PATH
FEATURE_UI_THIRD = '%s/feature/ui_3.csv' % SAVE_BASE_PATH

FEATURE_UC_FIRST = '%s/feature/uc_1.csv' % SAVE_BASE_PATH
FEATURE_UC_SECOND = '%s/feature/uc_2.csv' % SAVE_BASE_PATH
FEATURE_UC_THIRD = '%s/feature/uc_3.csv' % SAVE_BASE_PATH


def init_path():
    if not os.path.isdir(SAVE_BASE_PATH):
        os.makedirs(SAVE_BASE_PATH)
    if not os.path.isdir('%s/train' % SAVE_BASE_PATH):
        os.makedirs('%s/train' % SAVE_BASE_PATH)
    if not os.path.isdir('%s/feature' % SAVE_BASE_PATH):
        os.makedirs('%s/feature' % SAVE_BASE_PATH)
