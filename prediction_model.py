from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, TensorDataset
import yfinance as yf
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

#Historical sp500 data
df_sp500 = yf.download("^GSPC", start= "2023-01-01", end= "2023-08-04")

#calculate and add 5 day SMA/volume to dataframe. Remove NaN data
window_size = 5
df_sp500["5 Day SMA"] = df_sp500['Close'].rolling(window=window_size).mean()
df_sp500["5 Day Average Volume"] = df_sp500['Volume'].rolling(window=window_size).mean()
df_sp500.dropna(inplace=True)

#scale the data
scaler = MinMaxScaler()
df_sp500[['Open', '5 Day Average Volume', '5 Day SMA', 'Close']] = scaler.fit_transform(df_sp500[['Open', '5 Day Average Volume', '5 Day SMA', 'Close']])

#split into input and output for tensor creation
input_data = df_sp500[['Open', '5 Day Average Volume', '5 Day SMA']]
output_data = df_sp500[['Close']]

#create 70% train size then the test size
train_size = int(.7 * len(input_data))

train_input = input_data[:train_size]
train_target = output_data[:train_size]
test_input = input_data[train_size:]
test_target = output_data[train_size:]

#Convert to tensors
train_input_tensor = torch.tensor(train_input.values, dtype=torch.float32)
train_target_tensor = torch.tensor(train_target.values, dtype=torch.float32)
test_input_tensor = torch.tensor(test_input.values, dtype=torch.float32)
test_target_tensor = torch.tensor(test_target.values, dtype=torch.float32)

print(train_input_tensor.shape)
print(train_target_tensor.shape)
print(test_input_tensor.shape)
print(test_target_tensor.shape)

