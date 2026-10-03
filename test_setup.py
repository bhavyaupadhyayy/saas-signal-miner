"""
Test script for SaaS Signal Miner setup
Verifies all dependencies and basic functionality
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import plotly
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        import supabase
        print("✅ Supabase imported successfully")
    except ImportError as e:
        print(f"⚠️ Supabase import failed (optional): {e}")
    
    return True

def test_env_file():
    """Test if environment file exists and has required variables"""
    print("\n🔍 Testing environment configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️ .env file not found")
        print("   Please copy env_template.txt to .env and add your API key")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('PERPLEXITY_API_KEY')

    if not api_key or api_key.startswith("your_"):
        print("❌ PERPLEXITY_API_KEY not configured in .env file")
        print("   Please add your Perplexity API key to the .env file")
        return False

    print("✅ Environment variables loaded successfully")
    print(f"   Model: {os.getenv('PERPLEXITY_MODEL', 'sonar (default)')}")
    print(f"   API Key: {api_key[:5]}...{api_key[-4:] if len(api_key) > 14 else '***'}")
    
    return True

def test_core_modules():
    """Test if core modules can be imported"""
    print("\n🔍 Testing core modules...")
    
    try:
        from utils import get_fallback_data, format_startup_data
        print("✅ Utils module imported successfully")
    except ImportError as e:
        print(f"❌ Utils module import failed: {e}")
        return False
    
    try:
        from main import SaaSSignalMiner
        print("✅ Main module imported successfully")
    except ImportError as e:
        print(f"❌ Main module import failed: {e}")
        return False
    
    try:
        from supabase_client import SupabaseClient
        print("✅ Supabase client imported successfully")
    except ImportError as e:
        print(f"⚠️ Supabase client import failed (optional): {e}")
    
    return True

def test_fallback_data():
    """Test fallback data functionality"""
    print("\n🔍 Testing fallback data...")
    
    try:
        from utils import get_fallback_data, format_startup_data
        
        # Get fallback data
        fallback_data = get_fallback_data()
        print(f"✅ Fallback data generated: {len(fallback_data)} startups")
        
        # Format the data
        formatted_data = format_startup_data(fallback_data)
        print(f"✅ Data formatted successfully: {len(formatted_data)} startups")
        
        # Check structure
        if formatted_data:
            sample = formatted_data[0]
            required_fields = ['name', 'description', 'growth_reason', 'source_link', 'score']
            missing_fields = [field for field in required_fields if field not in sample]
            
            if missing_fields:
                print(f"❌ Missing required fields: {missing_fields}")
                return False
            else:
                print("✅ All required fields present in data structure")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback data test failed: {e}")
        return False

def test_miner_initialization():
    """Test SaaSSignalMiner initialization"""
    print("\n🔍 Testing SaaSSignalMiner initialization...")
    
    try:
        from main import SaaSSignalMiner
        
        miner = SaaSSignalMiner()
        print("✅ SaaSSignalMiner initialized successfully")
        
        # Test filtering
        from utils import get_fallback_data, format_startup_data
        test_data = format_startup_data(get_fallback_data())
        
        filtered_data = miner.filter_startups(test_data, min_score=80)
        print(f"✅ Filtering works: {len(filtered_data)} startups with score >= 80")
        
        return True
        
    except Exception as e:
        print(f"❌ SaaSSignalMiner test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 SaaS Signal Miner - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Environment Configuration", test_env_file),
        ("Core Modules", test_core_modules),
        ("Fallback Data", test_fallback_data),
        ("Miner Initialization", test_miner_initialization)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 Next steps:")
        print("1. Run 'streamlit run app.py' to start the dashboard")
        print("2. Or run 'python main.py' to test the core logic")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("\n🔧 Common fixes:")
        print("1. Run 'pip install -r requirements.txt'")
        print("2. Copy env_template.txt to .env and add your API key")
        print("3. Check your Python version (3.8+ required)")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 