"""
Simplified Streamlit App for Career Recommendation
Minimal version that works on Streamlit Cloud
"""

import streamlit as st
import json
import random

# Page config
st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎯",
    layout="wide"
)

# Sample career data
CAREER_DATA = {
    "Data Scientist": {
        "skills": ["Python", "SQL", "Statistics", "ML", "Data Analysis"],
        "description": "Analyze data to help organizations make decisions",
        "salary": "₹6-15 LPA"
    },
    "Software Developer": {
        "skills": ["Programming", "Algorithms", "OOP", "Git", "Testing"],
        "description": "Design and develop software applications",
        "salary": "₹5-12 LPA"
    },
    "Machine Learning Engineer": {
        "skills": ["Python", "ML", "Deep Learning", "TensorFlow", "Statistics"],
        "description": "Build and deploy machine learning models",
        "salary": "₹8-18 LPA"
    },
    "Data Analyst": {
        "skills": ["SQL", "Excel", "Statistics", "Python", "Visualization"],
        "description": "Analyze data to provide business insights",
        "salary": "₹4-10 LPA"
    },
    "Web Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
        "description": "Create and maintain websites and web applications",
        "salary": "₹4-12 LPA"
    },
    "Full Stack Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "Backend", "Database"],
        "description": "Develop both frontend and backend applications",
        "salary": "₹6-15 LPA"
    },
    "DevOps Engineer": {
        "skills": ["Linux", "Docker", "Kubernetes", "CI/CD", "Cloud"],
        "description": "Manage infrastructure and deployment pipelines",
        "salary": "₹8-20 LPA"
    },
    "UI/UX Developer": {
        "skills": ["Design", "Figma", "HTML", "CSS", "User Research"],
        "description": "Create user-friendly interfaces and experiences",
        "salary": "₹5-12 LPA"
    }
}

def calculate_career_match(user_skills, career_skills):
    """Calculate match percentage between user skills and career requirements"""
    user_skills_lower = [skill.lower().strip() for skill in user_skills]
    career_skills_lower = [skill.lower().strip() for skill in career_skills]
    
    matches = sum(1 for skill in user_skills_lower if skill in career_skills_lower)
    total_skills = len(career_skills_lower)
    
    return (matches / total_skills * 100) if total_skills > 0 else 0

def get_job_recommendations(career):
    """Get sample job recommendations for a career"""
    companies = ["TechCorp India", "AI Solutions Pvt Ltd", "DataTech Inc", "WebCraft Studios", "CloudSoft Systems"]
    locations = ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune"]
    
    jobs = []
    for i in range(3):
        jobs.append({
            "title": f"{career}",
            "company": random.choice(companies),
            "location": random.choice(locations),
            "salary": CAREER_DATA[career]["salary"],
            "description": f"Looking for a {career} with relevant skills and experience"
        })
    
    return jobs

def main():
    st.title("🎯 AI Career Recommendation System")
    st.markdown("---")
    
    # Sidebar for input
    with st.sidebar:
        st.header("📝 Your Profile")
        
        # Academic scores
        st.subheader("Academic Performance")
        tenth_score = st.slider("10th Grade Score (%)", 0, 100, 85)
        twelfth_score = st.slider("12th Grade Score (%)", 0, 100, 82)
        ug_score = st.slider("Undergraduate Score (%)", 0, 100, 78)
        
        # Skills input
        st.subheader("Technical Skills")
        skills_input = st.text_area(
            "Enter your skills (comma-separated)",
            value="Python, SQL, JavaScript, HTML, CSS",
            help="e.g., Python, SQL, JavaScript, Machine Learning, React"
        )
        
        # Interests
        st.subheader("Career Interests")
        interests_input = st.text_area(
            "Enter your interests (comma-separated)",
            value="Development, Analysis, Research",
            help="e.g., Development, Research, Business, Design"
        )
        
        # Submit button
        if st.button("🚀 Get Career Recommendation", type="primary"):
            st.session_state.show_results = True
            st.session_state.user_data = {
                "tenth_score": tenth_score,
                "twelfth_score": twelfth_score,
                "ug_score": ug_score,
                "skills": [skill.strip() for skill in skills_input.split(",")],
                "interests": [interest.strip() for interest in interests_input.split(",")]
            }
    
    # Main content area
    if st.session_state.get("show_results", False):
        user_data = st.session_state.user_data
        
        st.header("🎯 Your Career Recommendations")
        
        # Calculate career matches
        career_matches = []
        for career, info in CAREER_DATA.items():
            match_percentage = calculate_career_match(user_data["skills"], info["skills"])
            career_matches.append({
                "career": career,
                "match": match_percentage,
                "info": info
            })
        
        # Sort by match percentage
        career_matches.sort(key=lambda x: x["match"], reverse=True)
        
        # Display top 3 recommendations
        st.subheader("🏆 Top Career Matches")
        
        for i, match in enumerate(career_matches[:3], 1):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {i}. {match['career']}")
                    st.markdown(f"**Match:** {match['match']:.1f}%")
                    st.markdown(f"**Description:** {match['info']['description']}")
                    st.markdown(f"**Salary Range:** {match['info']['salary']}")
                
                with col2:
                    # Progress bar for match percentage
                    st.progress(match['match'] / 100)
                    st.metric("Match Score", f"{match['match']:.1f}%")
                
                st.markdown("---")
        
        # Job recommendations for top career
        top_career = career_matches[0]["career"]
        st.subheader(f"💼 Job Opportunities for {top_career}")
        
        jobs = get_job_recommendations(top_career)
        for i, job in enumerate(jobs, 1):
            with st.expander(f"Job {i}: {job['title']} at {job['company']}"):
                st.markdown(f"**Company:** {job['company']}")
                st.markdown(f"**Location:** {job['location']}")
                st.markdown(f"**Salary:** {job['salary']}")
                st.markdown(f"**Description:** {job['description']}")
                st.button(f"Apply Now", key=f"apply_{i}")
        
        # Skills analysis
        st.subheader("📊 Skills Analysis")
        top_career_skills = CAREER_DATA[top_career]["skills"]
        user_skills_lower = [skill.lower().strip() for skill in user_data["skills"]]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Your Skills:**")
            for skill in user_data["skills"]:
                if skill.lower().strip() in [s.lower() for s in top_career_skills]:
                    st.markdown(f"✅ {skill}")
                else:
                    st.markdown(f"❌ {skill}")
        
        with col2:
            st.markdown("**Required Skills:**")
            for skill in top_career_skills:
                if skill.lower() in user_skills_lower:
                    st.markdown(f"✅ {skill}")
                else:
                    st.markdown(f"⭕ {skill}")
        
        # Reset button
        if st.button("🔄 Try Again"):
            st.session_state.show_results = False
            st.rerun()
    
    else:
        # Welcome message
        st.markdown("""
        ## Welcome to the AI Career Recommendation System! 🎯
        
        This intelligent system analyzes your academic performance, technical skills, and career interests 
        to recommend the most suitable career paths for you.
        
        ### How it works:
        1. **Fill in your profile** using the sidebar
        2. **Enter your academic scores** (10th, 12th, UG)
        3. **List your technical skills** (comma-separated)
        4. **Specify your interests** (comma-separated)
        5. **Click "Get Career Recommendation"** to see your results
        
        ### Features:
        - 🎯 **Personalized career recommendations** based on your profile
        - 💼 **Real-time job opportunities** for recommended careers
        - 📊 **Skills gap analysis** to identify areas for improvement
        - 🏆 **Multiple career options** with match percentages
        
        **Get started by filling in your profile on the left!** 👈
        """)
        
        # Sample careers
        st.subheader("🌟 Available Career Paths")
        cols = st.columns(4)
        careers = list(CAREER_DATA.keys())
        
        for i, career in enumerate(careers):
            with cols[i % 4]:
                st.markdown(f"**{career}**")
                st.markdown(f"*{CAREER_DATA[career]['description']}*")
                st.markdown(f"💰 {CAREER_DATA[career]['salary']}")

if __name__ == "__main__":
    main()
