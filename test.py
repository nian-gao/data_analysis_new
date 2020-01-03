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

if version_info.major != 3:
    raise Exception('use python 3')

data_dir = "D:\\qqfile\\data\\"
# data_dir =

os.chdir(data_dir)
file_chdir = os.getcwd()
file_list = []
# root D:/qqfile/data/2012/0/2012-05-28/
for root, dirs, files in os.walk(file_chdir):
    for name in files:
        path = os.path.dirname(root)
        if path == data_dir + "2014\\0":
            # if root == data_dir + "2012\\0\\2012-05-28":
            file_list.append(os.path.join(root, name))
        # if root == data_dir + "2012\\0\\2012-05-28":
        #     file_list.append(os.path.join(root, name))
        # elif root == data_dir + "2012\\1\\2012-05-28":
        #     file_list.append(os.path.join(root, name))
        # elif root == data_dir + "2012\\2\\2012-05-28":
        #     file_list.append(os.path.join(root, name))
        else:
            continue

df = pd.DataFrame()
for file in file_list:
    df = df.append(pd.read_table(file, header=None, encoding='gb2312',
                                 sep='\\]\\[|\\[|\\]', engine='python'))

df.drop(0, axis=1, inplace=True)
df.drop(45, axis=1, inplace=True)

# data = data.drop(data[(data[1] > "2012-05-29")].index)
# data = data.sort_index(axis=0, ascending=False)
df = df.sort_values(1, 'index')
date_range = pd.date_range('2013-12-28', '2014-12-31')
result = []
for d in date_range:
    result.append(0)
# for date in date_range:
#     # print(date - datetime.timedelta(days=1))
#     total = 0
#     for row in df.itertuples():
#         if str(date) < row[1] < str(date + datetime.timedelta(days=1)):
#             total += row[2]
#         else:
#             result.append(total)
#             break

i = 0
j = 0
total = 0
for row in df.itertuples():
    date_now = date_range[i]
    if row[1] < str(date_now) or row[1] > str(date_now + datetime.timedelta(days=1)):
        if j != 0:
            result[i] = total / j
        else:
            result[i] = total
        i = i + 1
        if total != 0:
            total = 0
            j = 0
            total += row[2]
            j += 1
    else:
        total += row[2]
        j += 1
        result[i] = total / j

# df = df.loc[(df[1] < "2012-05-29") & (df[1] > "2012-05-28")]
# display(df)


x = range(len(result))
# # print x, print and check what is x
y = result
coef1 = np.polyfit(x, y, 3)
ploy_fit1 = np.poly1d(coef1)
plt.plot(x, ploy_fit1(x), 'g', label="1")
# print y
# plt.plot(x, y)  # plotting x and y
print(ploy_fit1)
plt.scatter(x, y, s=1, color='black')
plt.show()
