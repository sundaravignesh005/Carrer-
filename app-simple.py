"""
Simple Flask app for Vercel deployment
Minimal version without heavy dependencies
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Sample career data (instead of loading ML model)
CAREER_DATA = {
    "Data Scientist": {
        "skills": ["Python", "SQL", "Statistics", "ML", "Data Analysis"],
        "description": "Analyze data to help organizations make decisions"
    },
    "Software Developer": {
        "skills": ["Programming", "Algorithms", "OOP", "Git", "Testing"],
        "description": "Design and develop software applications"
    },
    "Machine Learning Engineer": {
        "skills": ["Python", "ML", "Deep Learning", "TensorFlow", "Statistics"],
        "description": "Build and deploy machine learning models"
    },
    "Data Analyst": {
        "skills": ["SQL", "Excel", "Statistics", "Python", "Visualization"],
        "description": "Analyze data to provide business insights"
    },
    "Web Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
        "description": "Create and maintain websites and web applications"
    }
}

@app.route('/')
def home():
    return jsonify({
        "message": "AI-Based Career Path Recommendation System",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Get career recommendation",
            "/health": "GET - Health check",
            "/careers": "GET - List all careers"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/careers')
def get_careers():
    return jsonify(list(CAREER_DATA.keys()))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Simple career matching based on skills
        user_skills = [skill.strip().lower() for skill in data.get('skills', '').split(',')]
        
        best_match = None
        best_score = 0
        
        for career, info in CAREER_DATA.items():
            career_skills = [skill.lower() for skill in info['skills']]
            matches = sum(1 for skill in user_skills if skill in career_skills)
            score = matches / len(career_skills) if career_skills else 0
            
            if score > best_score:
                best_score = score
                best_match = career
        
        if not best_match:
            best_match = "Software Developer"  # Default
            best_score = 0.3
        
        # Sample job recommendations
        jobs = [
            {
                "title": f"{best_match}",
                "company": "TechCorp India",
                "location": "Bangalore, India",
                "salary": "₹6-12 LPA",
                "description": f"Looking for a {best_match} with relevant skills",
                "apply_link": "https://example.com/apply/1"
            },
            {
                "title": f"Senior {best_match}",
                "company": "AI Solutions Pvt Ltd",
                "location": "Mumbai, India",
                "salary": "₹8-15 LPA",
                "description": f"Senior {best_match} position with growth opportunities",
                "apply_link": "https://example.com/apply/2"
            }
        ]
        
        # Simple skills analysis
        skills_analysis = {
            "target_career": best_match,
            "overall_readiness": round(best_score * 100, 1),
            "readiness_level": "Ready" if best_score > 0.6 else "Needs Development",
            "priority_skills_to_learn": [skill for skill in CAREER_DATA[best_match]['skills'] 
                                      if skill.lower() not in user_skills][:3]
        }
        
        return jsonify({
            "prediction": best_match,
            "confidence": round(best_score, 3),
            "jobs": jobs,
            "skills_analysis": skills_analysis,
            "description": CAREER_DATA[best_match]['description']
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.get_json()
        # Simple feedback storage (in production, use database)
        return jsonify({"message": "Feedback received successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
