#!/usr/bin/env python3
"""
Simple ANX + Ollama Integration Setup
"""

import os
import json
import requests

def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama running with {len(models)} models")
            for model in models[:3]:
                print(f"   📦 {model.get('name', 'Unknown')}")
            return True
        else:
            print("⚠️ Ollama not responding")
            return False
    except Exception as e:
        print("⚠️ Ollama not accessible - make sure it's running with: ollama serve")
        return False

def create_hybrid_config():
    """Create simple hybrid configuration"""
    config = {
        "name": "ANX + Superagent Hybrid",
        "local_ai": "ollama",
        "cloud_ai": "anthropic",
        "database": "supabase",
        "strategy": "local_first"
    }
    
    with open("anx-hybrid-config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration saved: anx-hybrid-config.json")

def create_startup_script():
    """Create simple startup script"""
    script = """@echo off
echo Starting ANX + Superagent Hybrid System
echo =======================================

echo Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama is running
) else (
    echo ⚠️ Start Ollama with: ollama serve
)

echo.
echo Starting Superagent backend...
start "Superagent API" cmd /k "cd bot-anx\\backend && python -m uvicorn server:app --port 8001 --reload --env-file .env.supabase"

echo.
echo ✅ Hybrid system ready!
echo 🏠 Use ANX in your terminal for local AI
echo ☁️ Use API at http://localhost:8001 for cloud features
echo 📊 Monitor at https://supabase.com/dashboard/project/heeshlozzipoullvnbja
pause
"""
    
    with open("start-anx-hybrid.bat", "w", encoding='utf-8') as f:
        f.write(script)
    
    print("✅ Startup script created: start-anx-hybrid.bat")

def main():
    print("🔥 Setting up ANX + Superagent Hybrid System")
    print("=" * 45)
    
    # Check Ollama
    ollama_running = check_ollama()
    
    # Create configuration
    create_hybrid_config()
    
    # Create startup script
    create_startup_script()
    
    print("\n🎉 Hybrid Setup Complete!")
    print("\n📋 Your Hybrid System:")
    print("🏠 Local ANX + Ollama: Fast, private AI in terminal")
    print("☁️ Cloud Superagent: Scalable coordination & monitoring")
    print("🗄️ Supabase Database: Real-time data sync")
    
    print("\n🚀 How to Use:")
    print("1. Keep using ANX in your terminal as usual")
    print("2. Start hybrid system: .\\start-anx-hybrid.bat")
    print("3. Get best of both: local speed + cloud coordination")
    
    if not ollama_running:
        print("\n⚠️ Next: Start Ollama with: ollama serve")
    
    print("\n💡 Benefits:")
    print("• Local AI: No API costs, fast responses, privacy")
    print("• Cloud coordination: Team collaboration, monitoring")
    print("• Hybrid workflow: Use both as needed")

if __name__ == "__main__":
    main()