import pandas as pd
from sys import version_info
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import time

# import keras

# from sklearn.preprocessing import MinMaxScaler
#
# from keras.models import Sequential
# from keras.layers import LSTM
# from keras.layers import Dense, Activation, Dropout
data_dir = "D:\\qqfile\\data\\"
# data_dir = "H:\\data\\"

if version_info.major != 3:
    raise Exception('use python 3')

print('start', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def init_data_frame(data_frame, file_list):
    for f in file_list:
        data_frame = data_frame.append(pd.read_table(f, header=None, encoding='gb2312',
                                                     sep='\\]\\[|\\[|\\]', engine='python'))
    data_frame.drop(0, axis=1, inplace=True)
    data_frame.drop(45, axis=1, inplace=True)
    data_frame = data_frame.sort_values(1, 'index')
    return data_frame.reset_index(drop=True)


def my_date_range(begin, end, time_delta=1):
    dates = []
    dt = datetime.datetime.strptime(begin, "%Y-%m-%d")
    my_date = begin[:]
    while my_date <= end:
        dates.append(my_date)
        dt = dt + datetime.timedelta(time_delta)
        my_date = dt.strftime("%Y-%m-%d")
    return dates


def add_data_to_result(temp, date_list, res, y_value):
    # row_of_data = temp.mean().round(2)  # avg
    row_of_data = temp.quantile().round(2)  # middle
    inner_s = pd.Series([date_list[-1], y_value], index=[1, 45])
    row_of_data = row_of_data.append(inner_s)
    row_of_data = row_of_data.sort_index(axis=0)
    return res.append(row_of_data, ignore_index=True)


def trans_data(data_frame, file_list, res_df, y_value):
    data_frame = init_data_frame(data_frame, file_list)
    print('data frame inited ' + str(y_value), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    date_list = []
    inner_temp = pd.DataFrame()

    for r_index, r in data_frame.iterrows():
        if inner_temp.empty:
            date_list.append(r[1][0:10])
            r.drop(labels=1, inplace=True)
            inner_temp = inner_temp.append(r, ignore_index=True)
        else:
            if r[1][0:10] != date_list[-1]:
                res_df = add_data_to_result(inner_temp, date_list, res_df, y_value)
                inner_temp = pd.DataFrame()
                date_list.append(r[1][0:10])
            else:
                r.drop(labels=1, inplace=True)
                inner_temp = inner_temp.append(r, ignore_index=True)
                if len(data_frame) - 1 == r_index:
                    res_df = add_data_to_result(inner_temp, date_list, res_df, y_value)
    return res_df


def trans_not_mid(data_frame, file_list, res_df, y_value):
    data_frame = init_data_frame(data_frame, file_list)

    for r_index, r in data_frame.iterrows():
        s = pd.Series([y_value], index=[45])
        r = r.append(s)
        r = r.sort_index(axis=0)
        res_df = res_df.append(r, ignore_index=True)
    return res_df


# get the result data_frame
# cwd current work dir
def get_result_df(cwd, date_range, tag):
    files0 = []
    files1 = []
    files2 = []
    for root, dirs, files in os.walk(cwd):
        for name in files:
            path = os.path.dirname(root)
            # if path == data_dir + "2014\\0":
            for d in date_range:
                if root == data_dir + d.split('-')[0] + "\\0\\" + d:
                    # if path == data_dir + "2012\\0":
                    files0.append(os.path.join(root, name))
                elif root == data_dir + d.split('-')[0] + "\\1\\" + d:
                    files1.append(os.path.join(root, name))
                # elif path == data_dir + "2012\\2":
                elif root == data_dir + d.split('-')[0] + "\\2\\" + d:
                    files2.append(os.path.join(root, name))
                else:
                    continue
    print(tag + 'files read finished time', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    df = pd.DataFrame()
    result_df = pd.DataFrame()
    result_df = trans_data(df, files0, result_df, 0)
    result_df = trans_data(df, files1, result_df, 1)
    result_df = trans_data(df, files2, result_df, 2)
    print(len(df), tag)
    return result_df


os.chdir(data_dir)
file_chdir = os.getcwd()
file_list0 = []
file_list1 = []
file_list2 = []
date_range_train = my_date_range('2012-01-01', '2014-12-31', 10)
train_df = get_result_df(file_chdir, date_range_train)
date_range_test = my_date_range('2015-01-01', '2015-12-31', 10)
test_df = get_result_df(file_chdir, date_range_test)
X_train = train_df.loc[:, range(2, 45)]
y_train = train_df.loc[:, [45]]
X_test = test_df.loc[:, range(2, 45)]
y_test = test_df.loc[:, [45]]
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
lin_reg = LinearRegression()
model = lin_reg.fit(X_train, y_train)
y_pred = lin_reg.predict(X_test)
for i in range(len(y_pred)):
    if y_pred[i][0] < 0:
        y_pred[i][0] = 0
    elif y_pred[i][0] > 2:
        y_pred[i][0] = 2
    else:
        y_pred[i][0] = round(y_pred[i][0])
plt.figure()
plt.plot(range(len(y_pred[0:100])), y_pred[0:100], 'b', label="predict")
plt.plot(range(len(y_pred[0:100])), y_test[0:100], 'r', label="test")
correct_items = 0
total_items = 0
y_test = y_test.reset_index()
print(len(y_pred))
for i in range(len(y_pred)):
    total_items += 1
    if y_pred[i][0] == y_test[45][i]:
        correct_items += 1
rate = correct_items / total_items
print(round(rate, 3))
plt.legend(loc="upper right")
plt.show()
print('finished', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
