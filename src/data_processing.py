"""
Data Processing Module for Career Recommendation System

This module handles data preprocessing, validation, and encoding for the career recommendation system.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import re
from typing import Dict, List, Tuple, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CareerDataProcessor:
    """
    Handles data preprocessing for career recommendation system.
    """
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.target_column = 'Recommended_Career'
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load career data from CSV file.
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            pd.DataFrame: Loaded dataset
        """
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def validate_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Validate and clean score inputs.
        
        Args:
            scores (Dict[str, float]): Dictionary containing score values
            
        Returns:
            Dict[str, float]: Validated and cleaned scores
        """
        validated_scores = {}
        
        for score_type, value in scores.items():
            if value is None or pd.isna(value):
                validated_scores[score_type] = 0.0
            elif not isinstance(value, (int, float)):
                try:
                    validated_scores[score_type] = float(value)
                except ValueError:
                    validated_scores[score_type] = 0.0
            else:
                validated_scores[score_type] = float(value)
            
            # Ensure scores are within valid range (0-100)
            validated_scores[score_type] = max(0.0, min(100.0, validated_scores[score_type]))
        
        return validated_scores
    
    def parse_skills(self, skills_str: str) -> List[str]:
        """
        Parse skills string into a list of individual skills.
        
        Args:
            skills_str (str): Comma-separated skills string
            
        Returns:
            List[str]: List of individual skills
        """
        if not skills_str or pd.isna(skills_str):
            return []
        
        # Split by comma and clean each skill
        skills = [skill.strip() for skill in str(skills_str).split(',')]
        # Remove empty strings and duplicates
        skills = list(set([skill for skill in skills if skill]))
        return skills
    
    def parse_interests(self, interests_str: str) -> List[str]:
        """
        Parse interests string into a list of individual interests.
        
        Args:
            interests_str (str): Comma-separated interests string
            
        Returns:
            List[str]: List of individual interests
        """
        if not interests_str or pd.isna(interests_str):
            return []
        
        # Split by comma and clean each interest
        interests = [interest.strip() for interest in str(interests_str).split(',')]
        # Remove empty strings and duplicates
        interests = list(set([interest for interest in interests if interest]))
        return interests
    
    def create_skill_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create binary features for each skill.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with skill features
        """
        # Get all unique skills from the dataset
        all_skills = set()
        for skills_str in df['Skills'].dropna():
            skills = self.parse_skills(skills_str)
            all_skills.update(skills)
        
        # Create binary features for each skill
        for skill in all_skills:
            df[f'has_{skill.replace(" ", "_").replace("/", "_").replace("-", "_").lower()}'] = df['Skills'].apply(
                lambda x: 1 if skill in self.parse_skills(x) else 0
            )
        
        return df
    
    def create_interest_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create binary features for each interest.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with interest features
        """
        # Get all unique interests from the dataset
        all_interests = set()
        for interests_str in df['Interests'].dropna():
            interests = self.parse_interests(interests_str)
            all_interests.update(interests)
        
        # Create binary features for each interest
        for interest in all_interests:
            df[f'interest_{interest.replace(" ", "_").replace("/", "_").replace("-", "_").lower()}'] = df['Interests'].apply(
                lambda x: 1 if interest in self.parse_interests(x) else 0
            )
        
        return df
    
    def preprocess_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Preprocess the dataset for training.
        
        Args:
            df (pd.DataFrame): Raw dataset
            
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Processed features and target
        """
        logger.info("Starting data preprocessing...")
        
        # Create a copy to avoid modifying original data
        df_processed = df.copy()
        
        # Validate and clean scores
        score_columns = ['10th_Score', '12th_Score', 'UG_Score']
        for col in score_columns:
            df_processed[col] = df_processed[col].apply(
                lambda x: max(0.0, min(100.0, float(x))) if pd.notna(x) else 0.0
            )
        
        # Create skill features
        df_processed = self.create_skill_features(df_processed)
        
        # Create interest features
        df_processed = self.create_interest_features(df_processed)
        
        # Prepare feature columns (exclude original text columns and target)
        exclude_columns = ['Student_ID', 'Skills', 'Interests', self.target_column]
        self.feature_columns = [col for col in df_processed.columns if col not in exclude_columns]
        
        # Separate features and target
        X = df_processed[self.feature_columns]
        y = df_processed[self.target_column]
        
        # Handle missing values
        X = X.fillna(0)
        
        logger.info(f"Preprocessing completed. Features: {len(self.feature_columns)}")
        logger.info(f"Feature columns: {self.feature_columns[:10]}...")  # Show first 10 features
        
        return X, y
    
    def preprocess_user_input(self, user_data: Dict[str, Any]) -> np.ndarray:
        """
        Preprocess user input for prediction.
        
        Args:
            user_data (Dict[str, Any]): User input data
            
        Returns:
            np.ndarray: Processed feature vector
        """
        logger.info("Preprocessing user input...")
        
        # Validate scores
        scores = self.validate_scores({
            '10th_Score': user_data.get('10th_score', 0),
            '12th_Score': user_data.get('12th_score', 0),
            'UG_Score': user_data.get('ug_score', 0)
        })
        
        # Parse skills and interests
        skills = self.parse_skills(user_data.get('skills', ''))
        interests = self.parse_interests(user_data.get('interests', ''))
        
        # Create feature vector
        feature_vector = np.zeros(len(self.feature_columns))
        
        # Set score features
        score_mapping = {
            '10th_Score': '10th_Score',
            '12th_Score': '12th_Score', 
            'UG_Score': 'UG_Score'
        }
        
        for user_key, feature_name in score_mapping.items():
            if feature_name in self.feature_columns:
                idx = self.feature_columns.index(feature_name)
                feature_vector[idx] = scores[user_key]
        
        # Set skill features
        for skill in skills:
            feature_name = f'has_{skill.replace(" ", "_").replace("/", "_").replace("-", "_").lower()}'
            if feature_name in self.feature_columns:
                idx = self.feature_columns.index(feature_name)
                feature_vector[idx] = 1
        
        # Set interest features
        for interest in interests:
            feature_name = f'interest_{interest.replace(" ", "_").replace("/", "_").replace("-", "_").lower()}'
            if feature_name in self.feature_columns:
                idx = self.feature_columns.index(feature_name)
                feature_vector[idx] = 1
        
        logger.info("User input preprocessing completed")
        return feature_vector.reshape(1, -1)
    
    def get_feature_importance(self, model, feature_names: List[str]) -> Dict[str, float]:
        """
        Get feature importance from trained model.
        
        Args:
            model: Trained model with feature_importances_ attribute
            feature_names (List[str]): List of feature names
            
        Returns:
            Dict[str, float]: Feature importance scores
        """
        if hasattr(model, 'feature_importances_'):
            importance_scores = model.feature_importances_
            return dict(zip(feature_names, importance_scores))
        else:
            logger.warning("Model does not have feature_importances_ attribute")
            return {}

def main():
    """
    Test the data processing module.
    """
    processor = CareerDataProcessor()
    
    # Load sample data
    df = processor.load_data('data/career_data.csv')
    
    # Preprocess data
    X, y = processor.preprocess_data(df)
    
    print(f"Processed dataset shape: {X.shape}")
    print(f"Target classes: {y.unique()}")
    print(f"Feature columns: {len(processor.feature_columns)}")
    
    # Test user input preprocessing
    user_input = {
        '10th_score': 85,
        '12th_score': 82,
        'ug_score': 78,
        'skills': 'Python,SQL,Statistics,ML',
        'interests': 'Research,Analysis,Development'
    }
    
    user_features = processor.preprocess_user_input(user_input)
    print(f"User input features shape: {user_features.shape}")

if __name__ == "__main__":
    main()
