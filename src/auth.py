"""
Authentication Module with JWT

This module handles user authentication, registration, and JWT token management.
"""

import jwt
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, Any
import logging
from functools import wraps
from flask import request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthManager:
    """
    Manages user authentication and JWT tokens.
    """
    
    def __init__(self, secret_key: str = None):
        """
        Initialize the auth manager.
        
        Args:
            secret_key (str): Secret key for JWT encoding
        """
        self.secret_key = secret_key or os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this')
        self.algorithm = 'HS256'
        self.token_expiry_hours = 24  # Token valid for 24 hours
        self.refresh_token_expiry_days = 30  # Refresh token valid for 30 days
    
    def hash_password(self, password: str) -> str:
        """
        Hash password using SHA-256.
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            password (str): Plain text password
            hashed_password (str): Hashed password
            
        Returns:
            bool: True if password matches
        """
        return self.hash_password(password) == hashed_password
    
    def generate_token(self, user_id: int, email: str, is_admin: bool = False) -> str:
        """
        Generate JWT access token.
        
        Args:
            user_id (int): User ID
            email (str): User email
            is_admin (bool): Whether user is admin
            
        Returns:
            str: JWT token
        """
        payload = {
            'user_id': user_id,
            'email': email,
            'is_admin': is_admin,
            'exp': datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def generate_refresh_token(self, user_id: int) -> str:
        """
        Generate JWT refresh token.
        
        Args:
            user_id (int): User ID
            
        Returns:
            str: Refresh token
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=self.refresh_token_expiry_days),
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode JWT token.
        
        Args:
            token (str): JWT token
            
        Returns:
            Optional[Dict]: Decoded payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email (str): Email address
            
        Returns:
            bool: True if valid
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength.
        
        Args:
            password (str): Password to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        
        return True, "Password is strong"
    
    def create_auth_response(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create authentication response with tokens.
        
        Args:
            user_data (Dict): User data
            
        Returns:
            Dict: Authentication response
        """
        access_token = self.generate_token(
            user_data['user_id'],
            user_data['email'],
            user_data.get('is_admin', False)
        )
        
        refresh_token = self.generate_refresh_token(user_data['user_id'])
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': self.token_expiry_hours * 3600,  # in seconds
            'user': {
                'user_id': user_data['user_id'],
                'email': user_data['email'],
                'full_name': user_data.get('full_name', ''),
                'is_admin': user_data.get('is_admin', False)
            }
        }


def token_required(f):
    """
    Decorator to require JWT token for Flask routes.
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route(current_user):
            return jsonify({'message': f'Hello {current_user["email"]}'})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Verify token
        auth_manager = AuthManager()
        payload = auth_manager.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Check if it's an access token
        if payload.get('type') != 'access':
            return jsonify({'error': 'Invalid token type'}), 401
        
        # Pass user info to the route
        current_user = {
            'user_id': payload['user_id'],
            'email': payload['email'],
            'is_admin': payload.get('is_admin', False)
        }
        
        return f(current_user, *args, **kwargs)
    
    return decorated


def admin_required(f):
    """
    Decorator to require admin privileges.
    
    Usage:
        @app.route('/admin')
        @admin_required
        def admin_route(current_user):
            return jsonify({'message': 'Admin access granted'})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Verify token
        auth_manager = AuthManager()
        payload = auth_manager.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Check if user is admin
        if not payload.get('is_admin', False):
            return jsonify({'error': 'Admin privileges required'}), 403
        
        # Pass user info to the route
        current_user = {
            'user_id': payload['user_id'],
            'email': payload['email'],
            'is_admin': True
        }
        
        return f(current_user, *args, **kwargs)
    
    return decorated


class SessionManager:
    """
    Manages user sessions and refresh tokens.
    """
    
    def __init__(self):
        """Initialize session manager."""
        self.active_sessions = {}  # In production, use Redis
        self.blacklisted_tokens = set()  # In production, use Redis
    
    def create_session(self, user_id: int, access_token: str, refresh_token: str):
        """
        Create a new user session.
        
        Args:
            user_id (int): User ID
            access_token (str): Access token
            refresh_token (str): Refresh token
        """
        self.active_sessions[user_id] = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'created_at': datetime.utcnow(),
            'last_activity': datetime.utcnow()
        }
    
    def update_session_activity(self, user_id: int):
        """Update last activity time."""
        if user_id in self.active_sessions:
            self.active_sessions[user_id]['last_activity'] = datetime.utcnow()
    
    def end_session(self, user_id: int):
        """End user session (logout)."""
        if user_id in self.active_sessions:
            # Blacklist tokens
            session = self.active_sessions[user_id]
            self.blacklisted_tokens.add(session['access_token'])
            self.blacklisted_tokens.add(session['refresh_token'])
            
            # Remove session
            del self.active_sessions[user_id]
    
    def is_token_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted."""
        return token in self.blacklisted_tokens
    
    def get_active_sessions_count(self) -> int:
        """Get number of active sessions."""
        return len(self.active_sessions)
    
    def cleanup_expired_sessions(self, hours: int = 24):
        """Remove expired sessions."""
        current_time = datetime.utcnow()
        expired_users = []
        
        for user_id, session in self.active_sessions.items():
            if (current_time - session['last_activity']).total_seconds() > hours * 3600:
                expired_users.append(user_id)
        
        for user_id in expired_users:
            self.end_session(user_id)
        
        logger.info(f"Cleaned up {len(expired_users)} expired sessions")


def main():
    """Test authentication functionality."""
    auth_manager = AuthManager()
    
    print("="*60)
    print("Testing Authentication System")
    print("="*60)
    
    # Test password hashing
    password = "SecurePassword123"
    hashed = auth_manager.hash_password(password)
    print(f"\n1. Password Hashing:")
    print(f"   Original: {password}")
    print(f"   Hashed: {hashed[:50]}...")
    print(f"   Verification: {auth_manager.verify_password(password, hashed)}")
    
    # Test password strength validation
    print(f"\n2. Password Strength Validation:")
    test_passwords = ["weak", "Weak123", "StrongPassword123"]
    for pwd in test_passwords:
        is_valid, msg = auth_manager.validate_password_strength(pwd)
        print(f"   {pwd}: {'✓' if is_valid else '✗'} - {msg}")
    
    # Test email validation
    print(f"\n3. Email Validation:")
    test_emails = ["user@example.com", "invalid.email", "test@test.co.uk"]
    for email in test_emails:
        is_valid = auth_manager.validate_email(email)
        print(f"   {email}: {'✓' if is_valid else '✗'}")
    
    # Test token generation
    print(f"\n4. JWT Token Generation:")
    token = auth_manager.generate_token(1, "user@example.com", False)
    print(f"   Token: {token[:50]}...")
    
    # Test token verification
    print(f"\n5. Token Verification:")
    payload = auth_manager.verify_token(token)
    if payload:
        print(f"   User ID: {payload['user_id']}")
        print(f"   Email: {payload['email']}")
        print(f"   Expires: {datetime.fromtimestamp(payload['exp'])}")
    
    # Test refresh token
    print(f"\n6. Refresh Token:")
    refresh_token = auth_manager.generate_refresh_token(1)
    print(f"   Refresh Token: {refresh_token[:50]}...")
    
    # Test auth response
    print(f"\n7. Complete Auth Response:")
    user_data = {
        'user_id': 1,
        'email': 'user@example.com',
        'full_name': 'Test User',
        'is_admin': False
    }
    auth_response = auth_manager.create_auth_response(user_data)
    print(f"   Access Token: {auth_response['access_token'][:50]}...")
    print(f"   Token Type: {auth_response['token_type']}")
    print(f"   Expires In: {auth_response['expires_in']} seconds")
    print(f"   User: {auth_response['user']['email']}")
    
    print("\n" + "="*60)
    print("Authentication System Test Complete!")
    print("="*60)


if __name__ == "__main__":
    main()

