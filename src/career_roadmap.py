"""
Career Roadmap Generator

This module generates step-by-step learning paths for different career trajectories.
"""

import logging
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CareerRoadmapGenerator:
    """
    Generates personalized career roadmaps with learning paths.
    """
    
    def __init__(self):
        """Initialize the roadmap generator."""
        self.roadmaps = self._load_roadmaps()
    
    def _load_roadmaps(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load predefined career roadmaps."""
        return {
            'Data Scientist': [
                {
                    'level': 'Beginner', 'duration': '3-4 months',
                    'steps': [
                        {'title': 'Learn Python Basics', 'skills': ['Python', 'Programming fundamentals'],
                         'resources': ['Coursera Python for Everybody', 'Python.org tutorials']},
                        {'title': 'Master Statistics & Mathematics', 'skills': ['Statistics', 'Probability', 'Linear Algebra'],
                         'resources': ['Khan Academy Statistics', 'MIT OpenCourseWare']},
                        {'title': 'SQL & Databases', 'skills': ['SQL', 'Database fundamentals'],
                         'resources': ['Mode Analytics SQL', 'W3Schools SQL']}
                    ]
                },
                {
                    'level': 'Intermediate', 'duration': '4-6 months',
                    'steps': [
                        {'title': 'Data Analysis Libraries', 'skills': ['Pandas', 'NumPy', 'Matplotlib'],
                         'resources': ['DataCamp', 'Kaggle Learn']},
                        {'title': 'Machine Learning Fundamentals', 'skills': ['ML algorithms', 'Scikit-learn'],
                         'resources': ['Andrew Ng ML Course', 'Hands-On ML Book']},
                        {'title': 'Data Visualization', 'skills': ['Tableau', 'Power BI', 'Plotly'],
                         'resources': ['Tableau Public', 'Power BI Microsoft Learn']}
                    ]
                },
                {
                    'level': 'Advanced', 'duration': '6-8 months',
                    'steps': [
                        {'title': 'Deep Learning', 'skills': ['Neural Networks', 'TensorFlow', 'PyTorch'],
                         'resources': ['Deep Learning Specialization', 'Fast.ai']},
                        {'title': 'Big Data & Cloud', 'skills': ['Spark', 'AWS', 'Azure'],
                         'resources': ['AWS Training', 'Databricks Academy']},
                        {'title': 'Deploy ML Models', 'skills': ['MLOps', 'Docker', 'Flask/FastAPI'],
                         'resources': ['MLOps courses', 'Docker documentation']}
                    ]
                }
            ],
            'Software Developer': [
                {
                    'level': 'Beginner', 'duration': '2-3 months',
                    'steps': [
                        {'title': 'Programming Language', 'skills': ['Choose: Python/Java/JavaScript'],
                         'resources': ['FreeCodeCamp', 'Codecademy']},
                        {'title': 'Data Structures & Algorithms', 'skills': ['Arrays', 'Lists', 'Trees', 'Graphs'],
                         'resources': ['LeetCode', 'HackerRank', 'AlgoExpert']},
                        {'title': 'Version Control', 'skills': ['Git', 'GitHub'],
                         'resources': ['Git documentation', 'GitHub Learning Lab']}
                    ]
                },
                {
                    'level': 'Intermediate', 'duration': '4-5 months',
                    'steps': [
                        {'title': 'Web Development Basics', 'skills': ['HTML', 'CSS', 'JavaScript'],
                         'resources': ['MDN Web Docs', 'FreeCodeCamp']},
                        {'title': 'Backend Framework', 'skills': ['Spring Boot/Django/Express'],
                         'resources': ['Framework official docs', 'Udemy courses']},
                        {'title': 'Databases', 'skills': ['SQL', 'NoSQL', 'Database design'],
                         'resources': ['PostgreSQL Tutorial', 'MongoDB University']}
                    ]
                },
                {
                    'level': 'Advanced', 'duration': '5-7 months',
                    'steps': [
                        {'title': 'System Design', 'skills': ['Architecture', 'Scalability', 'Microservices'],
                         'resources': ['System Design Primer', 'Grokking System Design']},
                        {'title': 'DevOps & Cloud', 'skills': ['Docker', 'Kubernetes', 'CI/CD'],
                         'resources': ['Docker Mastery', 'Kubernetes documentation']},
                        {'title': 'Advanced Patterns', 'skills': ['Design Patterns', 'Clean Code'],
                         'resources': ['Design Patterns Book', 'Clean Code Book']}
                    ]
                }
            ],
            'Full Stack Developer': [
                {
                    'level': 'Beginner', 'duration': '3-4 months',
                    'steps': [
                        {'title': 'Frontend Basics', 'skills': ['HTML', 'CSS', 'JavaScript'],
                         'resources': ['FreeCodeCamp', 'JavaScript.info']},
                        {'title': 'Backend Language', 'skills': ['Node.js/Python/Java'],
                         'resources': ['Node.js docs', 'Python.org']},
                        {'title': 'Database Fundamentals', 'skills': ['SQL basics'],
                         'resources': ['SQLBolt', 'PostgreSQL Tutorial']}
                    ]
                },
                {
                    'level': 'Intermediate', 'duration': '5-6 months',
                    'steps': [
                        {'title': 'Frontend Framework', 'skills': ['React/Angular/Vue'],
                         'resources': ['React docs', 'Scrimba React']},
                        {'title': 'Backend Framework', 'skills': ['Express/Django/Spring'],
                         'resources': ['Official documentation', 'Udemy']},
                        {'title': 'REST APIs', 'skills': ['API design', 'Authentication'],
                         'resources': ['REST API Tutorial', 'JWT documentation']}
                    ]
                },
                {
                    'level': 'Advanced', 'duration': '6-8 months',
                    'steps': [
                        {'title': 'State Management', 'skills': ['Redux', 'Context API', 'MobX'],
                         'resources': ['Redux docs', 'State management tutorials']},
                        {'title': 'Testing', 'skills': ['Jest', 'Cypress', 'Unit Testing'],
                         'resources': ['Testing Library', 'Cypress docs']},
                        {'title': 'Deployment & DevOps', 'skills': ['Docker', 'AWS/Heroku', 'CI/CD'],
                         'resources': ['Docker docs', 'AWS tutorials']}
                    ]
                }
            ],
            'DevOps Engineer': [
                {
                    'level': 'Beginner', 'duration': '2-3 months',
                    'steps': [
                        {'title': 'Linux Fundamentals', 'skills': ['Linux', 'Bash', 'Command Line'],
                         'resources': ['Linux Journey', 'Ubuntu tutorials']},
                        {'title': 'Networking Basics', 'skills': ['TCP/IP', 'DNS', 'HTTP'],
                         'resources': ['Networking courses', 'CompTIA Network+']},
                        {'title': 'Git & Version Control', 'skills': ['Git', 'GitHub'],
                         'resources': ['Git documentation', 'GitHub Learning']}
                    ]
                },
                {
                    'level': 'Intermediate', 'duration': '4-6 months',
                    'steps': [
                        {'title': 'Containerization', 'skills': ['Docker', 'Docker Compose'],
                         'resources': ['Docker Mastery', 'Docker docs']},
                        {'title': 'CI/CD', 'skills': ['Jenkins', 'GitLab CI', 'GitHub Actions'],
                         'resources': ['Jenkins tutorial', 'CI/CD courses']},
                        {'title': 'Cloud Platform', 'skills': ['AWS/Azure/GCP basics'],
                         'resources': ['AWS Free Tier', 'Cloud training']}
                    ]
                },
                {
                    'level': 'Advanced', 'duration': '6-8 months',
                    'steps': [
                        {'title': 'Kubernetes', 'skills': ['K8s', 'Helm', 'Service Mesh'],
                         'resources': ['Kubernetes.io', 'CKA certification']},
                        {'title': 'Infrastructure as Code', 'skills': ['Terraform', 'Ansible'],
                         'resources': ['Terraform docs', 'Ansible tutorials']},
                        {'title': 'Monitoring & Logging', 'skills': ['Prometheus', 'Grafana', 'ELK'],
                         'resources': ['Monitoring courses', 'Grafana tutorials']}
                    ]
                }
            ],
            'Mobile Developer': [
                {
                    'level': 'Beginner', 'duration': '3-4 months',
                    'steps': [
                        {'title': 'Choose Platform', 'skills': ['Android (Kotlin)/iOS (Swift)'],
                         'resources': ['Android Basics', 'Swift Playgrounds']},
                        {'title': 'Programming Language', 'skills': ['Kotlin/Swift fundamentals'],
                         'resources': ['Kotlin Koans', 'Swift documentation']},
                        {'title': 'UI Basics', 'skills': ['XML/SwiftUI', 'Layouts'],
                         'resources': ['Android UI guide', 'SwiftUI tutorials']}
                    ]
                },
                {
                    'level': 'Intermediate', 'duration': '4-6 months',
                    'steps': [
                        {'title': 'App Architecture', 'skills': ['MVVM', 'Clean Architecture'],
                         'resources': ['Architecture Components', 'iOS patterns']},
                        {'title': 'Networking', 'skills': ['REST APIs', 'JSON', 'Retrofit/Alamofire'],
                         'resources': ['Networking tutorials', 'API integration']},
                        {'title': 'Local Storage', 'skills': ['Room/Core Data', 'SQLite'],
                         'resources': ['Database tutorials', 'Storage guides']}
                    ]
                },
                {
                    'level': 'Advanced', 'duration': '5-7 months',
                    'steps': [
                        {'title': 'Advanced UI', 'skills': ['Custom Views', 'Animations'],
                         'resources': ['UI/UX courses', 'Animation guides']},
                        {'title': 'Testing', 'skills': ['Unit Testing', 'UI Testing'],
                         'resources': ['JUnit', 'XCTest', 'Espresso']},
                        {'title': 'Publishing', 'skills': ['Play Store/App Store deployment'],
                         'resources': ['Publishing guides', 'App Store guidelines']}
                    ]
                }
            ],
            'Data Analyst': [
                {
                    'level': 'Beginner', 'duration': '2-3 months',
                    'steps': [
                        {'title': 'Excel Mastery', 'skills': ['Excel', 'Pivot Tables', 'Formulas'],
                         'resources': ['Excel tutorials', 'Microsoft Learn']},
                        {'title': 'SQL Fundamentals', 'skills': ['SQL', 'Queries', 'Joins'],
                         'resources': ['Mode Analytics', 'SQLZoo']},
                        {'title': 'Statistics Basics', 'skills': ['Descriptive Statistics', 'Probability'],
                         'resources': ['Khan Academy', 'Statistics courses']}
                    ]
                },
                {
                    'level': 'Intermediate', 'duration': '3-5 months',
                    'steps': [
                        {'title': 'Data Visualization', 'skills': ['Tableau', 'Power BI'],
                         'resources': ['Tableau Public', 'Power BI tutorials']},
                        {'title': 'Python for Analysis', 'skills': ['Pandas', 'NumPy', 'Matplotlib'],
                         'resources': ['DataCamp', 'Kaggle Learn']},
                        {'title': 'Business Intelligence', 'skills': ['KPIs', 'Dashboards', 'Reporting'],
                         'resources': ['BI courses', 'Analytics tutorials']}
                    ]
                },
                {
                    'level': 'Advanced', 'duration': '4-6 months',
                    'steps': [
                        {'title': 'Advanced Analytics', 'skills': ['Statistical Analysis', 'A/B Testing'],
                         'resources': ['Statistics courses', 'Experimentation']},
                        {'title': 'Machine Learning Basics', 'skills': ['Predictive modeling', 'ML basics'],
                         'resources': ['ML for analysts', 'Scikit-learn']},
                        {'title': 'Big Data Tools', 'skills': ['Spark', 'Cloud platforms'],
                         'resources': ['Spark tutorials', 'Cloud training']}
                    ]
                }
            ]
        }
    
    def generate_roadmap(self, career: str, current_level: str = 'Beginner') -> Dict[str, Any]:
        """
        Generate a personalized career roadmap.
        
        Args:
            career (str): Target career
            current_level (str): Current skill level
            
        Returns:
            Dict[str, Any]: Career roadmap
        """
        if career not in self.roadmaps:
            return self._get_default_roadmap(career)
        
        roadmap_data = self.roadmaps[career]
        
        # Determine starting point
        level_order = ['Beginner', 'Intermediate', 'Advanced']
        start_index = level_order.index(current_level) if current_level in level_order else 0
        
        # Build roadmap
        total_duration_months = 0
        relevant_levels = roadmap_data[start_index:]
        
        for level_data in relevant_levels:
            duration_str = level_data['duration']
            # Extract max months from "X-Y months"
            max_months = int(duration_str.split('-')[1].split()[0])
            total_duration_months += max_months
        
        # Collect all skills
        all_skills = []
        for level_data in relevant_levels:
            for step in level_data['steps']:
                all_skills.extend(step['skills'])
        
        result = {
            'career': career,
            'current_level': current_level,
            'total_duration': f"{total_duration_months} months",
            'total_steps': sum(len(level['steps']) for level in relevant_levels),
            'skills_to_learn': list(set(all_skills)),
            'roadmap': relevant_levels,
            'milestones': self._generate_milestones(relevant_levels),
            'tips': self._get_career_tips(career)
        }
        
        return result
    
    def _generate_milestones(self, levels: List[Dict[str, Any]]) -> List[str]:
        """Generate milestone achievements."""
        milestones = []
        
        if len(levels) >= 1:
            milestones.append("Complete foundational skills")
        if len(levels) >= 2:
            milestones.append("Build 2-3 portfolio projects")
        if len(levels) >= 2:
            milestones.append("Start applying for entry-level positions")
        if len(levels) >= 3:
            milestones.append("Obtain relevant certification")
        if len(levels) >= 3:
            milestones.append("Contribute to open-source projects")
        
        return milestones
    
    def _get_career_tips(self, career: str) -> List[str]:
        """Get career-specific tips."""
        tips = {
            'Data Scientist': [
                "Build a portfolio on Kaggle and GitHub",
                "Work on real-world datasets",
                "Stay updated with latest ML research papers",
                "Network with data science professionals"
            ],
            'Software Developer': [
                "Contribute to open-source projects",
                "Build personal projects and showcase on GitHub",
                "Practice coding problems daily",
                "Participate in hackathons"
            ],
            'Full Stack Developer': [
                "Build full-stack applications from scratch",
                "Learn both SQL and NoSQL databases",
                "Focus on responsive design principles",
                "Deploy projects to cloud platforms"
            ],
            'DevOps Engineer': [
                "Get hands-on with cloud platforms",
                "Automate everything you can",
                "Learn about security best practices",
                "Contribute to DevOps tools and communities"
            ],
            'Mobile Developer': [
                "Publish apps to Play Store/App Store",
                "Follow platform design guidelines",
                "Optimize for performance and battery life",
                "Keep up with platform updates"
            ],
            'Data Analyst': [
                "Build dashboards for real problems",
                "Learn to tell stories with data",
                "Understand business metrics and KPIs",
                "Practice presenting insights to stakeholders"
            ]
        }
        
        return tips.get(career, [
            "Build a strong portfolio",
            "Network with professionals in your field",
            "Stay updated with industry trends",
            "Obtain relevant certifications"
        ])
    
    def _get_default_roadmap(self, career: str) -> Dict[str, Any]:
        """Return a default roadmap for unknown careers."""
        return {
            'career': career,
            'current_level': 'Unknown',
            'total_duration': 'Varies',
            'total_steps': 0,
            'skills_to_learn': [],
            'roadmap': [],
            'milestones': [],
            'tips': ["Research this career path", "Find online resources", "Connect with professionals in this field"],
            'message': 'Roadmap not available for this career. Please check back later.'
        }
    
    def get_available_careers(self) -> List[str]:
        """Get list of careers with available roadmaps."""
        return list(self.roadmaps.keys())


def main():
    """Test career roadmap generator."""
    generator = CareerRoadmapGenerator()
    
    print("="*70)
    print("Career Roadmap Generator - Test")
    print("="*70)
    
    # Test roadmap generation
    test_career = 'Data Scientist'
    print(f"\nGenerating roadmap for: {test_career}")
    print("-"*70)
    
    roadmap = generator.generate_roadmap(test_career, 'Beginner')
    
    print(f"\nCareer: {roadmap['career']}")
    print(f"Total Duration: {roadmap['total_duration']}")
    print(f"Total Steps: {roadmap['total_steps']}")
    print(f"Skills to Learn: {len(roadmap['skills_to_learn'])} skills")
    
    print(f"\nLearning Path:")
    for i, level in enumerate(roadmap['roadmap'], 1):
        print(f"\n  Level {i}: {level['level']} ({level['duration']})")
        for j, step in enumerate(level['steps'], 1):
            print(f"    {j}. {step['title']}")
            print(f"       Skills: {', '.join(step['skills'])}")
    
    print(f"\nMilestones:")
    for i, milestone in enumerate(roadmap['milestones'], 1):
        print(f"  {i}. {milestone}")
    
    print(f"\nCareer Tips:")
    for i, tip in enumerate(roadmap['tips'], 1):
        print(f"  {i}. {tip}")
    
    print("\n" + "="*70)
    print("Available Careers:")
    print("="*70)
    for career in generator.get_available_careers():
        print(f"  - {career}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()

