#!/usr/bin/env python3
"""
Data Loader Module
Handles loading, preprocessing, and validation of industrial sensor data
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, List, Optional

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Loads and preprocesses industrial sensor data for model training and inference
    """
    
    def __init__(self, data_dir: str = 'data/raw'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"DataLoader initialized with directory: {self.data_dir}")
    
    def load_csv(self, filename: str) -> pd.DataFrame:
        """
        Load CSV file containing sensor data
        
        Args:
            filename: Name of CSV file
            
        Returns:
            DataFrame with sensor data
        """
        filepath = self.data_dir / filename
        logger.info(f"Loading data from {filepath}")
        
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
    
    def preprocess(self, df: pd.DataFrame, 
                   handle_missing: str = 'mean',
                   normalize: bool = True) -> pd.DataFrame:
        """
        Preprocess sensor data
        
        Args:
            df: Input DataFrame
            handle_missing: Strategy for missing values ('mean', 'forward_fill', 'drop')
            normalize: Whether to normalize numerical columns
            
        Returns:
            Preprocessed DataFrame
        """
        logger.info("Starting data preprocessing")
        
        # Handle missing values
        if handle_missing == 'mean':
            df = df.fillna(df.mean(numeric_only=True))
        elif handle_missing == 'forward_fill':
            df = df.fillna(method='ffill').fillna(method='bfill')
        elif handle_missing == 'drop':
            df = df.dropna()
        
        logger.info(f"Missing values handled using: {handle_missing}")
        
        # Normalize numerical columns
        if normalize:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
            logger.info(f"Normalized {len(numeric_cols)} numerical columns")
        
        return df
    
    def split_train_test(self, df: pd.DataFrame, 
                        test_size: float = 0.2,
                        shuffle: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split data into training and testing sets
        
        Args:
            df: Input DataFrame
            test_size: Fraction of data for testing
            shuffle: Whether to shuffle before splitting
            
        Returns:
            Tuple of (train_df, test_df)
        """
        if shuffle:
            df = df.sample(frac=1).reset_index(drop=True)
        
        split_idx = int(len(df) * (1 - test_size))
        train_df = df[:split_idx]
        test_df = df[split_idx:]
        
        logger.info(f"Split data: {len(train_df)} training, {len(test_df)} testing")
        return train_df, test_df
    
    def create_sequences(self, data: np.ndarray, 
                        sequence_length: int = 50) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences for time-series models
        
        Args:
            data: Input array
            sequence_length: Length of sequences
            
        Returns:
            Tuple of (X, y) sequences
        """
        X, y = [], []
        
        for i in range(len(data) - sequence_length):
            X.append(data[i:i+sequence_length])
            y.append(data[i+sequence_length])
        
        logger.info(f"Created {len(X)} sequences of length {sequence_length}")
        return np.array(X), np.array(y)


if __name__ == '__main__':
    # Example usage
    loader = DataLoader()
    logger.info("DataLoader module ready for import")
