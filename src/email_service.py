"""
Email Notification Service

This module handles sending email notifications for various events
like job alerts, career recommendations, and feedback.
"""

import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailService:
    """
    Handles email notifications using SMTP.
    """
    
    def __init__(self):
        """Initialize email service with configuration."""
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_user)
        self.from_name = os.getenv('FROM_NAME', 'Career Recommendation System')
        
        self.enabled = bool(self.smtp_user and self.smtp_password)
        
        if not self.enabled:
            logger.warning("Email service not configured. Set SMTP credentials in .env file.")
    
    def send_email(self, to_email: str, subject: str, html_content: str,
                  text_content: Optional[str] = None) -> bool:
        """
        Send an email.
        
        Args:
            to_email (str): Recipient email
            subject (str): Email subject
            html_content (str): HTML email body
            text_content (Optional[str]): Plain text fallback
            
        Returns:
            bool: True if sent successfully
        """
        if not self.enabled:
            logger.warning("Email service not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
            
            # Add text part
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            # Add HTML part
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent to {to_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            return False
    
    def send_welcome_email(self, to_email: str, full_name: str) -> bool:
        """Send welcome email to new users."""
        subject = f"Welcome to Career Recommendation System, {full_name}!"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #1f77b4;">Welcome to Career Recommendation System! 🎯</h2>
                
                <p>Hi {full_name},</p>
                
                <p>Thank you for joining our platform! We're excited to help you discover your perfect career path.</p>
                
                <h3>What You Can Do:</h3>
                <ul>
                    <li>Get AI-powered career recommendations</li>
                    <li>Discover job opportunities tailored to your skills</li>
                    <li>Analyze skill gaps and get learning roadmaps</li>
                    <li>Predict salary ranges for different careers</li>
                    <li>Track your career progress</li>
                </ul>
                
                <p style="margin-top: 30px;">
                    <a href="#" style="background-color: #1f77b4; color: white; padding: 12px 24px; 
                       text-decoration: none; border-radius: 5px; display: inline-block;">
                        Get Started
                    </a>
                </p>
                
                <p style="margin-top: 30px; color: #666; font-size: 12px;">
                    If you have any questions, feel free to reach out to our support team.
                </p>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to Career Recommendation System!
        
        Hi {full_name},
        
        Thank you for joining our platform! We're excited to help you discover your perfect career path.
        
        What You Can Do:
        - Get AI-powered career recommendations
        - Discover job opportunities tailored to your skills
        - Analyze skill gaps and get learning roadmaps
        - Predict salary ranges for different careers
        - Track your career progress
        
        Get started today!
        """
        
        return self.send_email(to_email, subject, html_content, text_content)
    
    def send_career_recommendation_email(self, to_email: str, full_name: str,
                                        career: str, confidence: float,
                                        job_count: int) -> bool:
        """Send career recommendation notification."""
        subject = f"Your Career Recommendation: {career}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #1f77b4;">Your Career Recommendation 🎯</h2>
                
                <p>Hi {full_name},</p>
                
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; 
                     border-left: 5px solid #1f77b4; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Recommended Career</h3>
                    <h2 style="color: #1f77b4; margin: 10px 0;">{career}</h2>
                    <p><strong>Confidence:</strong> {confidence:.1f}%</p>
                </div>
                
                <p>We've found <strong>{job_count} job opportunities</strong> matching your profile!</p>
                
                <h3>Next Steps:</h3>
                <ol>
                    <li>Review the job listings we've curated for you</li>
                    <li>Check your skills gap analysis</li>
                    <li>Explore the learning roadmap for this career</li>
                    <li>Apply to jobs that match your interests</li>
                </ol>
                
                <p style="margin-top: 30px;">
                    <a href="#" style="background-color: #1f77b4; color: white; padding: 12px 24px; 
                       text-decoration: none; border-radius: 5px; display: inline-block;">
                        View Jobs
                    </a>
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)
    
    def send_job_alert(self, to_email: str, full_name: str,
                      jobs: List[Dict[str, Any]]) -> bool:
        """Send job alert notification."""
        subject = f"New Job Opportunities for You! ({len(jobs)} jobs)"
        
        # Build job listings HTML
        jobs_html = ""
        for job in jobs[:5]:  # Top 5 jobs
            jobs_html += f"""
            <div style="border: 1px solid #e0e0e0; padding: 15px; margin: 10px 0; 
                 border-radius: 8px; background-color: #ffffff;">
                <h4 style="margin: 0 0 10px 0; color: #1f77b4;">{job['title']}</h4>
                <p style="margin: 5px 0;"><strong>{job['company']}</strong></p>
                <p style="margin: 5px 0; color: #666;">{job['location']}</p>
                <p style="margin: 5px 0; color: #666;">{job.get('salary', 'Salary not specified')}</p>
                <p style="margin-top: 10px;">
                    <a href="{job.get('apply_link', '#')}" style="color: #1f77b4; 
                       text-decoration: none;">Apply Now →</a>
                </p>
            </div>
            """
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #1f77b4;">New Job Opportunities! 💼</h2>
                
                <p>Hi {full_name},</p>
                
                <p>We've found <strong>{len(jobs)} new job opportunities</strong> that match your profile!</p>
                
                <h3>Top Matches:</h3>
                {jobs_html}
                
                <p style="margin-top: 30px;">
                    <a href="#" style="background-color: #1f77b4; color: white; padding: 12px 24px; 
                       text-decoration: none; border-radius: 5px; display: inline-block;">
                        View All Jobs
                    </a>
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)
    
    def send_weekly_insights(self, to_email: str, full_name: str,
                           insights: Dict[str, Any]) -> bool:
        """Send weekly career insights newsletter."""
        subject = "Your Weekly Career Insights 📊"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #1f77b4;">Your Weekly Career Insights 📊</h2>
                
                <p>Hi {full_name},</p>
                
                <p>Here's a summary of your activity this week:</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3>This Week's Stats</h3>
                    <ul>
                        <li><strong>{insights.get('predictions_count', 0)}</strong> career predictions</li>
                        <li><strong>{insights.get('jobs_viewed', 0)}</strong> jobs viewed</li>
                        <li><strong>{insights.get('applications', 0)}</strong> job applications</li>
                        <li><strong>{insights.get('skills_learned', 0)}</strong> new skills added</li>
                    </ul>
                </div>
                
                <h3>Trending Careers This Week:</h3>
                <ul>
                    <li>AI Engineer - Growing demand</li>
                    <li>Cloud Engineer - High salaries</li>
                    <li>Data Scientist - Most searched</li>
                </ul>
                
                <p style="margin-top: 30px;">
                    <a href="#" style="background-color: #1f77b4; color: white; padding: 12px 24px; 
                       text-decoration: none; border-radius: 5px; display: inline-block;">
                        View Dashboard
                    </a>
                </p>
                
                <p style="margin-top: 30px; color: #666; font-size: 12px;">
                    You're receiving this because you subscribed to weekly insights.
                    <a href="#" style="color: #1f77b4;">Unsubscribe</a>
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)
    
    def send_feedback_thank_you(self, to_email: str, full_name: str) -> bool:
        """Send thank you email for feedback."""
        subject = "Thank You for Your Feedback!"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #1f77b4;">Thank You! 🙏</h2>
                
                <p>Hi {full_name},</p>
                
                <p>Thank you for taking the time to provide feedback! Your input helps us improve 
                   our career recommendation system and serve you better.</p>
                
                <p>We're constantly working to enhance your experience and appreciate your valuable insights.</p>
                
                <p>Keep exploring and discovering your perfect career path!</p>
                
                <p style="margin-top: 30px;">Best regards,<br>
                   Career Recommendation Team</p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)
    
    def configure_smtp(self, host: str, port: int, user: str, password: str):
        """
        Configure SMTP settings.
        
        Args:
            host (str): SMTP host
            port (int): SMTP port
            user (str): SMTP username
            password (str): SMTP password
        """
        self.smtp_host = host
        self.smtp_port = port
        self.smtp_user = user
        self.smtp_password = password
        self.from_email = user
        self.enabled = True
        
        logger.info(f"SMTP configured: {host}:{port}")


def main():
    """Test email service."""
    service = EmailService()
    
    print("="*70)
    print("Email Service - Test")
    print("="*70)
    
    if not service.enabled:
        print("\n[INFO] Email service not configured.")
        print("To enable, set these environment variables:")
        print("  - SMTP_HOST")
        print("  - SMTP_PORT")
        print("  - SMTP_USER")
        print("  - SMTP_PASSWORD")
        print("\nExample for Gmail:")
        print("  SMTP_HOST=smtp.gmail.com")
        print("  SMTP_PORT=587")
        print("  SMTP_USER=your-email@gmail.com")
        print("  SMTP_PASSWORD=your-app-password")
    else:
        print(f"\n[OK] Email service configured:")
        print(f"  Host: {service.smtp_host}:{service.smtp_port}")
        print(f"  From: {service.from_email}")
        
        # Test email (commented out to avoid sending)
        # service.send_welcome_email("test@example.com", "Test User")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()

