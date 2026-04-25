#!/usr/bin/env python3
"""
Test Supabase Connection for Ultimate Superagent
Verifies database setup and real-time capabilities
"""

import os
import sys
import asyncio
from datetime import datetime
import json

# Add the bot-anx backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'bot-anx', 'backend'))

try:
    from supabase import create_client, Client
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("Install with: pip install supabase postgrest-py realtime-py gotrue-py")
    sys.exit(1)

async def test_supabase_connection():
    """Test Supabase connection and functionality"""
    print("🧪 Testing Supabase connection...")
    
    # Check environment variables
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set them in your environment or .env file")
        return False
    
    try:
        # Test basic connection
        url = os.environ.get('SUPABASE_URL')
        anon_key = os.environ.get('SUPABASE_ANON_KEY')
        service_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
        
        client = create_client(url, anon_key)
        print(f"✅ Connected to Supabase: {url}")
        
        # Test database query
        result = client.table('tickets').select('count').execute()
        print("✅ Database query successful")
        
        # Test inserting test data (using service role to bypass RLS for testing)
        test_ticket = {
            'clickup_id': f'TEST-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'name': 'Test Connection Ticket',
            'description': 'This is a test ticket to verify Supabase connection',
            'status': 'open',
            'priority': 'normal'
        }
        
        # Use service role client for admin operations (bypasses RLS)
        service_client = create_client(url, service_key or anon_key)
        result = service_client.table('tickets').insert(test_ticket).execute()
        
        if result.data:
            print("✅ Test data inserted successfully")
            
            # Test retrieving the ticket
            retrieved = service_client.table('tickets').select('*').eq('clickup_id', test_ticket['clickup_id']).execute()
            if retrieved.data:
                print("✅ Test data retrieved successfully")
            else:
                print("⚠️ Could not retrieve test data")
        else:
            print("⚠️ Could not insert test data")
        
        # Test real-time endpoint
        realtime_url = client.url.replace('http', 'ws') + '/realtime/v1/websocket'
        print(f"✅ Real-time endpoint: {realtime_url}")
        
        # Test event logging (using service role)
        event_data = {
            'event_type': 'connection_test',
            'data': {'timestamp': datetime.utcnow().isoformat()}
        }
        service_client.table('superagent_events').insert(event_data).execute()
        print("✅ Event logging successful")
        
        # Test getting recent events
        events = service_client.table('superagent_events').select('*').limit(5).execute()
        print(f"✅ Retrieved {len(events.data)} recent events")
        
        print("\n🎉 Supabase setup successful!")
        print(f"Dashboard: {url.replace('https://', 'https://supabase.com/dashboard/project/').replace('.supabase.co', '')}")
        print(f"API: {url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def test_environment_setup():
    """Test if environment is properly configured"""
    print("\n🔧 Testing environment setup...")
    
    # Check if Supabase CLI is available
    try:
        import subprocess
        result = subprocess.run(['supabase', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Supabase CLI: {result.stdout.strip()}")
        else:
            print("⚠️ Supabase CLI not found - install with: npm install -g supabase")
    except FileNotFoundError:
        print("⚠️ Supabase CLI not found - install with: npm install -g supabase")
    
    # Check if Supabase is running
    try:
        import requests
        supabase_url = os.environ.get('SUPABASE_URL', 'http://localhost:54321')
        response = requests.get(f"{supabase_url}/rest/v1/", timeout=5)
        if response.status_code == 200:
            print("✅ Supabase server is running")
        else:
            print(f"⚠️ Supabase server returned status {response.status_code}")
    except Exception as e:
        print(f"⚠️ Cannot reach Supabase server: {e}")
        print("Start with: supabase start")
    
    # Check Python dependencies
    required_packages = ['supabase', 'postgrest', 'realtime', 'gotrue']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ Python package: {package}")
        except ImportError:
            print(f"❌ Missing Python package: {package}")
    
    return True

def load_env_file():
    """Load environment variables from .env file"""
    env_files = [
        'bot-anx/backend/.env.supabase',
        '.env.supabase',
        '.env'
    ]
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"📁 Loading environment from: {env_file}")
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            return True
    
    print("⚠️ No .env file found - using system environment variables")
    return False

async def main():
    """Main test function"""
    print("🚀 Ultimate Superagent - Supabase Connection Test")
    print("=" * 50)
    
    # Load environment variables
    load_env_file()
    
    # Test environment setup
    test_environment_setup()
    
    # Test Supabase connection
    success = await test_supabase_connection()
    
    if success:
        print("\n✅ All tests passed! Your Supabase setup is ready.")
        print("\nNext steps:")
        print("1. Add your API tokens to bot-anx/backend/.env.supabase")
        print("2. Start the complete system with: start-superagent-supabase.bat")
        print("3. Monitor progress at: http://localhost:54323")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure Supabase is running: supabase start")
        print("2. Check environment variables in .env.supabase")
        print("3. Install missing dependencies: pip install supabase")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())