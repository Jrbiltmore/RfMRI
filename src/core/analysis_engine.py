
# /RfMRI/src/core/analysis_engine.py

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import logging

class AnalysisEngine:
    """Class responsible for performing the analysis on MRI data."""

    def __init__(self, data):
        """
        Initialize the AnalysisEngine with preprocessed data.
        
        Parameters:
            data (DataFrame): The preprocessed data ready for analysis.
        """
        self.data = data
        self.features = data.drop('target', axis=1)
        self.target = data['target']
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.logger = logging.getLogger('rfmri_application.analysis_engine')

    def train_model(self):
        """Train the machine learning model on the provided data."""
        self.logger.info("Training model")
        self.model.fit(self.features, self.target)
        self.logger.info("Model training completed")

    def predict(self):
        """Make predictions using the trained model."""
        self.logger.info("Making predictions")
        predictions = self.model.predict(self.features)
        return predictions

    def evaluate_model(self):
        """Evaluate the model's performance."""
        self.logger.info("Evaluating model")
        predictions = self.predict()
        report = classification_report(self.target, predictions)
        accuracy = accuracy_score(self.target, predictions)
        self.logger.info(f"Model evaluation completed with accuracy: {accuracy}")
        return report, accuracy

    def analyze(self):
        """Run the full analysis pipeline: train, predict, and evaluate."""
        self.train_model()
        report, accuracy = self.evaluate_model()
        return {
            'classification_report': report,
            'accuracy': accuracy
        }
    