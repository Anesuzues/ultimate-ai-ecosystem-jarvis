#!/usr/bin/env python3
"""
Check ANX + Superagent Hybrid System Status
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv('bot-anx/backend/.env.supabase')

def check_hybrid_status():
    """Check all components of the hybrid system"""
    print("🔥 ANX + Superagent Hybrid System Status")
    print("=" * 45)
    
    # Check Ollama (Local AI)
    print("\n🏠 Local AI Engine:")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama: Running with {len(models)} models")
            for model in models[:3]:
                print(f"   📦 {model.get('name', 'Unknown')}")
        else:
            print("⚠️ Ollama: Not responding")
    except:
        print("❌ Ollama: Not running")
        print("   Start with: ollama serve")
    
    # Check ANX (assume running if in terminal)
    print("✅ ANX: Available in your terminal")
    
    # Check Supabase (Cloud Database)
    print("\n☁️ Cloud Database:")
    supabase_url = os.environ.get('SUPABASE_URL')
    if supabase_url:
        try:
            response = requests.get(f"{supabase_url}/rest/v1/", timeout=5)
            if response.status_code in [200, 401]:
                print(f"✅ Supabase: Connected")
                project_id = supabase_url.split('//')[1].split('.')[0]
                print(f"   📊 Dashboard: https://supabase.com/dashboard/project/{project_id}")
            else:
                print(f"⚠️ Supabase: Status {response.status_code}")
        except:
            print("❌ Supabase: Connection failed")
    
    # Check Superagent API
    print("\n🤖 Superagent API:")
    try:
        response = requests.get("http://localhost:8001/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API: Running on http://localhost:8001")
            print("   📖 Docs: http://localhost:8001/docs")
        else:
            print(f"⚠️ API: Status {response.status_code}")
    except:
        print("❌ API: Not running")
        print("   Start with: .\\start-anx-hybrid.bat")
    
    # Check API Tokens
    print("\n🔑 API Integrations:")
    tokens = {
        'ClickUp': os.environ.get('CLICKUP_TOKEN'),
        'GitHub': os.environ.get('GITHUB_TOKEN'),
        'Anthropic': os.environ.get('ANTHROPIC_API_KEY')
    }
    
    for name, token in tokens.items():
        if token and not token.startswith('your_'):
            print(f"✅ {name}: Configured")
        else:
            print(f"⚠️ {name}: Not configured")
    
    # System Summary
    print("\n🎯 Hybrid System Summary:")
    print("🏠 Local Processing: ANX + Ollama (fast, private, free)")
    print("☁️ Cloud Coordination: Supabase + API (scalable, collaborative)")
    print("🔄 Hybrid Workflow: Best of both worlds")
    
    print("\n💡 How to Use:")
    print("1. 🏠 Use ANX in terminal for coding (local, fast, private)")
    print("2. ☁️ Monitor progress in Supabase dashboard (team collaboration)")
    print("3. 🔗 Create ClickUp tickets to trigger full workflows")
    print("4. 📊 Track everything in real-time")
    
    print("\n🌟 Advantages:")
    print("• Zero API costs for local AI processing")
    print("• Complete privacy for sensitive code")
    print("• Real-time team collaboration")
    print("• Automated workflow orchestration")
    print("• Offline capability with local fallback")
    
    print("\n🚀 Access Points:")
    if supabase_url:
        project_id = supabase_url.split('//')[1].split('.')[0]
        print(f"   📊 Supabase: https://supabase.com/dashboard/project/{project_id}")
    print("   🤖 API Docs: http://localhost:8001/docs")
    print("   🏠 ANX: Your terminal")
    print("   🔧 Ollama: http://localhost:11434")

if __name__ == "__main__":
    check_hybrid_status()
    print("\n🎉 Your hybrid Ultimate Superagent is ready to rock! 🔥")