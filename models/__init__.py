#!/usr/bin/env python3
"""
Deep Learning Models Module
Contains LSTM, Autoencoder, CNN, and Hybrid models for industrial monitoring
"""

import logging
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
import numpy as np

logger = logging.getLogger(__name__)

class LSTMRNNModel:
    """
    LSTM RNN model for Remaining Useful Life (RUL) prediction
    """
    
    def __init__(self, sequence_length: int = 50, num_features: int = 10):
        self.sequence_length = sequence_length
        self.num_features = num_features
        self.model = None
        logger.info(f"Initialized LSTM Model: seq_len={sequence_length}, features={num_features}")
    
    def build(self, units: int = 128, dropout: float = 0.2):
        """
        Build LSTM model architecture
        
        Args:
            units: Number of LSTM units
            dropout: Dropout rate
        """
        model = keras.Sequential([
            layers.LSTM(units, return_sequences=True, 
                       input_shape=(self.sequence_length, self.num_features)),
            layers.Dropout(dropout),
            layers.LSTM(units//2),
            layers.Dropout(dropout),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(1)  # RUL prediction
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae', 'mape']
        )
        
        self.model = model
        logger.info(f"LSTM model built with {model.count_params()} parameters")
        return model
    
    def train(self, X_train, y_train, epochs: int = 50, batch_size: int = 32,
              validation_split: float = 0.2):
        """
        Train LSTM model
        """
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
        logger.info(f"LSTM training completed. Final loss: {history.history['loss'][-1]:.4f}")
        return history


class AutoencoderModel:
    """
    Autoencoder model for anomaly detection
    """
    
    def __init__(self, input_dim: int = 10, encoding_dim: int = 32):
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim
        self.model = None
        self.encoder = None
        logger.info(f"Initialized Autoencoder: input={input_dim}, encoding={encoding_dim}")
    
    def build(self, layers_config: list = None):
        """
        Build Autoencoder model
        
        Args:
            layers_config: Configuration of hidden layers
        """
        if layers_config is None:
            layers_config = [64, 32]
        
        # Encoder
        encoder_inputs = keras.Input(shape=(self.input_dim,))
        x = encoder_inputs
        
        for units in layers_config:
            x = layers.Dense(units, activation='relu')(x)
        
        encoded = layers.Dense(self.encoding_dim, activation='relu', name='encoding')(x)
        
        self.encoder = Model(encoder_inputs, encoded, name='encoder')
        
        # Decoder
        decoder_inputs = keras.Input(shape=(self.encoding_dim,))
        x = decoder_inputs
        
        for units in reversed(layers_config):
            x = layers.Dense(units, activation='relu')(x)
        
        decoded = layers.Dense(self.input_dim, activation='sigmoid')(x)
        
        # Autoencoder
        self.model = Model(encoder_inputs, decoded, name='autoencoder')
        self.model.compile(optimizer='adam', loss='mse')
        
        logger.info(f"Autoencoder built with {self.model.count_params()} parameters")
        return self.model
    
    def train(self, X_train, epochs: int = 100, batch_size: int = 32):
        """
        Train Autoencoder
        """
        history = self.model.fit(
            X_train, X_train,
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )
        logger.info(f"Autoencoder training completed")
        return history
    
    def detect_anomalies(self, X_test, threshold: float = None):
        """
        Detect anomalies using reconstruction error
        """
        predictions = self.model.predict(X_test)
        mse = np.mean(np.power(X_test - predictions, 2), axis=1)
        
        if threshold is None:
            threshold = np.mean(mse) + 2 * np.std(mse)
        
        anomalies = mse > threshold
        logger.info(f"Detected {np.sum(anomalies)} anomalies")
        
        return anomalies, mse


class CNNDetectorModel:
    """
    CNN model for fault pattern detection
    """
    
    def __init__(self, input_shape: tuple = (100,), num_classes: int = 10):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = None
        logger.info(f"Initialized CNN Detector: shape={input_shape}, classes={num_classes}")
    
    def build(self, filters: int = 64, kernel_size: int = 3):
        """
        Build CNN model
        """
        model = keras.Sequential([
            layers.Input(shape=self.input_shape),
            layers.Conv1D(filters, kernel_size, activation='relu'),
            layers.MaxPooling1D(2),
            layers.Conv1D(filters*2, kernel_size, activation='relu'),
            layers.MaxPooling1D(2),
            layers.GlobalAveragePooling1D(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        logger.info(f"CNN model built with {model.count_params()} parameters")
        return model


if __name__ == '__main__':
    logger.info("Models module ready for import")
