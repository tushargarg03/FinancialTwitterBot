import yfinance as yf
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Rest of the code remains the same...


# Set a random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Function to download stock data from Yahoo Finance
def download_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to create the dataset for training the RNN
def create_dataset(data, look_back=1):
    X, Y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back)])
        Y.append(data[i + look_back])
    return np.array(X), np.array(Y)

# Set the ticker symbol of the stock you want to predict
ticker = "AAPL"

# Download historical stock data from Yahoo Finance
start_date = "2020-01-01"
end_date = "2023-01-01"
data = download_stock_data(ticker, start_date, end_date)

# Extract the "Close" price for prediction
close_prices = data['Close'].values.reshape(-1, 1)

# Normalize the data using MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
close_prices_normalized = scaler.fit_transform(close_prices)

# Split data into training and test sets (80-20 split)
train_size = int(len(close_prices_normalized) * 0.8)
test_size = len(close_prices_normalized) - train_size
train_data, test_data = close_prices_normalized[:train_size, :], close_prices_normalized[train_size:, :]

# Create the dataset for training the RNN
look_back = 10  # Number of previous time steps to use for prediction
X_train, y_train = create_dataset(train_data, look_back)
X_test, y_test = create_dataset(test_data, look_back)

# Reshape input data to fit the LSTM layer (samples, time steps, features)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Build the RNN model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(look_back, 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the RNN model
model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)

# Evaluate the model on the test data
loss = model.evaluate(X_test, y_test, verbose=0)
print(f"Test loss: {loss}")

# Make predictions on the test data
y_pred = model.predict(X_test)

# Inverse transform the normalized predictions and ground truth data to get actual stock prices
y_pred_actual = scaler.inverse_transform(y_pred)
y_test_actual = scaler.inverse_transform(y_test)

# Calculate the Root Mean Squared Error (RMSE)
rmse = np.sqrt(np.mean((y_pred_actual - y_test_actual) ** 2))
print(f"Root Mean Squared Error (RMSE): {rmse}")

# Download historical stock data from Yahoo Finance for the entire period
data_all = download_stock_data(ticker, start_date, end_date)
dates_all = data_all.index

# Extract dates corresponding to the test dataset
dates_test = dates_all[train_size + look_back:]

# Visualize the predictions vs actual stock prices
plt.figure(figsize=(12, 6))
plt.plot(dates_test, y_test_actual, label='Actual Prices', color='b')
plt.plot(dates_test, y_pred_actual, label='Predicted Prices', color='r')
plt.title(f"Stock Price Prediction vs Actual (RMSE: {rmse:.2f})")
plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()