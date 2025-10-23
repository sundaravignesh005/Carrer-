"""
Salary Prediction Module

This module predicts salary ranges based on career, location,
skills, and experience using machine learning.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
import joblib
import os
import json
import logging
from typing import Dict, List, Tuple, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SalaryPredictor:
    """
    Predicts salary ranges based on career, skills, experience, and location.
    """
    
    def __init__(self, model_path: str = 'models/salary_predictor.pkl'):
        """Initialize the salary predictor."""
        self.model_path = model_path
        self.model = None
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = []
        
        # Salary data for Indian market (in LPA - Lakhs Per Annum)
        self.salary_data = self._generate_salary_data()
    
    def _generate_salary_data(self) -> pd.DataFrame:
        """
        Generate salary dataset for training.
        
        Returns:
            pd.DataFrame: Salary dataset
        """
        data = []
        
        # Career-wise salary ranges with experience
        careers_salary = {
            'Data Scientist': {
                '0-2': (4, 8), '2-5': (8, 15), '5-8': (15, 25), '8+': (25, 40)
            },
            'Machine Learning Engineer': {
                '0-2': (5, 10), '2-5': (10, 18), '5-8': (18, 30), '8+': (30, 50)
            },
            'Software Developer': {
                '0-2': (3, 7), '2-5': (7, 14), '5-8': (14, 22), '8+': (22, 35)
            },
            'Full Stack Developer': {
                '0-2': (4, 8), '2-5': (8, 16), '5-8': (16, 25), '8+': (25, 40)
            },
            'Data Analyst': {
                '0-2': (3, 6), '2-5': (6, 12), '5-8': (12, 18), '8+': (18, 28)
            },
            'DevOps Engineer': {
                '0-2': (4, 8), '2-5': (8, 16), '5-8': (16, 26), '8+': (26, 42)
            },
            'Cloud Engineer': {
                '0-2': (5, 10), '2-5': (10, 18), '5-8': (18, 28), '8+': (28, 45)
            },
            'Web Developer': {
                '0-2': (2, 5), '2-5': (5, 10), '5-8': (10, 16), '8+': (16, 25)
            },
            'Mobile Developer': {
                '0-2': (3, 7), '2-5': (7, 14), '5-8': (14, 22), '8+': (22, 35)
            },
            'UI/UX Developer': {
                '0-2': (3, 6), '2-5': (6, 12), '5-8': (12, 20), '8+': (20, 30)
            },
            'Business Analyst': {
                '0-2': (3, 6), '2-5': (6, 12), '5-8': (12, 18), '8+': (18, 28)
            },
            'Product Manager': {
                '0-2': (6, 12), '2-5': (12, 22), '5-8': (22, 35), '8+': (35, 60)
            },
            'AI Engineer': {
                '0-2': (6, 12), '2-5': (12, 22), '5-8': (22, 35), '8+': (35, 55)
            },
            'Cybersecurity Analyst': {
                '0-2': (4, 8), '2-5': (8, 16), '5-8': (16, 25), '8+': (25, 40)
            },
            'Database Administrator': {
                '0-2': (3, 7), '2-5': (7, 14), '5-8': (14, 22), '8+': (22, 35)
            },
            'QA Engineer': {
                '0-2': (2, 5), '2-5': (5, 10), '5-8': (10, 16), '8+': (16, 25)
            },
            'Network Engineer': {
                '0-2': (3, 6), '2-5': (6, 12), '5-8': (12, 18), '8+': (18, 28)
            },
            'Blockchain Developer': {
                '0-2': (5, 10), '2-5': (10, 20), '5-8': (20, 35), '8+': (35, 60)
            },
            'Game Developer': {
                '0-2': (3, 7), '2-5': (7, 14), '5-8': (14, 25), '8+': (25, 40)
            },
            'System Administrator': {
                '0-2': (2, 5), '2-5': (5, 10), '5-8': (10, 16), '8+': (16, 25)
            }
        }
        
        # Cities with multipliers
        cities = {
            'Bangalore': 1.15, 'Mumbai': 1.12, 'Delhi': 1.10, 'Hyderabad': 1.08,
            'Pune': 1.05, 'Chennai': 1.03, 'Kolkata': 0.98, 'Ahmedabad': 0.95,
            'Gurgaon': 1.10, 'Noida': 1.05, 'Remote': 1.0, 'India': 1.0
        }
        
        # Skills that boost salary
        high_value_skills = [
            'ML', 'Deep Learning', 'AI', 'Cloud', 'AWS', 'Azure', 'Kubernetes',
            'Docker', 'Blockchain', 'Big Data', 'Spark', 'Leadership'
        ]
        
        # Generate samples
        for career, exp_ranges in careers_salary.items():
            for exp_range, (min_sal, max_sal) in exp_ranges.items():
                for city, multiplier in cities.items():
                    for _ in range(3):  # 3 samples per combination
                        # Base experience
                        if exp_range == '0-2':
                            experience = np.random.uniform(0, 2)
                        elif exp_range == '2-5':
                            experience = np.random.uniform(2, 5)
                        elif exp_range == '5-8':
                            experience = np.random.uniform(5, 8)
                        else:
                            experience = np.random.uniform(8, 15)
                        
                        # Base salary
                        base_salary = np.random.uniform(min_sal, max_sal)
                        
                        # Apply city multiplier
                        salary = base_salary * multiplier
                        
                        # Skill count effect (more skills = higher salary)
                        skill_count = np.random.randint(3, 12)
                        has_high_value_skills = np.random.randint(0, 4)  # 0-3 high-value skills
                        
                        # Boost salary based on skills
                        salary *= (1 + (skill_count * 0.02))  # 2% per skill
                        salary *= (1 + (has_high_value_skills * 0.05))  # 5% per high-value skill
                        
                        # Education bonus
                        education_level = np.random.choice(['Bachelor', 'Master', 'PhD'])
                        if education_level == 'Master':
                            salary *= 1.10
                        elif education_level == 'PhD':
                            salary *= 1.20
                        
                        # Add some noise
                        salary *= np.random.uniform(0.95, 1.05)
                        
                        data.append({
                            'career': career,
                            'experience_years': round(experience, 1),
                            'location': city,
                            'skill_count': skill_count,
                            'high_value_skills': has_high_value_skills,
                            'education': education_level,
                            'salary_lpa': round(salary, 2)
                        })
        
        df = pd.DataFrame(data)
        logger.info(f"Generated {len(df)} salary records for training")
        
        return df
    
    def train(self) -> Dict[str, Any]:
        """
        Train the salary prediction model.
        
        Returns:
            Dict[str, Any]: Training results
        """
        logger.info("Training salary prediction model...")
        
        df = self.salary_data
        
        # Prepare features
        categorical_features = ['career', 'location', 'education']
        numerical_features = ['experience_years', 'skill_count', 'high_value_skills']
        
        # Encode categorical features
        X = df.copy()
        for col in categorical_features:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            self.label_encoders[col] = le
        
        # Select features
        self.feature_columns = categorical_features + numerical_features
        X = X[self.feature_columns]
        y = df['salary_lpa']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_scaled, y, cv=5)
        
        # Calculate metrics
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        results = {
            'train_score': float(train_score),
            'test_score': float(test_score),
            'cv_mean': float(cv_scores.mean()),
            'cv_std': float(cv_scores.std()),
            'mae': float(mae),
            'rmse': float(rmse),
            'r2_score': float(r2),
            'samples': len(df)
        }
        
        logger.info(f"Model trained. R² Score: {r2:.4f}, RMSE: {rmse:.2f} LPA")
        
        return results
    
    def predict_salary(self, career: str, experience_years: float,
                      location: str, skills: List[str],
                      education: str = 'Bachelor') -> Dict[str, Any]:
        """
        Predict salary for given parameters.
        
        Args:
            career (str): Career path
            experience_years (float): Years of experience
            location (str): Work location
            skills (List[str]): List of skills
            education (str): Education level
            
        Returns:
            Dict[str, Any]: Salary prediction
        """
        if self.model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Count skills
        skill_count = len(skills)
        
        # Count high-value skills
        high_value_skills = ['ML', 'Deep Learning', 'AI', 'Cloud', 'AWS', 'Azure',
                            'Kubernetes', 'Docker', 'Blockchain', 'Big Data', 'Spark']
        high_value_count = sum(1 for skill in skills 
                              if any(hv.lower() in skill.lower() for hv in high_value_skills))
        
        # Prepare input
        input_data = {
            'career': career,
            'experience_years': experience_years,
            'location': location,
            'skill_count': skill_count,
            'high_value_skills': high_value_count,
            'education': education
        }
        
        # Encode categorical features
        X = pd.DataFrame([input_data])
        for col in ['career', 'location', 'education']:
            if col in self.label_encoders:
                try:
                    X[col] = self.label_encoders[col].transform([input_data[col]])[0]
                except ValueError:
                    # Handle unknown categories
                    X[col] = 0
        
        # Select and scale features
        X = X[self.feature_columns]
        X_scaled = self.scaler.transform(X)
        
        # Predict
        predicted_salary = self.model.predict(X_scaled)[0]
        
        # Calculate range (±15%)
        min_salary = predicted_salary * 0.85
        max_salary = predicted_salary * 1.15
        
        # Market comparison
        market_position = self._get_market_position(career, experience_years, predicted_salary)
        
        result = {
            'predicted_salary': round(predicted_salary, 2),
            'min_salary': round(min_salary, 2),
            'max_salary': round(max_salary, 2),
            'currency': 'INR (LPA)',
            'confidence': 'Medium' if skill_count >= 5 else 'Low',
            'market_position': market_position,
            'factors': {
                'career': career,
                'experience': f"{experience_years} years",
                'location': location,
                'skills': f"{skill_count} skills",
                'high_value_skills': f"{high_value_count} premium skills",
                'education': education
            },
            'recommendations': self._get_salary_recommendations(
                predicted_salary, experience_years, skill_count
            )
        }
        
        return result
    
    def _get_market_position(self, career: str, experience: float,
                            predicted_salary: float) -> str:
        """Determine market position."""
        # Get similar profiles from data
        similar = self.salary_data[
            (self.salary_data['career'] == career) &
            (abs(self.salary_data['experience_years'] - experience) <= 2)
        ]
        
        if len(similar) == 0:
            return 'Average'
        
        percentile = (similar['salary_lpa'] < predicted_salary).mean() * 100
        
        if percentile >= 75:
            return 'Above Average (Top 25%)'
        elif percentile >= 50:
            return 'Average (50th percentile)'
        elif percentile >= 25:
            return 'Below Average (Bottom 50%)'
        else:
            return 'Entry Level (Bottom 25%)'
    
    def _get_salary_recommendations(self, salary: float, experience: float,
                                   skill_count: int) -> List[str]:
        """Get recommendations to increase salary."""
        recommendations = []
        
        if skill_count < 8:
            recommendations.append("Learn additional in-demand skills to increase market value")
        
        if experience < 5:
            recommendations.append("Gain more experience in your field")
        
        recommendations.append("Consider high-growth cities like Bangalore or Mumbai")
        recommendations.append("Obtain relevant certifications in your domain")
        
        if salary < 10:
            recommendations.append("Focus on building strong project portfolio")
        
        return recommendations
    
    def save_model(self):
        """Save the trained model."""
        if self.model is None:
            raise ValueError("No model to save")
        
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Save model
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, f"{self.model_path}_scaler.pkl")
        
        # Save label encoders
        for name, encoder in self.label_encoders.items():
            joblib.dump(encoder, f"{self.model_path}_encoder_{name}.pkl")
        
        # Save metadata
        metadata = {
            'feature_columns': self.feature_columns,
            'encoder_names': list(self.label_encoders.keys())
        }
        
        with open(f"{self.model_path}_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self) -> bool:
        """Load a trained model."""
        try:
            if not os.path.exists(self.model_path):
                return False
            
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(f"{self.model_path}_scaler.pkl")
            
            # Load metadata
            with open(f"{self.model_path}_metadata.json", 'r') as f:
                metadata = json.load(f)
            
            self.feature_columns = metadata['feature_columns']
            
            # Load label encoders
            for name in metadata['encoder_names']:
                self.label_encoders[name] = joblib.load(
                    f"{self.model_path}_encoder_{name}.pkl"
                )
            
            logger.info("Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False


def main():
    """Test salary predictor."""
    predictor = SalaryPredictor()
    
    print("="*70)
    print("Salary Predictor - Test")
    print("="*70)
    
    # Train model
    print("\n1. Training model...")
    results = predictor.train()
    print(f"   R² Score: {results['r2_score']:.4f}")
    print(f"   RMSE: {results['rmse']:.2f} LPA")
    print(f"   MAE: {results['mae']:.2f} LPA")
    
    # Save model
    predictor.save_model()
    print("   Model saved!")
    
    # Test predictions
    print("\n2. Salary Predictions:\n")
    
    test_cases = [
        {
            'career': 'Data Scientist',
            'experience_years': 3,
            'location': 'Bangalore',
            'skills': ['Python', 'ML', 'SQL', 'Statistics', 'Deep Learning', 'TensorFlow'],
            'education': 'Master'
        },
        {
            'career': 'Software Developer',
            'experience_years': 1,
            'location': 'Pune',
            'skills': ['Java', 'Spring Boot', 'MySQL'],
            'education': 'Bachelor'
        },
        {
            'career': 'AI Engineer',
            'experience_years': 6,
            'location': 'Mumbai',
            'skills': ['Python', 'AI', 'Deep Learning', 'ML', 'NLP', 'Computer Vision', 'Cloud', 'AWS'],
            'education': 'PhD'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        prediction = predictor.predict_salary(**test_case)
        
        print(f"   Case {i}: {test_case['career']} with {test_case['experience_years']} years")
        print(f"   Location: {test_case['location']}")
        print(f"   Predicted Salary: ₹{prediction['predicted_salary']} LPA")
        print(f"   Range: ₹{prediction['min_salary']}-{prediction['max_salary']} LPA")
        print(f"   Market Position: {prediction['market_position']}")
        print()
    
    print("="*70)
    print("Salary Predictor Test Complete!")
    print("="*70)


if __name__ == "__main__":
    main()

