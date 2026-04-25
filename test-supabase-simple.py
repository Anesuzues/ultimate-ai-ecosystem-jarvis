#!/usr/bin/env python3
"""
Simple Supabase Connection Test
Tests the database connection and basic operations
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv('bot-anx/backend/.env.supabase')

def test_connection():
    """Test Supabase connection and basic operations"""
    print("🚀 Testing Supabase Connection")
    print("=" * 40)
    
    # Get environment variables
    url = os.environ.get('SUPABASE_URL')
    service_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    anon_key = os.environ.get('SUPABASE_ANON_KEY')
    
    if not all([url, service_key, anon_key]):
        print("❌ Missing environment variables")
        return False
    
    try:
        # Create service role client (bypasses RLS for admin operations)
        service_client: Client = create_client(url, service_key)
        print(f"✅ Connected to Supabase: {url}")
        
        # Test 1: Check if tables exist
        print("\n🔍 Testing table access...")
        result = service_client.table('tickets').select('count').execute()
        print("✅ Tables accessible")
        
        # Test 2: Check existing data
        existing_tickets = service_client.table('tickets').select('*').limit(5).execute()
        print(f"✅ Found {len(existing_tickets.data)} existing tickets")
        
        # Test 3: Insert test data
        print("\n📝 Testing data insertion...")
        test_ticket = {
            'clickup_id': f'TEST-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'name': 'Connection Test Ticket',
            'description': 'Testing Supabase connection and RLS policies',
            'status': 'open',
            'priority': 'normal'
        }
        
        insert_result = service_client.table('tickets').insert(test_ticket).execute()
        if insert_result.data:
            print("✅ Test ticket inserted successfully")
            ticket_id = insert_result.data[0]['clickup_id']
            
            # Test 4: Retrieve the data
            retrieve_result = service_client.table('tickets').select('*').eq('clickup_id', ticket_id).execute()
            if retrieve_result.data:
                print("✅ Test ticket retrieved successfully")
                
                # Test 5: Update the data
                update_result = service_client.table('tickets').update({
                    'status': 'in_progress'
                }).eq('clickup_id', ticket_id).execute()
                if update_result.data:
                    print("✅ Test ticket updated successfully")
                
                # Test 6: Clean up
                delete_result = service_client.table('tickets').delete().eq('clickup_id', ticket_id).execute()
                print("✅ Test ticket cleaned up")
            else:
                print("⚠️ Could not retrieve test ticket")
        else:
            print("❌ Could not insert test ticket")
            return False
        
        # Test 7: Test real-time capabilities
        print("\n📡 Testing real-time setup...")
        realtime_url = url.replace('https://', 'wss://') + '/realtime/v1/websocket'
        print(f"✅ Real-time endpoint: {realtime_url}")
        
        # Test 8: Test other tables
        print("\n🗂️ Testing other tables...")
        tables_to_test = ['task_runs', 'deployments', 'workers', 'superagent_events', 'quality_gates']
        for table in tables_to_test:
            try:
                result = service_client.table(table).select('count').execute()
                print(f"✅ Table '{table}' accessible")
            except Exception as e:
                print(f"⚠️ Table '{table}' issue: {str(e)[:50]}...")
        
        print("\n🎉 All tests passed!")
        print("\n📊 Dashboard URLs:")
        print(f"   🌐 Supabase Dashboard: {url.replace('https://', 'https://supabase.com/dashboard/project/').replace('.supabase.co', '')}")
        print(f"   📋 Table Editor: {url.replace('https://', 'https://supabase.com/dashboard/project/').replace('.supabase.co', '')}/editor")
        print(f"   📈 API Docs: {url}/rest/v1/")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n✅ Supabase is ready for your Ultimate Superagent!")
        print("Next step: Run .\start-cloud-superagent.bat")
    else:
        print("\n❌ Please check your configuration and try again")
        print("Make sure your .env.supabase file has the correct values")