"""
Neural Network Model for Career Recommendation

This module implements a deep learning model using TensorFlow/Keras
for career path prediction.
"""

import numpy as np
import pandas as pd
import logging
import os
import json
from typing import Dict, List, Tuple, Any, Optional
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

# TensorFlow imports
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logging.warning("TensorFlow not available. Neural network model will not work.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NeuralNetworkCareerModel:
    """
    Deep learning model for career recommendations using TensorFlow/Keras.
    """
    
    def __init__(self, model_path: str = 'models/nn_career_model'):
        """
        Initialize the neural network model.
        
        Args:
            model_path (str): Path to save/load the model
        """
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is not installed. Install with: pip install tensorflow")
        
        self.model_path = model_path
        self.model = None
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.history = None
        
        # Model configuration
        self.config = {
            'hidden_layers': [256, 128, 64, 32],
            'dropout_rate': 0.3,
            'learning_rate': 0.001,
            'batch_size': 32,
            'epochs': 100,
            'early_stopping_patience': 15,
            'reduce_lr_patience': 5
        }
    
    def create_model(self, input_dim: int, output_dim: int) -> keras.Model:
        """
        Create a deep neural network model.
        
        Args:
            input_dim (int): Number of input features
            output_dim (int): Number of output classes
            
        Returns:
            keras.Model: Compiled neural network model
        """
        model = models.Sequential([
            # Input layer
            layers.Input(shape=(input_dim,)),
            layers.BatchNormalization(),
            
            # Hidden layers
            layers.Dense(self.config['hidden_layers'][0], activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(self.config['dropout_rate']),
            
            layers.Dense(self.config['hidden_layers'][1], activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(self.config['dropout_rate']),
            
            layers.Dense(self.config['hidden_layers'][2], activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(self.config['dropout_rate']),
            
            layers.Dense(self.config['hidden_layers'][3], activation='relu'),
            layers.Dropout(self.config['dropout_rate']),
            
            # Output layer
            layers.Dense(output_dim, activation='softmax')
        ])
        
        # Compile model
        optimizer = keras.optimizers.Adam(learning_rate=self.config['learning_rate'])
        model.compile(
            optimizer=optimizer,
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy', 'top_k_categorical_accuracy']
        )
        
        logger.info("Neural network model created")
        logger.info(f"Architecture: {self.config['hidden_layers']} -> {output_dim}")
        
        return model
    
    def train(self, X: pd.DataFrame, y: pd.Series, feature_columns: List[str],
              validation_split: float = 0.2) -> Dict[str, Any]:
        """
        Train the neural network model.
        
        Args:
            X (pd.DataFrame): Feature matrix
            y (pd.Series): Target labels
            feature_columns (List[str]): List of feature column names
            validation_split (float): Validation split ratio
            
        Returns:
            Dict[str, Any]: Training results and metrics
        """
        logger.info("Training Neural Network model...")
        
        # Store feature columns
        self.feature_columns = feature_columns
        
        # Encode target labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Create model
        input_dim = X_train.shape[1]
        output_dim = len(self.label_encoder.classes_)
        self.model = self.create_model(input_dim, output_dim)
        
        # Print model summary
        logger.info(f"Model summary:")
        self.model.summary()
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=self.config['early_stopping_patience'],
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=self.config['reduce_lr_patience'],
                min_lr=1e-7,
                verbose=1
            ),
            ModelCheckpoint(
                filepath=f"{self.model_path}_best.h5",
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Train model
        self.history = self.model.fit(
            X_train, y_train,
            batch_size=self.config['batch_size'],
            epochs=self.config['epochs'],
            validation_split=validation_split,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate on test set
        test_loss, test_accuracy, test_top_k_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        
        # Make predictions
        y_pred = self.model.predict(X_test, verbose=0)
        y_pred_classes = np.argmax(y_pred, axis=1)
        
        # Calculate metrics
        from sklearn.metrics import classification_report, confusion_matrix
        
        results = {
            'test_accuracy': float(test_accuracy),
            'test_loss': float(test_loss),
            'test_top_k_accuracy': float(test_top_k_accuracy),
            'training_history': {
                'loss': [float(x) for x in self.history.history['loss']],
                'accuracy': [float(x) for x in self.history.history['accuracy']],
                'val_loss': [float(x) for x in self.history.history['val_loss']],
                'val_accuracy': [float(x) for x in self.history.history['val_accuracy']]
            },
            'epochs_trained': len(self.history.history['loss']),
            'classification_report': classification_report(y_test, y_pred_classes, output_dict=True),
            'confusion_matrix': confusion_matrix(y_test, y_pred_classes).tolist()
        }
        
        logger.info(f"Model training completed.")
        logger.info(f"Test Accuracy: {test_accuracy:.4f}")
        logger.info(f"Test Top-K Accuracy: {test_top_k_accuracy:.4f}")
        logger.info(f"Epochs Trained: {results['epochs_trained']}")
        
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
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        predictions = self.model.predict(X_scaled, verbose=0)
        prediction_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][prediction_idx])
        
        # Decode prediction
        career = self.label_encoder.inverse_transform([prediction_idx])[0]
        
        return career, confidence
    
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
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        predictions = self.model.predict(X_scaled, verbose=0)[0]
        
        # Get top-k indices
        top_indices = np.argsort(predictions)[-top_k:][::-1]
        
        # Get corresponding careers and confidences
        careers = self.label_encoder.inverse_transform(top_indices)
        confidences = predictions[top_indices]
        
        return list(zip(careers, confidences))
    
    def save_model(self):
        """Save the trained model and metadata."""
        if self.model is None:
            raise ValueError("No model to save. Please train the model first.")
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Save Keras model
        self.model.save(f"{self.model_path}.h5")
        
        # Save scaler
        joblib.dump(self.scaler, f"{self.model_path}_scaler.pkl")
        
        # Save label encoder
        joblib.dump(self.label_encoder, f"{self.model_path}_encoder.pkl")
        
        # Save metadata
        metadata = {
            'model_type': 'neural_network',
            'feature_columns': self.feature_columns,
            'label_classes': self.label_encoder.classes_.tolist(),
            'config': self.config,
            'input_shape': self.model.input_shape,
            'output_shape': self.model.output_shape
        }
        
        with open(f"{self.model_path}_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self) -> bool:
        """
        Load a previously trained model.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            model_file = f"{self.model_path}.h5"
            if not os.path.exists(model_file):
                logger.warning(f"Model file not found: {model_file}")
                return False
            
            # Load Keras model
            self.model = keras.models.load_model(model_file)
            
            # Load scaler
            self.scaler = joblib.load(f"{self.model_path}_scaler.pkl")
            
            # Load label encoder
            self.label_encoder = joblib.load(f"{self.model_path}_encoder.pkl")
            
            # Load metadata
            with open(f"{self.model_path}_metadata.json", 'r') as f:
                metadata = json.load(f)
            
            self.feature_columns = metadata.get('feature_columns', [])
            self.config = metadata.get('config', self.config)
            
            logger.info("Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def plot_training_history(self, save_path: str = 'models/training_history.png'):
        """
        Plot training history.
        
        Args:
            save_path (str): Path to save the plot
        """
        if self.history is None:
            logger.warning("No training history available")
            return
        
        try:
            import matplotlib.pyplot as plt
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            
            # Plot accuracy
            ax1.plot(self.history.history['accuracy'], label='Training Accuracy')
            ax1.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
            ax1.set_title('Model Accuracy')
            ax1.set_xlabel('Epoch')
            ax1.set_ylabel('Accuracy')
            ax1.legend()
            ax1.grid(True)
            
            # Plot loss
            ax2.plot(self.history.history['loss'], label='Training Loss')
            ax2.plot(self.history.history['val_loss'], label='Validation Loss')
            ax2.set_title('Model Loss')
            ax2.set_xlabel('Epoch')
            ax2.set_ylabel('Loss')
            ax2.legend()
            ax2.grid(True)
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Training history plot saved to {save_path}")
            
        except Exception as e:
            logger.error(f"Error plotting training history: {e}")


def main():
    """Test the neural network model."""
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
    
    from data_processing import CareerDataProcessor
    from database import DatabaseManager
    
    # Load data from database
    db = DatabaseManager('data/career_system.db')
    career_data = db.get_all_career_data()
    
    # Convert to DataFrame
    df = pd.DataFrame(career_data)
    df = df.rename(columns={
        'score_10th': '10th_Score',
        'score_12th': '12th_Score',
        'score_ug': 'UG_Score',
        'skills': 'Skills',
        'interests': 'Interests',
        'recommended_career': 'Recommended_Career'
    })
    
    # Preprocess data
    processor = CareerDataProcessor()
    X, y = processor.preprocess_data(df)
    
    # Train neural network
    nn_model = NeuralNetworkCareerModel()
    results = nn_model.train(X, y, processor.feature_columns)
    
    print("\nTraining Results:")
    print(f"Test Accuracy: {results['test_accuracy']:.4f}")
    print(f"Test Top-K Accuracy: {results['test_top_k_accuracy']:.4f}")
    print(f"Epochs Trained: {results['epochs_trained']}")
    
    # Save model
    nn_model.save_model()
    
    # Plot training history
    nn_model.plot_training_history()
    
    # Test prediction
    user_input = {
        '10th_score': 85,
        '12th_score': 82,
        'ug_score': 78,
        'skills': 'Python,SQL,Statistics,ML',
        'interests': 'Research,Analysis,Development'
    }
    
    user_features = processor.preprocess_user_input(user_input)
    prediction, confidence = nn_model.predict(user_features)
    
    print(f"\nTest Prediction:")
    print(f"Career: {prediction}")
    print(f"Confidence: {confidence:.4f}")
    
    # Get top 3 predictions
    top_predictions = nn_model.predict_multiple(user_features, top_k=3)
    print(f"\nTop 3 Predictions:")
    for i, (career, conf) in enumerate(top_predictions, 1):
        print(f"{i}. {career}: {conf:.4f}")


if __name__ == "__main__":
    main()

