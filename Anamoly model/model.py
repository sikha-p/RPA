from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from collections import deque
import pandas as pd
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

app = Flask(__name__)

# Load your trained model
model = tf.keras.models.load_model(r'C:\Users\syed.hasnain\Downloads\WordToVector\sequential_9.h5')

# Core metrics
METRICS = ['cpu_usage', 'memory_usage', 'response_time', 'error_rate', 'request_count']

# Default threshold
ANOMALY_THRESHOLD = 0.5

# Storage for historical data (needed for feature creation)
historical_data = pd.DataFrame(columns=METRICS + ['anomaly_flag'])

# Define your create_features function here
def create_features(df, window_size=6):
    """Create rolling window features"""
    features = df.copy()

    # Create rolling window statistics
    for metric in METRICS:
        features[f'{metric}_rolling_mean'] = df[metric].rolling(window=window_size).mean()
        features[f'{metric}_rolling_std'] = df[metric].rolling(window=window_size).std()
        features[f'{metric}_rolling_min'] = df[metric].rolling(window=window_size).min()
        features[f'{metric}_rolling_max'] = df[metric].rolling(window=window_size).max()

        # Calculate the difference instead of percentage for more stability
        features[f'{metric}_change'] = df[metric].diff(periods=window_size)

        # Calculate percentage change with clipping to reasonable bounds
        pct_change = df[metric].pct_change(periods=window_size)
        features[f'{metric}_rate_of_change'] = pct_change.clip(-10, 10).fillna(0)

    # Drop NaN values
    features.dropna(inplace=True)

    return features

@app.route('/predict', methods=['POST'])
def predict():
    global historical_data

    # Get data from request
    data = request.json

    # Extract the metrics
    if 'input' in data:
        metrics_values = data['input'][0]  # Assuming first element of input array
    else:
        metrics_values = [data.get(metric, 0) for metric in METRICS]

    # Create a new row with current metrics (assuming anomaly_flag=0 initially)
    new_row = pd.DataFrame([metrics_values + [0]], columns=METRICS + ['anomaly_flag'])

    # Append to historical data
    historical_data = pd.concat([historical_data, new_row], ignore_index=True)

    # Keep only necessary history (depending on your feature engineering requirements)
    # Adjust the number based on how much history your create_features function needs
    if len(historical_data) > 100:  # Example: keep last 100 records
        historical_data = historical_data.tail(100)

    # Create features using your function
    features_df = create_features(historical_data)

    # Get the latest feature set (the one we just added)
    latest_features = features_df.iloc[-1:].drop('anomaly_flag', axis=1).values

    # Create input in the shape expected by the model (assuming time window = 24)
    window_size = 24
    if len(features_df) >= window_size:
        # If we have enough history, use the window
        input_window = features_df.tail(window_size).drop('anomaly_flag', axis=1).values
        input_data = np.expand_dims(input_window, axis=0)  # Add batch dimension
    else:
        # Not enough history yet, pad with zeros
        pad_size = window_size - len(features_df)
        feature_count = latest_features.shape[1]
        padding = np.zeros((pad_size, feature_count))
        available_features = features_df.drop('anomaly_flag', axis=1).values
        input_window = np.vstack((padding, available_features))
        input_data = np.expand_dims(input_window, axis=0)  # Add batch dimension

    # Make prediction
    prediction = model.predict(input_data)

    # Get the raw prediction score
    raw_score = float(prediction[0][0])  # Adjust based on your model's output format

    # Update the historical data with the prediction (if needed for future feature engineering)
    historical_data.iloc[-1, -1] = int(raw_score > ANOMALY_THRESHOLD)

    return jsonify({
        'prediction_score': raw_score,
        'is_anomaly': bool(raw_score > ANOMALY_THRESHOLD),
        'input_metrics': {metric: float(val) for metric, val in zip(METRICS, metrics_values)}
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)