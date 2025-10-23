"""
Skills Gap Analysis Module

This module analyzes the gap between user's current skills
and required skills for target career paths.
"""

import logging
from typing import Dict, List, Set, Tuple, Any
from collections import Counter
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SkillsGapAnalyzer:
    """
    Analyzes skills gap and provides recommendations for skill development.
    """
    
    def __init__(self):
        """Initialize the skills gap analyzer."""
        self.career_skill_requirements = self._load_career_requirements()
        self.learning_resources = self._load_learning_resources()
    
    def _load_career_requirements(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Load career skill requirements.
        
        Returns:
            Dict: Career skill requirements with essential and optional skills
        """
        return {
            'Data Scientist': {
                'essential': ['Python', 'SQL', 'Statistics', 'ML', 'Data Analysis'],
                'recommended': ['Deep Learning', 'NLP', 'Computer Vision', 'Big Data', 'Cloud'],
                'tools': ['Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'Tableau', 'Jupyter'],
                'certifications': ['Google Data Analytics', 'IBM Data Science', 'AWS ML Specialty']
            },
            'Machine Learning Engineer': {
                'essential': ['Python', 'ML', 'Deep Learning', 'Mathematics', 'Programming'],
                'recommended': ['MLOps', 'Docker', 'Kubernetes', 'Cloud', 'Spark'],
                'tools': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Git', 'Docker', 'Kubernetes'],
                'certifications': ['TensorFlow Developer', 'AWS ML Specialty', 'MLOps Professional']
            },
            'Software Developer': {
                'essential': ['Programming', 'Data Structures', 'Algorithms', 'OOP', 'Git'],
                'recommended': ['Design Patterns', 'Testing', 'CI/CD', 'Cloud', 'Microservices'],
                'tools': ['IDE', 'Git', 'Docker', 'Jenkins', 'JIRA'],
                'certifications': ['AWS Developer', 'Oracle Java', 'Microsoft Azure Developer']
            },
            'Full Stack Developer': {
                'essential': ['HTML', 'CSS', 'JavaScript', 'Backend Language', 'Database', 'REST API'],
                'recommended': ['React/Angular/Vue', 'Node.js', 'MongoDB', 'Docker', 'AWS'],
                'tools': ['VS Code', 'Git', 'Postman', 'Docker', 'npm/yarn'],
                'certifications': ['AWS Solutions Architect', 'React Developer', 'Node.js Certification']
            },
            'Data Analyst': {
                'essential': ['SQL', 'Excel', 'Data Analysis', 'Statistics', 'Reporting'],
                'recommended': ['Python/R', 'Power BI', 'Tableau', 'Business Intelligence'],
                'tools': ['Excel', 'SQL', 'Power BI', 'Tableau', 'Python', 'R'],
                'certifications': ['Microsoft Power BI', 'Tableau Desktop', 'Google Data Analytics']
            },
            'DevOps Engineer': {
                'essential': ['Linux', 'Docker', 'Kubernetes', 'CI/CD', 'Cloud', 'Scripting'],
                'recommended': ['Terraform', 'Ansible', 'Monitoring', 'Security', 'Networking'],
                'tools': ['Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'Terraform', 'Ansible'],
                'certifications': ['AWS DevOps', 'Kubernetes CKA', 'Docker Certified']
            },
            'Cloud Engineer': {
                'essential': ['Cloud Platform', 'Networking', 'Security', 'Linux', 'Scripting'],
                'recommended': ['Terraform', 'Docker', 'Kubernetes', 'Serverless', 'DevOps'],
                'tools': ['AWS/Azure/GCP', 'Terraform', 'Docker', 'CLI Tools'],
                'certifications': ['AWS Solutions Architect', 'Azure Administrator', 'GCP Professional']
            },
            'Web Developer': {
                'essential': ['HTML', 'CSS', 'JavaScript', 'Responsive Design', 'Git'],
                'recommended': ['React/Vue/Angular', 'TypeScript', 'Webpack', 'Testing'],
                'tools': ['VS Code', 'Git', 'Chrome DevTools', 'npm', 'Webpack'],
                'certifications': ['JavaScript Developer', 'React Developer', 'Web Design Professional']
            },
            'Mobile Developer': {
                'essential': ['Mobile Platform', 'Programming', 'UI/UX', 'APIs', 'Git'],
                'recommended': ['Cross-platform', 'Firebase', 'App Store Deployment', 'Testing'],
                'tools': ['Android Studio/Xcode', 'Git', 'Firebase', 'Postman'],
                'certifications': ['Android Developer', 'iOS Developer', 'Flutter Developer']
            },
            'Cybersecurity Analyst': {
                'essential': ['Network Security', 'Linux', 'Security Tools', 'Threat Analysis'],
                'recommended': ['Penetration Testing', 'Python', 'Cloud Security', 'Compliance'],
                'tools': ['Wireshark', 'Metasploit', 'Nmap', 'Burp Suite', 'Kali Linux'],
                'certifications': ['CEH', 'CISSP', 'CompTIA Security+', 'OSCP']
            },
            'AI Engineer': {
                'essential': ['Python', 'ML', 'Deep Learning', 'Neural Networks', 'Mathematics'],
                'recommended': ['NLP', 'Computer Vision', 'Reinforcement Learning', 'MLOps'],
                'tools': ['TensorFlow', 'PyTorch', 'Keras', 'Jupyter', 'Docker'],
                'certifications': ['TensorFlow Developer', 'AWS ML', 'AI Engineering Professional']
            },
            'Business Analyst': {
                'essential': ['Business Analysis', 'Requirements Gathering', 'Documentation', 'SQL'],
                'recommended': ['Agile', 'Power BI', 'Process Modeling', 'Stakeholder Management'],
                'tools': ['JIRA', 'Confluence', 'Visio', 'Excel', 'Power BI'],
                'certifications': ['CBAP', 'PMI-PBA', 'Agile BA', 'IIBA Certifications']
            },
            'Product Manager': {
                'essential': ['Product Strategy', 'User Research', 'Agile', 'Analytics', 'Communication'],
                'recommended': ['SQL', 'A/B Testing', 'Design Thinking', 'Roadmapping'],
                'tools': ['JIRA', 'Confluence', 'Figma', 'Google Analytics', 'Mixpanel'],
                'certifications': ['Product Management', 'Agile Product Owner', 'Product Analytics']
            },
            'UI/UX Developer': {
                'essential': ['HTML', 'CSS', 'JavaScript', 'Design Principles', 'User Research'],
                'recommended': ['React/Vue', 'Design Systems', 'Accessibility', 'Animation'],
                'tools': ['Figma', 'Adobe XD', 'Sketch', 'VS Code', 'Git'],
                'certifications': ['Google UX Design', 'Nielsen Norman UX', 'Adobe Certified']
            },
            'Database Administrator': {
                'essential': ['SQL', 'Database Design', 'Performance Tuning', 'Backup/Recovery'],
                'recommended': ['NoSQL', 'Replication', 'High Availability', 'Cloud Databases'],
                'tools': ['Oracle/MySQL/PostgreSQL', 'Monitoring Tools', 'Backup Tools'],
                'certifications': ['Oracle DBA', 'Microsoft SQL Server', 'PostgreSQL Certified']
            },
            'QA Engineer': {
                'essential': ['Testing', 'Test Automation', 'Bug Tracking', 'Quality Assurance'],
                'recommended': ['Selenium', 'Cypress', 'API Testing', 'Performance Testing'],
                'tools': ['Selenium', 'JIRA', 'Postman', 'JUnit/TestNG', 'Git'],
                'certifications': ['ISTQB', 'Selenium Testing', 'Agile Tester']
            },
            'Blockchain Developer': {
                'essential': ['Blockchain', 'Solidity', 'Smart Contracts', 'Cryptography'],
                'recommended': ['Web3', 'DApps', 'Ethereum', 'Security'],
                'tools': ['Truffle', 'Hardhat', 'MetaMask', 'Remix', 'Web3.js'],
                'certifications': ['Blockchain Developer', 'Ethereum Developer', 'Hyperledger']
            },
            'Game Developer': {
                'essential': ['Programming', 'Game Engine', 'Game Design', '3D/2D Graphics'],
                'recommended': ['Physics', 'AI', 'Multiplayer', 'Optimization'],
                'tools': ['Unity', 'Unreal Engine', 'Blender', 'Git'],
                'certifications': ['Unity Certified', 'Unreal Engine Developer']
            },
            'Network Engineer': {
                'essential': ['Networking', 'Routing', 'Switching', 'Firewall', 'Troubleshooting'],
                'recommended': ['Security', 'VPN', 'Load Balancing', 'SD-WAN', 'Automation'],
                'tools': ['Cisco', 'Wireshark', 'Network Monitoring Tools'],
                'certifications': ['CCNA', 'CCNP', 'Network+', 'JNCIA']
            },
            'System Administrator': {
                'essential': ['Linux', 'Windows Server', 'Networking', 'Security', 'Scripting'],
                'recommended': ['Virtualization', 'Docker', 'Monitoring', 'Backup', 'Automation'],
                'tools': ['PowerShell', 'Bash', 'VMware', 'Active Directory', 'Monitoring Tools'],
                'certifications': ['RHCSA', 'Microsoft MCSA', 'Linux+', 'AWS SysOps']
            }
        }
    
    def _load_learning_resources(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Load learning resources for skills.
        
        Returns:
            Dict: Learning resources for each skill
        """
        return {
            'Python': [
                {'name': 'Python for Everybody', 'platform': 'Coursera', 'level': 'Beginner'},
                {'name': 'Complete Python Bootcamp', 'platform': 'Udemy', 'level': 'Beginner'},
                {'name': 'Python Documentation', 'platform': 'python.org', 'level': 'All'}
            ],
            'SQL': [
                {'name': 'SQL for Data Science', 'platform': 'Coursera', 'level': 'Beginner'},
                {'name': 'The Complete SQL Bootcamp', 'platform': 'Udemy', 'level': 'Beginner'}
            ],
            'ML': [
                {'name': 'Machine Learning by Andrew Ng', 'platform': 'Coursera', 'level': 'Intermediate'},
                {'name': 'Applied ML', 'platform': 'Coursera', 'level': 'Advanced'}
            ],
            'Deep Learning': [
                {'name': 'Deep Learning Specialization', 'platform': 'Coursera', 'level': 'Advanced'},
                {'name': 'Fast.ai Practical Deep Learning', 'platform': 'fast.ai', 'level': 'Intermediate'}
            ],
            'JavaScript': [
                {'name': 'JavaScript: The Complete Guide', 'platform': 'Udemy', 'level': 'Beginner'},
                {'name': 'JavaScript30', 'platform': 'javascript30.com', 'level': 'Intermediate'}
            ],
            'React': [
                {'name': 'React - The Complete Guide', 'platform': 'Udemy', 'level': 'Intermediate'},
                {'name': 'React Documentation', 'platform': 'react.dev', 'level': 'All'}
            ],
            'Docker': [
                {'name': 'Docker Mastery', 'platform': 'Udemy', 'level': 'Beginner'},
                {'name': 'Docker Documentation', 'platform': 'docker.com', 'level': 'All'}
            ],
            'Kubernetes': [
                {'name': 'Kubernetes for Beginners', 'platform': 'Udemy', 'level': 'Beginner'},
                {'name': 'CKA Certification Course', 'platform': 'Linux Foundation', 'level': 'Advanced'}
            ],
            'AWS': [
                {'name': 'AWS Certified Solutions Architect', 'platform': 'A Cloud Guru', 'level': 'Intermediate'},
                {'name': 'AWS Free Tier', 'platform': 'AWS', 'level': 'All'}
            ],
            'Cloud': [
                {'name': 'Cloud Computing Basics', 'platform': 'Coursera', 'level': 'Beginner'},
                {'name': 'Multi-Cloud Architecture', 'platform': 'Pluralsight', 'level': 'Advanced'}
            ]
        }
    
    def analyze_skills_gap(self, user_skills: List[str], target_career: str) -> Dict[str, Any]:
        """
        Analyze the gap between user's skills and career requirements.
        
        Args:
            user_skills (List[str]): List of user's current skills
            target_career (str): Target career path
            
        Returns:
            Dict[str, Any]: Skills gap analysis result
        """
        # Normalize skills
        user_skills_set = set(skill.strip().lower() for skill in user_skills)
        
        # Get career requirements
        if target_career not in self.career_skill_requirements:
            logger.warning(f"Career not found: {target_career}")
            return self._get_default_analysis()
        
        requirements = self.career_skill_requirements[target_career]
        
        # Normalize required skills
        essential_skills = set(s.lower() for s in requirements.get('essential', []))
        recommended_skills = set(s.lower() for s in requirements.get('recommended', []))
        tools = set(s.lower() for s in requirements.get('tools', []))
        
        # Calculate matches
        essential_matches = user_skills_set & essential_skills
        essential_gaps = essential_skills - user_skills_set
        
        recommended_matches = user_skills_set & recommended_skills
        recommended_gaps = recommended_skills - user_skills_set
        
        tool_matches = user_skills_set & tools
        tool_gaps = tools - user_skills_set
        
        # Calculate readiness score
        essential_score = (len(essential_matches) / len(essential_skills) * 100) if essential_skills else 100
        recommended_score = (len(recommended_matches) / len(recommended_skills) * 100) if recommended_skills else 100
        tool_score = (len(tool_matches) / len(tools) * 100) if tools else 100
        
        overall_readiness = (
            essential_score * 0.5 +
            recommended_score * 0.3 +
            tool_score * 0.2
        )
        
        # Get learning recommendations
        priority_skills = list(essential_gaps)[:5]  # Top 5 essential gaps
        learning_recommendations = self._get_learning_recommendations(priority_skills)
        
        # Get certifications
        certifications = requirements.get('certifications', [])
        
        # Estimate time to readiness
        total_gaps = len(essential_gaps) + len(recommended_gaps)
        estimated_months = self._estimate_learning_time(total_gaps)
        
        result = {
            'target_career': target_career,
            'overall_readiness': round(overall_readiness, 2),
            'readiness_level': self._get_readiness_level(overall_readiness),
            'skills_analysis': {
                'essential_skills': {
                    'required': list(essential_skills),
                    'matched': list(essential_matches),
                    'gaps': list(essential_gaps),
                    'score': round(essential_score, 2)
                },
                'recommended_skills': {
                    'required': list(recommended_skills),
                    'matched': list(recommended_matches),
                    'gaps': list(recommended_gaps),
                    'score': round(recommended_score, 2)
                },
                'tools': {
                    'required': list(tools),
                    'matched': list(tool_matches),
                    'gaps': list(tool_gaps),
                    'score': round(tool_score, 2)
                }
            },
            'priority_skills_to_learn': priority_skills,
            'learning_recommendations': learning_recommendations,
            'certifications': certifications,
            'estimated_time_to_readiness': estimated_months,
            'next_steps': self._generate_next_steps(essential_gaps, recommended_gaps, overall_readiness)
        }
        
        return result
    
    def _get_readiness_level(self, score: float) -> str:
        """Get readiness level based on score."""
        if score >= 80:
            return "Ready - You meet most requirements!"
        elif score >= 60:
            return "Nearly Ready - A few gaps to fill"
        elif score >= 40:
            return "Moderate - Significant learning needed"
        else:
            return "Beginner - Start with essentials"
    
    def _estimate_learning_time(self, total_gaps: int) -> str:
        """Estimate time needed to fill skill gaps."""
        if total_gaps == 0:
            return "You're ready!"
        elif total_gaps <= 3:
            return "1-2 months of focused learning"
        elif total_gaps <= 6:
            return "3-4 months of dedicated study"
        elif total_gaps <= 10:
            return "6-9 months with consistent effort"
        else:
            return "12+ months for comprehensive preparation"
    
    def _get_learning_recommendations(self, skills: List[str]) -> List[Dict[str, Any]]:
        """Get learning resources for skills."""
        recommendations = []
        
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower in self.learning_resources:
                recommendations.append({
                    'skill': skill,
                    'resources': self.learning_resources[skill_lower]
                })
            else:
                recommendations.append({
                    'skill': skill,
                    'resources': [
                        {'name': f'{skill} Tutorial', 'platform': 'YouTube', 'level': 'Beginner'},
                        {'name': f'{skill} Documentation', 'platform': 'Official Docs', 'level': 'All'}
                    ]
                })
        
        return recommendations
    
    def _generate_next_steps(self, essential_gaps: Set[str], 
                            recommended_gaps: Set[str], readiness: float) -> List[str]:
        """Generate actionable next steps."""
        steps = []
        
        if readiness >= 80:
            steps.append("Start applying for jobs! You're well-prepared.")
            steps.append("Work on personal projects to showcase your skills")
            steps.append("Prepare for technical interviews")
        elif readiness >= 60:
            steps.append("Focus on filling the essential skill gaps")
            steps.append("Build projects using the required skills")
            steps.append("Consider online courses for missing skills")
        else:
            steps.append("Start with the essential skills first")
            steps.append("Take beginner-friendly courses")
            steps.append("Practice with small projects")
            steps.append("Join online communities for support")
        
        if essential_gaps:
            top_gap = list(essential_gaps)[0]
            steps.insert(0, f"Priority: Learn {top_gap} - it's essential for this career")
        
        return steps
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Return default analysis when career not found."""
        return {
            'target_career': 'Unknown',
            'overall_readiness': 0,
            'readiness_level': 'Career not found in database',
            'skills_analysis': {},
            'priority_skills_to_learn': [],
            'learning_recommendations': [],
            'certifications': [],
            'estimated_time_to_readiness': 'Unknown',
            'next_steps': ['Please select a valid career path']
        }
    
    def compare_multiple_careers(self, user_skills: List[str], 
                                careers: List[str]) -> List[Dict[str, Any]]:
        """
        Compare readiness for multiple careers.
        
        Args:
            user_skills (List[str]): User's current skills
            careers (List[str]): List of careers to compare
            
        Returns:
            List[Dict[str, Any]]: Comparison results sorted by readiness
        """
        results = []
        
        for career in careers:
            analysis = self.analyze_skills_gap(user_skills, career)
            results.append({
                'career': career,
                'readiness': analysis['overall_readiness'],
                'readiness_level': analysis['readiness_level'],
                'essential_gaps': len(analysis['skills_analysis'].get('essential_skills', {}).get('gaps', [])),
                'estimated_time': analysis['estimated_time_to_readiness']
            })
        
        # Sort by readiness score
        results.sort(key=lambda x: x['readiness'], reverse=True)
        
        return results


def main():
    """Test skills gap analyzer."""
    analyzer = SkillsGapAnalyzer()
    
    # Test case 1: Data Scientist
    print("="*70)
    print("Skills Gap Analysis - Data Scientist")
    print("="*70)
    
    user_skills = ['Python', 'SQL', 'Excel', 'Statistics']
    analysis = analyzer.analyze_skills_gap(user_skills, 'Data Scientist')
    
    print(f"\nOverall Readiness: {analysis['overall_readiness']}%")
    print(f"Readiness Level: {analysis['readiness_level']}")
    print(f"\nEssential Skills Score: {analysis['skills_analysis']['essential_skills']['score']}%")
    print(f"Matched: {', '.join(analysis['skills_analysis']['essential_skills']['matched'])}")
    print(f"Gaps: {', '.join(analysis['skills_analysis']['essential_skills']['gaps'])}")
    print(f"\nPriority Skills to Learn: {', '.join(analysis['priority_skills_to_learn'])}")
    print(f"Estimated Time: {analysis['estimated_time_to_readiness']}")
    print(f"\nNext Steps:")
    for i, step in enumerate(analysis['next_steps'], 1):
        print(f"  {i}. {step}")
    
    # Test case 2: Compare multiple careers
    print("\n\n" + "="*70)
    print("Career Comparison")
    print("="*70)
    
    careers_to_compare = ['Data Scientist', 'Data Analyst', 'Machine Learning Engineer']
    comparison = analyzer.compare_multiple_careers(user_skills, careers_to_compare)
    
    print(f"\nBest Career Matches (based on current skills):\n")
    for i, result in enumerate(comparison, 1):
        print(f"{i}. {result['career']}")
        print(f"   Readiness: {result['readiness']}% - {result['readiness_level']}")
        print(f"   Essential Gaps: {result['essential_gaps']}")
        print(f"   Estimated Time: {result['estimated_time']}\n")


if __name__ == "__main__":
    main()

