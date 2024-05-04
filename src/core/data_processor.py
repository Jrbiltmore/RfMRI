
# /RfMRI/src/core/data_processor.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import logging

class DataProcessor:
    """Class to handle preprocessing of MRI data."""
    
    def __init__(self, data):
        """
        Initialize the DataProcessor with data.
        
        Parameters:
            data (dict): Raw data to be processed.
        """
        self.data = pd.DataFrame(data)
        self.logger = logging.getLogger('rfmri_application.data_processor')

    def preprocess(self):
        """
        Preprocess the data by cleaning, normalizing, and transforming it.
        
        Returns:
            DataFrame: The preprocessed data.
        """
        self.logger.info("Starting data preprocessing")
        self._handle_missing_values()
        self._normalize_data()
        self._transform_data()
        self.logger.info("Data preprocessing completed")
        return self.data

    def _handle_missing_values(self):
        """Fill missing values in the dataset."""
        self.logger.debug("Handling missing values")
        # Example: Fill missing values with the median
        for column in self.data.columns:
            if self.data[column].isnull().any():
                median = self.data[column].median()
                self.data[column].fillna(median, inplace=True)
                self.logger.debug(f"Filled missing values in {column} with median value {median}")

    def _normalize_data(self):
        """Normalize data to have a mean of 0 and a standard deviation of 1."""
        self.logger.debug("Normalizing data")
        scaler = StandardScaler()
        self.data = pd.DataFrame(scaler.fit_transform(self.data), columns=self.data.columns)

    def _transform_data(self):
        """Apply any additional transformations required on the data."""
        self.logger.debug("Transforming data")
        # Example: Log transform to reduce skewness in data
        for column in self.data.columns:
            self.data[column] = np.log1p(self.data[column])
