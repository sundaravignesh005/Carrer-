"""
Data Augmentation Script for Career Dataset

This script expands the career dataset from 100 to 1000 samples
using intelligent data augmentation techniques.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database import DatabaseManager
import pandas as pd
import numpy as np
import random
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Extended skill sets for different career paths
CAREER_SKILLS_MAP = {
    'Data Scientist': [
        'Python,SQL,Statistics,ML,Deep Learning',
        'Python,R,Statistics,ML,Tableau',
        'Python,SQL,ML,NLP,Computer Vision',
        'Python,Spark,SQL,ML,Big Data',
        'Python,TensorFlow,Keras,ML,Statistics',
        'R,Python,Statistics,ML,Data Visualization',
        'Python,SQL,ML,AWS,Docker',
        'Python,Pandas,NumPy,Scikit-learn,ML'
    ],
    'Machine Learning Engineer': [
        'Python,TensorFlow,Keras,ML,Deep Learning',
        'Python,PyTorch,ML,Deep Learning,Docker',
        'Python,ML,Deep Learning,Kubernetes,MLOps',
        'Python,TensorFlow,ML,Cloud,AWS',
        'Python,Spark,ML,Scala,Big Data',
        'Python,ML,Deep Learning,NLP,Computer Vision',
        'C++,Python,ML,Deep Learning,Optimization',
        'Python,ML,Deep Learning,Edge Computing,IoT'
    ],
    'Software Developer': [
        'Java,Spring Boot,MySQL,REST API',
        'Python,Django,PostgreSQL,REST API',
        'JavaScript,Node.js,MongoDB,React',
        'C#,.NET,SQL Server,Azure',
        'Java,Microservices,Docker,Kubernetes',
        'Python,Flask,SQLAlchemy,Redis',
        'Go,PostgreSQL,Docker,Microservices',
        'Ruby,Rails,PostgreSQL,Redis'
    ],
    'Data Analyst': [
        'Python,SQL,Excel,Tableau,Power BI',
        'R,SQL,Statistics,Tableau,Excel',
        'Python,SQL,Power BI,Statistics',
        'SQL,Excel,Power BI,Data Visualization',
        'Python,Pandas,SQL,Tableau,Statistics',
        'R,SQL,ggplot2,Statistics,Excel',
        'Python,SQL,Looker,Statistics',
        'SQL,Excel,Tableau,Statistics,Business Intelligence'
    ],
    'Web Developer': [
        'HTML,CSS,JavaScript,React,Node.js',
        'HTML,CSS,JavaScript,Angular,TypeScript',
        'HTML,CSS,JavaScript,Vue.js,Firebase',
        'HTML,CSS,JavaScript,React,Redux',
        'HTML,CSS,JavaScript,Svelte,Node.js',
        'PHP,MySQL,JavaScript,WordPress,CSS',
        'HTML,CSS,JavaScript,Next.js,React',
        'HTML,CSS,JavaScript,jQuery,Bootstrap'
    ],
    'Full Stack Developer': [
        'React,Node.js,MongoDB,Express,JavaScript',
        'Angular,Node.js,PostgreSQL,TypeScript',
        'Vue.js,Python,Django,PostgreSQL,Docker',
        'React,Python,Flask,MySQL,Redis',
        'Angular,Java,Spring Boot,MySQL',
        'React,Node.js,GraphQL,PostgreSQL,Docker',
        'Vue.js,Node.js,MongoDB,Express',
        'React,Django,PostgreSQL,Redis,Docker'
    ],
    'DevOps Engineer': [
        'Docker,Kubernetes,AWS,CI/CD,Terraform',
        'Docker,Kubernetes,Azure,Jenkins,Ansible',
        'AWS,Terraform,Docker,Python,Linux',
        'Kubernetes,Docker,GCP,CI/CD,Python',
        'Jenkins,Docker,AWS,Terraform,Monitoring',
        'GitLab CI,Docker,Kubernetes,AWS,Python',
        'Azure DevOps,Docker,Kubernetes,PowerShell',
        'Docker,Kubernetes,AWS,Python,CloudFormation'
    ],
    'Cloud Engineer': [
        'AWS,Terraform,Docker,Python,Linux',
        'Azure,PowerShell,Docker,Kubernetes',
        'GCP,Terraform,Kubernetes,Python',
        'AWS,CloudFormation,Lambda,Python,S3',
        'Azure,ARM Templates,PowerShell,Docker',
        'AWS,Serverless,Lambda,Python,DynamoDB',
        'GCP,Kubernetes,Docker,Python,Cloud Functions',
        'Multi-Cloud,Terraform,Docker,Python,Ansible'
    ],
    'Mobile Developer': [
        'Java,Kotlin,Android,Firebase,REST API',
        'Swift,iOS,Xcode,Firebase,REST API',
        'Flutter,Dart,Firebase,REST API',
        'React Native,JavaScript,Firebase,Redux',
        'Kotlin,Android,Jetpack,Room,Retrofit',
        'Swift,iOS,SwiftUI,CoreData,Alamofire',
        'Flutter,Dart,Provider,SQLite,HTTP',
        'React Native,TypeScript,Redux,AsyncStorage'
    ],
    'UI/UX Developer': [
        'HTML,CSS,JavaScript,React,Figma',
        'HTML,CSS,JavaScript,Vue.js,Adobe XD',
        'HTML,CSS,JavaScript,Angular,Sketch',
        'React,CSS,JavaScript,Figma,Design Systems',
        'HTML,CSS,JavaScript,Responsive Design,Figma',
        'Vue.js,CSS,JavaScript,Adobe XD,Animation',
        'React,Styled Components,Figma,TypeScript',
        'HTML,CSS,SASS,JavaScript,Figma,Accessibility'
    ],
    'Business Analyst': [
        'SQL,Excel,Power BI,Tableau,JIRA',
        'SQL,Excel,Business Intelligence,Requirements Analysis',
        'SQL,Power BI,Agile,Stakeholder Management',
        'Excel,SQL,Tableau,Project Management',
        'SQL,Power BI,Process Improvement,Documentation',
        'Excel,SQL,Visio,Business Process Modeling',
        'SQL,Tableau,Agile,User Stories,JIRA',
        'Power BI,SQL,Excel,Data Analysis,Reporting'
    ],
    'Cybersecurity Analyst': [
        'Network Security,Python,Linux,Penetration Testing',
        'Security Auditing,Python,Wireshark,Kali Linux',
        'Ethical Hacking,Python,Linux,SIEM,Firewall',
        'Network Security,Cryptography,Python,IDS/IPS',
        'Python,Linux,Security Tools,Incident Response',
        'Penetration Testing,Python,Metasploit,Nmap',
        'Security Operations,Python,SIEM,Threat Intelligence',
        'Application Security,Python,OWASP,Burp Suite'
    ],
    'Database Administrator': [
        'Oracle,SQL,PL/SQL,Database Tuning,Backup',
        'SQL Server,T-SQL,Performance Tuning,SSIS',
        'MySQL,SQL,Database Design,Replication',
        'PostgreSQL,SQL,Query Optimization,pgAdmin',
        'MongoDB,NoSQL,Database Design,Sharding',
        'Oracle,SQL,RAC,Data Guard,Backup Recovery',
        'SQL Server,T-SQL,Always On,Performance',
        'MySQL,MariaDB,SQL,Clustering,Backup'
    ],
    'Game Developer': [
        'Unity,C#,Game Design,3D Modeling',
        'Unreal Engine,C++,Blueprint,Game Design',
        'Unity,C#,Multiplayer,Game Physics',
        'Unreal Engine,C++,VR,Game Design',
        'Unity,C#,Mobile Games,Monetization',
        'Godot,GDScript,2D Games,Game Design',
        'Unity,C#,AR,Mobile Development',
        'Unreal Engine,C++,AAA Games,Optimization'
    ],
    'AI Engineer': [
        'Python,TensorFlow,NLP,Deep Learning,ML',
        'Python,PyTorch,Computer Vision,Deep Learning',
        'Python,NLP,Transformers,Deep Learning,ML',
        'Python,Reinforcement Learning,TensorFlow,ML',
        'Python,Computer Vision,OpenCV,Deep Learning',
        'Python,NLP,BERT,GPT,Deep Learning',
        'Python,ML,Deep Learning,Model Deployment,MLOps',
        'Python,TensorFlow,Keras,Neural Networks,AI'
    ],
    'Blockchain Developer': [
        'Solidity,Ethereum,Web3.js,Smart Contracts',
        'Solidity,Blockchain,Truffle,Hardhat',
        'Rust,Solana,Blockchain,Smart Contracts',
        'JavaScript,Ethereum,Web3,DApps,Solidity',
        'Go,Hyperledger,Blockchain,Smart Contracts',
        'Solidity,Ethereum,React,Web3.js,IPFS',
        'Python,Blockchain,Cryptography,Smart Contracts',
        'C++,Bitcoin,Blockchain,Cryptography'
    ],
    'Network Engineer': [
        'Cisco,Routing,Switching,Firewall,VPN',
        'Network Administration,Cisco,TCP/IP,Routing',
        'Cisco,CCNA,Network Security,Troubleshooting',
        'Juniper,Routing,Switching,Network Design',
        'Cisco,Load Balancing,Firewall,VPN,Network Security',
        'Network Design,Cisco,WAN,LAN,Protocols',
        'Cisco,SD-WAN,Network Automation,Python',
        'Network Security,Firewall,IDS/IPS,Cisco,VPN'
    ],
    'QA Engineer': [
        'Selenium,Java,Test Automation,JIRA',
        'Python,Selenium,Test Automation,CI/CD',
        'Manual Testing,Automation,Selenium,TestNG',
        'Cypress,JavaScript,Test Automation,Agile',
        'Selenium,Python,API Testing,Postman',
        'Java,JUnit,Selenium,Test Automation,Maven',
        'JavaScript,Jest,Cypress,Test Automation,React',
        'Python,Pytest,Selenium,API Testing,CI/CD'
    ],
    'Product Manager': [
        'Product Strategy,Agile,JIRA,Roadmapping,Analytics',
        'Product Management,User Research,Agile,Data Analysis',
        'Agile,Scrum,Product Roadmap,Stakeholder Management',
        'Product Strategy,Market Research,Analytics,A/B Testing',
        'Agile,Product Development,User Stories,JIRA',
        'Product Management,Go-to-Market,Analytics,SQL',
        'Agile,Product Roadmap,Customer Research,Metrics',
        'Product Strategy,Competitive Analysis,Agile,SQL'
    ],
    'System Administrator': [
        'Linux,Windows Server,Bash,PowerShell,Active Directory',
        'Linux,VMware,Docker,Networking,Scripting',
        'Windows Server,Active Directory,PowerShell,Group Policy',
        'Linux,Ansible,Bash,Monitoring,Backup',
        'Windows,Linux,Virtualization,Networking,Security',
        'Linux,Shell Scripting,Apache,MySQL,Monitoring',
        'Windows Server,Hyper-V,PowerShell,Backup,Security',
        'Linux,Docker,Kubernetes,Monitoring,Automation'
    ]
}

# Extended interest combinations
CAREER_INTERESTS_MAP = {
    'Data Scientist': [
        'Research,Analysis,Statistics,Problem Solving',
        'Research,ML,Data Analysis,Innovation',
        'Analysis,Mathematics,Research,Development',
        'Problem Solving,Research,Analysis,Technology',
        'Research,Statistics,Data,Innovation',
        'Analysis,Research,ML,Mathematics'
    ],
    'Machine Learning Engineer': [
        'Development,Research,ML,AI,Innovation',
        'AI,Research,Development,Problem Solving',
        'Research,Development,Innovation,Technology',
        'ML,AI,Development,Research,Mathematics',
        'Development,AI,Research,Optimization',
        'Research,ML,Development,Innovation'
    ],
    'Software Developer': [
        'Development,Programming,Problem Solving,Technology',
        'Development,Coding,Innovation,Design',
        'Programming,Development,Logic,Problem Solving',
        'Development,Technology,Innovation,Architecture',
        'Coding,Development,Problem Solving,Design',
        'Development,Programming,Debugging,Innovation'
    ],
    'Data Analyst': [
        'Analysis,Business,Statistics,Reporting',
        'Data Analysis,Business Intelligence,Reporting',
        'Analysis,Statistics,Business,Visualization',
        'Business Analysis,Data,Reporting,Insights',
        'Analysis,Business,Data,Decision Making',
        'Statistics,Analysis,Business,Problem Solving'
    ],
    'Web Developer': [
        'Development,Design,UI/UX,Frontend',
        'Web Development,Design,User Experience',
        'Development,Frontend,Design,Innovation',
        'Web Design,Development,Creativity,User Experience',
        'Development,UI Design,Frontend,Responsive',
        'Design,Development,Web,User Experience'
    ],
    'Full Stack Developer': [
        'Development,Full Stack,Problem Solving,Architecture',
        'Development,Frontend,Backend,Database',
        'Full Stack,Development,Design,Problem Solving',
        'Development,Architecture,Full Stack,Innovation',
        'Frontend,Backend,Development,Problem Solving',
        'Development,Full Stack,API,Database'
    ],
    'DevOps Engineer': [
        'Automation,CI/CD,Infrastructure,Cloud',
        'DevOps,Automation,Cloud,Problem Solving',
        'Infrastructure,Automation,Monitoring,Cloud',
        'CI/CD,Automation,DevOps,Innovation',
        'Cloud,Automation,Infrastructure,Deployment',
        'DevOps,Cloud,Automation,Scalability'
    ],
    'Cloud Engineer': [
        'Cloud,Infrastructure,Architecture,Scalability',
        'Cloud Computing,Infrastructure,Automation',
        'Cloud,Architecture,DevOps,Innovation',
        'Infrastructure,Cloud,Automation,Security',
        'Cloud,Scalability,Architecture,Cost Optimization',
        'Cloud Computing,Infrastructure,Migration'
    ],
    'Mobile Developer': [
        'Mobile Development,Apps,UI/UX,Innovation',
        'Development,Mobile,User Experience,Design',
        'Mobile Apps,Development,Innovation,Performance',
        'Development,Mobile,Cross-Platform,UI',
        'Mobile Development,User Experience,Performance',
        'Apps,Mobile Development,Design,Innovation'
    ],
    'UI/UX Developer': [
        'Design,User Experience,Frontend,Creativity',
        'UI/UX,Design,Development,User Research',
        'Design,User Experience,Prototyping,Innovation',
        'UI Design,UX,Development,Accessibility',
        'Design,User Experience,Visual Design,Frontend',
        'UX,UI,Design Thinking,User Research'
    ],
    'Business Analyst': [
        'Business,Analysis,Requirements,Strategy',
        'Business Analysis,Requirements,Process Improvement',
        'Analysis,Business,Stakeholder Management',
        'Business,Strategy,Analysis,Problem Solving',
        'Requirements Analysis,Business,Documentation',
        'Business Analysis,Strategy,Process,Reporting'
    ],
    'Cybersecurity Analyst': [
        'Security,Analysis,Threat Detection,Protection',
        'Cybersecurity,Security,Risk Management',
        'Security,Analysis,Incident Response,Prevention',
        'Security,Protection,Analysis,Compliance',
        'Cybersecurity,Threat Analysis,Security,Monitoring',
        'Security,Analysis,Risk Assessment,Protection'
    ],
    'Database Administrator': [
        'Database,Administration,Performance,Backup',
        'Database Management,Performance Tuning,Optimization',
        'Administration,Database,Security,Backup',
        'Database,Optimization,Administration,Design',
        'Database Management,Performance,High Availability',
        'Administration,Database,Troubleshooting,Backup'
    ],
    'Game Developer': [
        'Game Development,Design,Creativity,Innovation',
        'Gaming,Development,3D,Graphics',
        'Game Design,Development,Programming,Creativity',
        'Development,Gaming,Innovation,Visual Effects',
        'Game Development,Programming,Design,Physics',
        'Gaming,Development,Creativity,Storytelling'
    ],
    'AI Engineer': [
        'AI,ML,Research,Innovation,Deep Learning',
        'Artificial Intelligence,Research,ML,Development',
        'AI,Research,Innovation,Problem Solving',
        'ML,AI,Research,Neural Networks,Innovation',
        'AI,Deep Learning,Research,Development',
        'Artificial Intelligence,Research,ML,Algorithms'
    ],
    'Blockchain Developer': [
        'Blockchain,DeFi,Development,Cryptography',
        'Blockchain,Development,Decentralization,Innovation',
        'Blockchain,Smart Contracts,Development,Security',
        'Development,Blockchain,Cryptography,DApps',
        'Blockchain,Development,Web3,Innovation',
        'Blockchain,Decentralization,Development,Finance'
    ],
    'Network Engineer': [
        'Networking,Infrastructure,Troubleshooting,Design',
        'Network Design,Administration,Security',
        'Networking,Infrastructure,Performance,Security',
        'Network Administration,Design,Troubleshooting',
        'Networking,Security,Infrastructure,Optimization',
        'Network Design,Infrastructure,Administration'
    ],
    'QA Engineer': [
        'Testing,Quality Assurance,Automation,Problem Detection',
        'QA,Testing,Bug Detection,Quality',
        'Quality Assurance,Testing,Automation,Analysis',
        'Testing,QA,Automation,Problem Solving',
        'Quality,Testing,Automation,Debugging',
        'QA,Testing,Quality Control,Automation'
    ],
    'Product Manager': [
        'Product Management,Strategy,Leadership,Innovation',
        'Product,Strategy,User Research,Business',
        'Product Management,Roadmap,Strategy,Analysis',
        'Strategy,Product,Leadership,Market Research',
        'Product Management,Innovation,Strategy,User Focus',
        'Product,Business,Strategy,Development'
    ],
    'System Administrator': [
        'System Administration,Infrastructure,Troubleshooting,Automation',
        'Administration,Systems,Monitoring,Problem Solving',
        'System Administration,Infrastructure,Security,Backup',
        'Administration,Systems,Automation,Maintenance',
        'System Administration,Networking,Security,Infrastructure',
        'Administration,Systems,Troubleshooting,Monitoring'
    ]
}


def generate_realistic_scores(base_score: float, variation: int = 5) -> float:
    """
    Generate realistic score variations.
    
    Args:
        base_score (float): Base score to vary
        variation (int): Maximum variation in percentage points
        
    Returns:
        float: Varied score
    """
    score = base_score + random.uniform(-variation, variation)
    return max(40.0, min(100.0, score))  # Clamp between 40 and 100


def generate_augmented_samples(original_data: List[Dict[str, Any]], target_count: int = 1000) -> List[Dict[str, Any]]:
    """
    Generate augmented samples from original data.
    
    Args:
        original_data (List[Dict[str, Any]]): Original dataset
        target_count (int): Target number of samples
        
    Returns:
        List[Dict[str, Any]]: Augmented dataset
    """
    augmented_data = []
    
    # Group original data by career
    career_groups = {}
    for record in original_data:
        career = record['recommended_career']
        if career not in career_groups:
            career_groups[career] = []
        career_groups[career].append(record)
    
    # Calculate how many samples per career
    careers = list(career_groups.keys())
    samples_per_career = target_count // len(careers)
    
    logger.info(f"Generating {samples_per_career} samples for each of {len(careers)} careers...")
    
    student_id_counter = 1
    
    for career in careers:
        career_samples = career_groups[career]
        
        for i in range(samples_per_career):
            # Select a base sample
            base_sample = random.choice(career_samples)
            
            # Generate varied scores
            score_10th = generate_realistic_scores(float(base_sample['score_10th']), variation=5)
            score_12th = generate_realistic_scores(float(base_sample['score_12th']), variation=5)
            score_ug = generate_realistic_scores(float(base_sample['score_ug']), variation=5)
            
            # Select varied skills and interests
            if career in CAREER_SKILLS_MAP:
                skills = random.choice(CAREER_SKILLS_MAP[career])
            else:
                skills = base_sample['skills']
            
            if career in CAREER_INTERESTS_MAP:
                interests = random.choice(CAREER_INTERESTS_MAP[career])
            else:
                interests = base_sample['interests']
            
            augmented_sample = {
                'student_id': f'S{student_id_counter:04d}',
                'score_10th': round(score_10th, 2),
                'score_12th': round(score_12th, 2),
                'score_ug': round(score_ug, 2),
                'skills': skills,
                'interests': interests,
                'recommended_career': career
            }
            
            augmented_data.append(augmented_sample)
            student_id_counter += 1
    
    logger.info(f"Generated {len(augmented_data)} augmented samples")
    return augmented_data


def main():
    """Main function to generate expanded dataset."""
    print("="*60)
    print("Career Dataset Augmentation - 100 to 1000 Samples")
    print("="*60)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Initialize database
    db = DatabaseManager('data/career_system.db')
    
    # Get original data
    print("\n[1/4] Loading original data from database...")
    original_data = db.get_all_career_data()
    print(f"[OK] Loaded {len(original_data)} original samples")
    
    # Generate augmented samples
    print(f"\n[2/4] Generating {1000} augmented samples...")
    augmented_data = generate_augmented_samples(original_data, target_count=1000)
    print(f"[OK] Generated {len(augmented_data)} samples")
    
    # Clear existing data and insert augmented data
    print("\n[3/4] Replacing database with augmented data...")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM career_data")
        logger.info("Cleared existing career data")
    
    # Insert augmented data
    db.bulk_insert_career_data(augmented_data)
    print(f"[OK] Inserted {len(augmented_data)} records into database")
    
    # Save to CSV as well
    print("\n[4/4] Saving to CSV...")
    df = pd.DataFrame(augmented_data)
    df = df.rename(columns={
        'student_id': 'Student_ID',
        'score_10th': '10th_Score',
        'score_12th': '12th_Score',
        'score_ug': 'UG_Score',
        'skills': 'Skills',
        'interests': 'Interests',
        'recommended_career': 'Recommended_Career'
    })
    df.to_csv('data/career_data_expanded.csv', index=False)
    print("[OK] Saved to data/career_data_expanded.csv")
    
    # Show statistics
    print("\n" + "="*60)
    print("Dataset Statistics:")
    print("="*60)
    print(f"Total Samples: {len(augmented_data)}")
    print(f"Unique Careers: {df['Recommended_Career'].nunique()}")
    print("\nSamples per Career:")
    career_counts = df['Recommended_Career'].value_counts()
    for career, count in career_counts.items():
        print(f"  {career}: {count}")
    
    print("\nScore Statistics:")
    print(f"  10th Score: {df['10th_Score'].min():.2f} - {df['10th_Score'].max():.2f} (avg: {df['10th_Score'].mean():.2f})")
    print(f"  12th Score: {df['12th_Score'].min():.2f} - {df['12th_Score'].max():.2f} (avg: {df['12th_Score'].mean():.2f})")
    print(f"  UG Score: {df['UG_Score'].min():.2f} - {df['UG_Score'].max():.2f} (avg: {df['UG_Score'].mean():.2f})")
    
    print("\n" + "="*60)
    print("[OK] Dataset augmentation completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()

