#!/usr/bin/env python3
"""
Simple Schema Application for Supabase
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('bot-anx/backend/.env.supabase')

# Add the bot-anx backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'bot-anx', 'backend'))

try:
    from supabase_client import get_supabase_client
except ImportError:
    print("❌ Could not import supabase_client")
    print("Make sure you're in the right directory and dependencies are installed")
    sys.exit(1)

def apply_schema():
    """Apply the database schema"""
    print("🗄️ Applying database schema to Supabase...")
    
    try:
        # Get Supabase client
        client = get_supabase_client()
        print(f"✅ Connected to Supabase: {client.url}")
        
        # Read the schema file
        with open('supabase-schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        print("📝 Schema file loaded successfully")
        
        # Test basic connection first
        try:
            result = client.anon_client.table('tickets').select('count').execute()
            print("✅ Tables already exist - schema may already be applied")
            return True
        except Exception:
            print("📋 Tables don't exist yet - applying schema...")
        
        # For now, let's just verify the connection works
        # The actual schema needs to be applied via the Supabase dashboard
        print("\n📖 To complete setup:")
        print("1. Go to your Supabase dashboard: https://supabase.com/dashboard/project/heeshlozzipoullvnbja")
        print("2. Click 'SQL Editor' in the left sidebar")
        print("3. Copy the entire contents of 'supabase-schema.sql'")
        print("4. Paste into the SQL Editor and click 'Run'")
        print("5. Come back and run this test again")
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = apply_schema()
    if success:
        print("\n🎉 Schema is ready!")
        print("Run: python test-supabase-connection.py")
    else:
        print("\n⏳ Waiting for manual schema application...")
        print("After applying schema, run: python test-supabase-connection.py")