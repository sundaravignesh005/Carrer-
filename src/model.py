"""
Machine Learning Model Module for Career Recommendation System

This module handles model training, prediction, and persistence for career recommendations.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import logging
from typing import Dict, List, Tuple, Any, Optional
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CareerRecommendationModel:
    """
    Handles machine learning model training and prediction for career recommendations.
    """
    
    def __init__(self, model_type: str = 'random_forest'):
        """
        Initialize the career recommendation model.
        
        Args:
            model_type (str): Type of model to use ('decision_tree', 'random_forest', 'gradient_boosting')
        """
        self.model_type = model_type
        self.model = None
        self.label_encoder = LabelEncoder()
        self.feature_columns = []
        self.model_path = 'models/career_model.pkl'
        self.metadata_path = 'models/model_metadata.json'
        
        # Model configurations
        self.model_configs = {
            'decision_tree': {
                'class': DecisionTreeClassifier,
                'params': {
                    'max_depth': 10,
                    'min_samples_split': 5,
                    'min_samples_leaf': 2,
                    'random_state': 42
                }
            },
            'random_forest': {
                'class': RandomForestClassifier,
                'params': {
                    'n_estimators': 100,
                    'max_depth': 10,
                    'min_samples_split': 5,
                    'min_samples_leaf': 2,
                    'random_state': 42
                }
            },
            'gradient_boosting': {
                'class': GradientBoostingClassifier,
                'params': {
                    'n_estimators': 100,
                    'learning_rate': 0.1,
                    'max_depth': 6,
                    'random_state': 42
                }
            }
        }
    
    def create_model(self) -> Any:
        """
        Create a new model instance based on the model type.
        
        Returns:
            Any: Model instance
        """
        if self.model_type not in self.model_configs:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        config = self.model_configs[self.model_type]
        return config['class'](**config['params'])
    
    def train(self, X: pd.DataFrame, y: pd.Series, feature_columns: List[str]) -> Dict[str, Any]:
        """
        Train the career recommendation model.
        
        Args:
            X (pd.DataFrame): Feature matrix
            y (pd.Series): Target labels
            feature_columns (List[str]): List of feature column names
            
        Returns:
            Dict[str, Any]: Training results and metrics
        """
        logger.info(f"Training {self.model_type} model...")
        
        # Store feature columns
        self.feature_columns = feature_columns
        
        # Encode target labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Create and train model
        self.model = self.create_model()
        self.model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        cv_scores = cross_val_score(self.model, X, y_encoded, cv=5)
        
        # Get feature importance
        feature_importance = {}
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = dict(zip(feature_columns, self.model.feature_importances_))
        
        # Prepare results
        results = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_importance': feature_importance,
            'classification_report': classification_report(y_test, y_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        logger.info(f"Model training completed. Accuracy: {accuracy:.4f}")
        logger.info(f"Cross-validation score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        return results
    
    def predict(self, X: np.ndarray) -> Tuple[str, float]:
        """
        Make career prediction for given features.
        
        Args:
            X (np.ndarray): Feature vector
            
        Returns:
            Tuple[str, float]: Predicted career and confidence score
        """
        if self.model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Make prediction
        prediction_encoded = self.model.predict(X)
        prediction = self.label_encoder.inverse_transform(prediction_encoded)[0]
        
        # Get prediction probability
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(X)[0]
            confidence = float(np.max(probabilities))
        else:
            confidence = 1.0
        
        return prediction, confidence
    
    def predict_multiple(self, X: np.ndarray, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Get top-k career predictions with confidence scores.
        
        Args:
            X (np.ndarray): Feature vector
            top_k (int): Number of top predictions to return
            
        Returns:
            List[Tuple[str, float]]: List of (career, confidence) tuples
        """
        if self.model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        if not hasattr(self.model, 'predict_proba'):
            # If model doesn't support probabilities, return single prediction
            prediction, confidence = self.predict(X)
            return [(prediction, confidence)]
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(X)[0]
        
        # Get top-k indices
        top_indices = np.argsort(probabilities)[-top_k:][::-1]
        
        # Get corresponding careers and confidences
        careers = self.label_encoder.inverse_transform(top_indices)
        confidences = probabilities[top_indices]
        
        return list(zip(careers, confidences))
    
    def get_feature_importance(self, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Get top-n most important features.
        
        Args:
            top_n (int): Number of top features to return
            
        Returns:
            List[Tuple[str, float]]: List of (feature, importance) tuples
        """
        if self.model is None or not hasattr(self.model, 'feature_importances_'):
            return []
        
        # Get feature importance
        importance_scores = self.model.feature_importances_
        
        # Create feature-importance pairs and sort
        feature_importance = list(zip(self.feature_columns, importance_scores))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        return feature_importance[:top_n]
    
    def save_model(self) -> None:
        """
        Save the trained model and metadata.
        """
        if self.model is None:
            raise ValueError("No model to save. Please train the model first.")
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Save model
        joblib.dump(self.model, self.model_path)
        
        # Save metadata
        metadata = {
            'model_type': self.model_type,
            'feature_columns': self.feature_columns,
            'label_encoder_classes': self.label_encoder.classes_.tolist(),
            'model_config': {
                'class_name': self.model_configs[self.model_type]['class'].__name__,
                'params': self.model_configs[self.model_type]['params']
            }
        }
        
        with open(self.metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Model saved to {self.model_path}")
        logger.info(f"Metadata saved to {self.metadata_path}")
    
    def load_model(self) -> bool:
        """
        Load a previously trained model.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.model_path):
                logger.warning(f"Model file not found: {self.model_path}")
                return False
            
            # Load model
            self.model = joblib.load(self.model_path)
            
            # Load metadata
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                self.model_type = metadata.get('model_type', self.model_type)
                self.feature_columns = metadata.get('feature_columns', [])
                
                # Recreate label encoder
                classes = metadata.get('label_encoder_classes', [])
                if classes:
                    self.label_encoder.fit(classes)
            
            logger.info("Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def evaluate_model(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """
        Evaluate the model performance.
        
        Args:
            X (pd.DataFrame): Feature matrix
            y (pd.Series): Target labels
            
        Returns:
            Dict[str, Any]: Evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Encode target labels
        y_encoded = self.label_encoder.transform(y)
        
        # Make predictions
        y_pred = self.model.predict(X)
        
        # Calculate metrics
        accuracy = accuracy_score(y_encoded, y_pred)
        cv_scores = cross_val_score(self.model, X, y_encoded, cv=5)
        
        # Classification report
        report = classification_report(y_encoded, y_pred, output_dict=True)
        
        return {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'classification_report': report
        }

def main():
    """
    Test the model training and prediction.
    """
    from data_processing import CareerDataProcessor
    
    # Load and preprocess data
    processor = CareerDataProcessor()
    df = processor.load_data('data/career_data.csv')
    X, y = processor.preprocess_data(df)
    
    # Train model
    model = CareerRecommendationModel('random_forest')
    results = model.train(X, y, processor.feature_columns)
    
    print("Training Results:")
    print(f"Accuracy: {results['accuracy']:.4f}")
    print(f"CV Score: {results['cv_mean']:.4f} (+/- {results['cv_std'] * 2:.4f})")
    
    # Save model
    model.save_model()
    
    # Test prediction
    user_input = {
        '10th_score': 85,
        '12th_score': 82,
        'ug_score': 78,
        'skills': 'Python,SQL,Statistics,ML',
        'interests': 'Research,Analysis,Development'
    }
    
    user_features = processor.preprocess_user_input(user_input)
    prediction, confidence = model.predict(user_features)
    
    print(f"\nPrediction: {prediction}")
    print(f"Confidence: {confidence:.4f}")
    
    # Get top features
    top_features = model.get_feature_importance(5)
    print(f"\nTop 5 Features:")
    for feature, importance in top_features:
        print(f"  {feature}: {importance:.4f}")

if __name__ == "__main__":
    main()
