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

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def my_date_range(begin, end, time_delta):
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
    for f in file_list:
        data_frame = data_frame.append(pd.read_table(f, header=None, encoding='gb2312',
                                                     sep='\\]\\[|\\[|\\]', engine='python'))

    data_frame.drop(0, axis=1, inplace=True)
    data_frame.drop(45, axis=1, inplace=True)
    data_frame = data_frame.sort_values(1, 'index')
    data_frame = data_frame.reset_index(drop=True)
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


os.chdir(data_dir)
file_chdir = os.getcwd()
file_list0 = []
file_list1 = []
file_list2 = []
date_range = my_date_range('2012-01-01', '2012-06-30', 10)
for root, dirs, files in os.walk(file_chdir):
    for name in files:
        path = os.path.dirname(root)
        # if path == data_dir + "2014\\0":
        for d in date_range:
            if root == data_dir + "2012\\0\\" + d:
                # if path == data_dir + "2012\\0":
                file_list0.append(os.path.join(root, name))
            elif root == data_dir + "2012\\1\\" + d:
                file_list1.append(os.path.join(root, name))
            # elif path == data_dir + "2012\\2":
            elif root == data_dir + "2012\\2\\" + d:
                file_list2.append(os.path.join(root, name))
            else:
                continue

df = pd.DataFrame()
result_df = pd.DataFrame()
result_df = trans_data(df, file_list0, result_df, 0)
result_df = trans_data(df, file_list1, result_df, 1)
result_df = trans_data(df, file_list2, result_df, 2)
# print(result_df)
X = result_df.loc[:, range(2, 45)]
y = result_df.loc[:, [45]]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
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
print(y_pred)
plt.plot(range(len(y_pred[0:130])), y_pred[0:130], 'b', label="predict")
plt.plot(range(len(y_pred[0:130])), y_test[0:130], 'r', label="test")
correct_items = 0
total_items = 0
y_test = y_test.reset_index()

for i in range(len(y_pred)):
    total_items += 1
    if y_pred[i][0] == y_test[45][i]:
        correct_items += 1
rate = correct_items / total_items
print(round(rate, 3))
plt.legend(loc="upper right")
plt.show()
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
