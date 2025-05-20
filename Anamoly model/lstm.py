#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install xgboost


# In[2]:


# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, precision_score, recall_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Bidirectional
from sklearn.ensemble import RandomForestClassifier, IsolationForest
import xgboost as xgb
from sklearn.svm import OneClassSVM
import warnings
warnings.filterwarnings('ignore')


# In[3]:


# Assuming you've created the dataset from the previous code
df = pd.read_csv(r'C:\Users\syed.hasnain\Downloads\WordToVector\system_logs_with_anomalies1.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set timestamp as index
df.set_index('timestamp', inplace=True)

# EDA - Explore the dataset
print("Dataset shape:", df.shape)
print("\nDataset information:")
print(df.info())
print("\nSummary statistics:")
print(df.describe())

# Check anomaly distribution
print("\nAnomaly flag distribution:")
print(df['anomaly_flag'].value_counts())


# In[4]:


# Visualize the data
plt.figure(figsize=(15, 12))

# Plot each metric
metrics = ['cpu_usage', 'memory_usage', 'response_time', 'error_rate', 'request_count']
for i, metric in enumerate(metrics):
    plt.subplot(len(metrics), 1, i+1)
    plt.plot(df.index, df[metric], label=metric)

    # Highlight precursors and anomalies
    plt.scatter(df[df['anomaly_flag']==1].index, df[df['anomaly_flag']==1][metric], 
                color='orange', label='Precursor', alpha=0.5, s=10)
    plt.scatter(df[df['anomaly_flag']==2].index, df[df['anomaly_flag']==2][metric], 
                color='red', label='Anomaly', alpha=0.7, s=20)

    if i == 0:
        plt.legend()
    plt.title(f'{metric} Over Time')

plt.tight_layout()
plt.savefig('metrics_visualization.png')
plt.show()


# In[39]:


# Approach 1: Time-series Forecasting with LSTM
# ----------------------------------------

# Feature Engineering
def create_features(df, window_size=6):
    """Create rolling window features"""
    features = df.copy()

    # Create rolling window statistics
    for metric in metrics:
        features[f'{metric}_rolling_mean'] = df[metric].rolling(window=window_size).mean()
        features[f'{metric}_rolling_std'] = df[metric].rolling(window=window_size).std()
        features[f'{metric}_rolling_min'] = df[metric].rolling(window=window_size).min()
        features[f'{metric}_rolling_max'] = df[metric].rolling(window=window_size).max()

    features[f'{metric}_rate_of_change'] = df[metric].pct_change(periods=window_size)

    # With this approach instead:
    for metric in metrics:
        # Calculate the difference instead of percentage for more stability
        features[f'{metric}_change'] = df[metric].diff(periods=window_size)

        # If you still want percentage change, clip it to reasonable bounds
        pct_change = df[metric].pct_change(periods=window_size)
        features[f'{metric}_rate_of_change'] = pct_change.clip(-10, 10).fillna(0)
    # Drop NaN values
    features.dropna(inplace=True)

    return features



# In[40]:


# Create features
features_df = create_features(df[metrics + ['anomaly_flag']])

# Split data
X = features_df.drop('anomaly_flag', axis=1)
y = features_df['anomaly_flag']

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Convert y to binary (0: normal, 1: precursor or anomaly)
y_binary = (y > 0).astype(int)




# In[41]:


# Create sequences for LSTM
def create_sequences(X, y, time_steps=5):
    X_seq, y_seq = [], []
    for i in range(len(X) - time_steps):
        # X_seq.append(X[i:i + time_steps])
        # y_seq.append(y[i + time_steps])
        X_seq.append(X[i:i + time_steps])
        y_seq.append(1 if y[i:i + time_steps].any() else 0)
    return np.array(X_seq), np.array(y_seq)

# Create sequences
time_steps = 24  # 2 hours of data (with 5-min intervals)
X_seq, y_seq = create_sequences(X_scaled, y_binary, time_steps)

# Split data into train and test
# Use time-based split instead of random split since it's time series data
split_idx = int(len(X_seq) * 0.8)
X_train, X_test = X_seq[:split_idx], X_seq[split_idx:]
y_train, y_test = y_seq[:split_idx], y_seq[split_idx:]



# In[45]:


# LSTM Model for Anomaly Prediction
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(Bidirectional(LSTM(32, return_sequences=True), input_shape=input_shape))
    model.add(Dropout(0.5))
    model.add(Bidirectional(LSTM(32)))
    model.add(Dense(32, activation='relu')) 
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model
# Build and train LSTM model
lstm_model = build_lstm_model((X_train.shape[1], X_train.shape[2]))
print("\nLSTM Model Summary:")
lstm_model.summary()
# Class weights to handle imbalanced data
class_weights = {0: 1, 1: y_binary.value_counts()[0] / y_binary.value_counts()[1]}
print(f"\nClass weights: {class_weights}")
from keras.callbacks import EarlyStopping
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=8,
    restore_best_weights=True
)
from keras.callbacks import ReduceLROnPlateau
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.1,
    patience=2,
    min_lr=1e-6
)
# Train the model with learning rate scheduler
lstm_history = lstm_model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=16,
    validation_data=(X_test, y_test),
    class_weight=class_weights,
    callbacks=[early_stop, reduce_lr],  # Added learning rate scheduler
    verbose=1
)


# In[46]:


# Plot training history
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(lstm_history.history['loss'], label='Training Loss')
plt.plot(lstm_history.history['val_loss'], label='Validation Loss')
plt.title('LSTM Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(lstm_history.history['accuracy'], label='Training Accuracy')
plt.plot(lstm_history.history['val_accuracy'], label='Validation Accuracy')
plt.title('LSTM Accuracy')
plt.legend()

plt.tight_layout()
plt.savefig('lstm_training_history.png')
plt.show()


# In[47]:


# Evaluate the model
score = lstm_model.evaluate(X_test, y_test, verbose=0)
print(f'Test Loss: {score[0]}, Test Accuracy: {score[1]}')

# Evaluate LSTM model
y_pred_proba = lstm_model.predict(X_test)
y_pred = (y_pred_proba > 0.5).astype(int)

print("\nLSTM Model Evaluation:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix - LSTM')
plt.savefig('lstm_confusion_matrix.png')
plt.show()


# In[48]:


lstm_model.save(r'C:\Users\syed.hasnain\Downloads\WordToVector\sequential_9.h5')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




