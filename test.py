import pandas as pd
from sys import version_info
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime


# import time
# import keras
# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import MinMaxScaler
#
# from keras.models import Sequential
# from keras.layers import LSTM
# from keras.layers import Dense, Activation, Dropout


def my_date_range(begin, end, time_delta):
    dates = []
    dt = datetime.datetime.strptime(begin, "%Y-%m-%d")
    my_date = begin[:]
    while my_date <= end:
        dates.append(my_date)
        dt = dt + datetime.timedelta(time_delta)
        my_date = dt.strftime("%Y-%m-%d")
    return dates


if version_info.major != 3:
    raise Exception('use python 3')

data_dir = "D:\\qqfile\\data\\"
# data_dir = "H:\\data\\"

os.chdir(data_dir)
file_chdir = os.getcwd()
file_list0 = []
file_list1 = []
file_list2 = []
# root D:/qqfile/data/2012/0/2012-05-28/
date_range = my_date_range('2012-01-01', '2012-12-31', 10)
# print(date_range)
# current_date_str = "2012-01-01"
# current_date = datetime.datetime.strptime(current_date_str, '%Y-%m-%d')
for root, dirs, files in os.walk(file_chdir):
    for name in files:
        path = os.path.dirname(root)
        # if path == data_dir + "2014\\0":
        for d in date_range:
            if root == data_dir + "2012\\0\\" + d:
                # if path == data_dir + "2012\\0":
                file_list0.append(os.path.join(root, name))
            # elif path == data_dir + "2012\\1":
            #     file_list1.append(os.path.join(root, name))
            # elif path == data_dir + "2012\\2":
            #     file_list2.append(os.path.join(root, name))
            else:
                continue

df = pd.DataFrame()
for file in file_list0:
    df = df.append(pd.read_table(file, header=None, encoding='gb2312',
                                 sep='\\]\\[|\\[|\\]', engine='python'))
# df[45] = df[45].fillna(0)
# for file in file_list1:
#     df = df.append(pd.read_table(file, header=None, encoding='gb2312',
#                                  sep='\\]\\[|\\[|\\]', engine='python'))
# df[45] = df[45].fillna(1)
# for file in file_list2:
#     df = df.append(pd.read_table(file, header=None, encoding='gb2312',
#                                  sep='\\]\\[|\\[|\\]', engine='python'))
# df[45] = df[45].fillna(2)
df.drop(0, axis=1, inplace=True)
df.drop(45, axis=1, inplace=True)
# print(df.corr())

# data = data.drop(data[(data[1] > "2012-05-29")].index)
# data = data.sort_index(axis=0, ascending=False)
df = df.sort_values(1, 'index')
# date_range = pd.date_range('2013-12-28', '2014-12-31')
# result = []
# for d in date_range:
#     result.append(0)
# for date in date_range:
#     # print(date - datetime.timedelta(days=1))
#     total = 0
#     for row in df.itertuples():
#         if str(date) < row[1] < str(date + datetime.timedelta(days=1)):
#             total += row[2]
#         else:
#             result.append(total)
#             break

# i = 0
# j = 0
# total = 0
# for row in df.itertuples():
#     date_now = date_range[i]
#     if row[1] < str(date_now) or row[1] > str(date_now + datetime.timedelta(days=1)):
#         if j != 0:
#             result[i] = total / j
#         else:
#             result[i] = total
#         i = i + 1
#         if total != 0:
#             total = 0
#             j = 0
#             total += row[2]
#             j += 1
#     else:
#         total += row[2]
#         j += 1
#         result[i] = total / j

# df = df.loc[(df[1] < "2012-05-29") & (df[1] > "2012-05-28")]
# display(df)


# x = range(len(result))
# # # print x, print and check what is x
# y = result
# coef1 = np.polyfit(x, y, 3)
# ploy_fit1 = np.poly1d(coef1)
# plt.plot(x, ploy_fit1(x), 'g', label="1")
# # print y
# # plt.plot(x, y)  # plotting x and y
# print(ploy_fit1)
# plt.scatter(x, y, s=1, color='black')
# plt.show()
date = []
total = []
result = []
df_result = pd.DataFrame()
current_date = ""
i = 0
j = 1
temp_df = pd.DataFrame()
for row_index, row in df.iterrows():
    if temp_df.empty:
        date.append(row[1][0:10])
        row.drop(labels=1, inplace=True)
        temp_df = temp_df.append(row, ignore_index=True)
        # temp_df.iloc[0:1, 0:1] = row[1][0:10]

    else:
        if row[1][0:10] != date[-1]:
            temp_row = temp_df.mean().round(2)
            s = pd.Series([date[-1], 0], index=[1, 45])
            temp_row = temp_row.append(s)
            temp_row = temp_row.sort_index(axis=0)
            df_result = df_result.append(temp_row, ignore_index=True)
            temp_df = pd.DataFrame()
            # df_result = df_result.append(row, ignore_index=True)
            # df_result.iloc[i:i + 1, 0:1] = date[-1]
            i += 1
            date.append(row[1][0:10])
        else:
            row.drop(labels=1, inplace=True)
            # df_result.iloc[i:i + 1, 1:45] += row
            temp_df = temp_df.append(row, ignore_index=True)

    # if len(date) == 0:
    #     date.append(row[1][0:10])
    # if row[1][0:10] != date[-1]:
    #     date.append(row[1][0:10])
    #     i += 1
    # else:
    #     # row.drop(labels=1, inplace=True)
    #     df_result = df_result.append(row, ignore_index=True)
    #     df_result.iloc[i:i + 1, 0:1] = row[1][0:10]
    # if df_result.empty:
    #     row[1] = date[-1]
    #
    #     df_result = df_result.append(row, ignore_index=True)
    # else:
    #     df_result.iloc[i:i + 1, :] += row

    # if i == 1:
    #     break

print(df_result)
