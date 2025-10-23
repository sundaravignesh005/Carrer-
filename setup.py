"""
Setup Script for Career Recommendation System

This script sets up the environment and installs dependencies.
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"   ✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ {description} failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"   ❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.8 or higher.")
        return False
    else:
        print(f"   ✅ Python {version.major}.{version.minor} is compatible")
        return True

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    # Check if pip is available
    if not run_command("pip --version", "Checking pip"):
        print("   ❌ pip is not available. Please install pip first.")
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("   ❌ Failed to install requirements. Please check the requirements.txt file.")
        return False
    
    return True

def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    
    directories = ['data', 'models', 'src']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✅ Created directory: {directory}")
        else:
            print(f"   ✅ Directory already exists: {directory}")
    
    return True

def verify_files():
    """Verify that all required files exist."""
    print("🔍 Verifying files...")
    
    required_files = [
        'requirements.txt',
        'README.md',
        'data/career_data.csv',
        'src/data_processing.py',
        'src/model.py',
        'src/jobs_scraper.py',
        'src/cli_interface.py',
        'app.py',
        'streamlit_app.py',
        'test_system.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"   ⚠️  {len(missing_files)} files are missing. Please check the project structure.")
        return False
    
    return True

def run_tests():
    """Run system tests."""
    print("🧪 Running system tests...")
    
    if not run_command("python test_system.py", "Running tests"):
        print("   ⚠️  Some tests failed. Please check the test output above.")
        return False
    
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up Career Recommendation System")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Verify files
    if not verify_files():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Run tests
    if not run_tests():
        print("   ⚠️  Setup completed with warnings. Some tests failed.")
    else:
        print("   ✅ All tests passed!")
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\n📝 How to use the system:")
    print("1. CLI Interface: python src/cli_interface.py")
    print("2. Flask API: python app.py")
    print("3. Streamlit Web App: streamlit run streamlit_app.py")
    print("4. Run tests: python test_system.py")
    
    print("\n🔧 System Information:")
    print(f"   - Python version: {sys.version}")
    print(f"   - Platform: {platform.system()} {platform.release()}")
    print(f"   - Working directory: {os.getcwd()}")

if __name__ == "__main__":
    main()
