#!/usr/bin/env python3
"""
Apply Database Schema to Supabase Cloud
"""

import os
import sys
from supabase import create_client, Client

# Load environment variables
sys.path.append(os.path.join(os.path.dirname(__file__), 'bot-anx', 'backend'))

# Set environment variables
os.environ['SUPABASE_URL'] = 'https://heeshlozzipoulllvnbja.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'your_supabase_anon_key_here'
os.environ['SUPABASE_SERVICE_ROLE_KEY'] = 'sb_publishable_mWuSlSezHjKLYqmUS6JNsQ_6lXsZ7uT'

def apply_schema():
    """Apply the database schema to Supabase"""
    print("🗄️ Applying database schema to Supabase...")
    
    try:
        # Read the schema file
        with open('supabase-schema.sql', 'r') as f:
            schema_sql = f.read()
        
        # Create Supabase client
        url = os.environ['SUPABASE_URL']
        key = os.environ['SUPABASE_SERVICE_ROLE_KEY']
        supabase: Client = create_client(url, key)
        
        print(f"✅ Connected to Supabase: {url}")
        
        # Split schema into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        print(f"📝 Executing {len(statements)} SQL statements...")
        
        success_count = 0
        for i, statement in enumerate(statements, 1):
            try:
                if statement.upper().startswith(('CREATE', 'ALTER', 'INSERT', 'GRANT')):
                    # Execute via RPC call for DDL statements
                    result = supabase.rpc('exec_sql', {'sql': statement}).execute()
                    print(f"✅ Statement {i}/{len(statements)}: {statement[:50]}...")
                    success_count += 1
                else:
                    print(f"⏭️ Skipping statement {i}: {statement[:50]}...")
            except Exception as e:
                print(f"⚠️ Statement {i} failed: {str(e)[:100]}...")
                # Continue with other statements
                continue
        
        print(f"\n🎉 Schema application complete!")
        print(f"✅ Successfully executed {success_count}/{len(statements)} statements")
        print(f"📊 Dashboard: {url.replace('https://', 'https://supabase.com/dashboard/project/')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to apply schema: {e}")
        return False

if __name__ == "__main__":
    success = apply_schema()
    if success:
        print("\n🚀 Ready to start your Ultimate Superagent!")
        print("Run: python test-supabase-connection.py")
    else:
        print("\n📖 Manual setup required:")
        print("1. Go to your Supabase dashboard")
        print("2. Open SQL Editor")
        print("3. Copy and paste the contents of supabase-schema.sql")
        print("4. Run the SQL")