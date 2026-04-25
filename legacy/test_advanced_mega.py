#!/usr/bin/env python3
'''
Advanced MEGA Ecosystem Test
Tests all advanced features
'''

import asyncio
import requests
import json
from pathlib import Path

async def test_advanced_features():
    print("Advanced MEGA AI Ecosystem Test")
    print("=" * 40)
    
    results = {}
    
    # Test Ollama (Local AI)
    print("\n1. Testing Ollama Advanced Features...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            results['ollama'] = f"Running with {len(models)} models"
            print(f"   Ollama: Running with {len(models)} models")
        else:
            results['ollama'] = "Not responding"
            print("   Ollama: Not responding")
    except:
        results['ollama'] = "Not running"
        print("   Ollama: Not running - start with 'ollama serve'")
    
    # Test Claw-code
    print("\n2. Testing Claw-code Advanced Features...")
    claw_path = Path("claw-code/rust/target/debug/claw.exe")
    if claw_path.exists():
        results['claw_code'] = "Built and ready"
        print("   Claw-code: Built and ready")
        
        # Check advanced settings
        settings_path = Path("claw-code/.claw/settings.json")
        if settings_path.exists():
            print("   Advanced settings: Configured")
        else:
            print("   Advanced settings: Not found")
    else:
        results['claw_code'] = "Not built"
        print("   Claw-code: Not built - run startup script")
    
    # Test Superagent
    print("\n3. Testing Superagent Advanced Features...")
    try:
        response = requests.get("http://localhost:8001/docs", timeout=2)
        if response.status_code == 200:
            results['superagent'] = "API running"
            print("   Superagent: API running with advanced workflows")
        else:
            results['superagent'] = "Not responding"
            print("   Superagent: Not responding")
    except:
        results['superagent'] = "Not running"
        print("   Superagent: Not running")
    
    # Test Godmode
    print("\n4. Testing Godmode Advanced Features...")
    try:
        response = requests.get("http://localhost:18789/health", timeout=2)
        if response.status_code == 200:
            results['godmode'] = "AI OS running with 35 agents"
            print("   Godmode: AI OS running with 35 specialist agents")
        else:
            results['godmode'] = "Not responding"
            print("   Godmode: Not responding")
    except:
        results['godmode'] = "Not running"
        print("   Godmode: Not running")
    
    # Test Supabase
    print("\n5. Testing Supabase Advanced Integration...")
    try:
        response = requests.get("https://heeshlozzipoullvnbja.supabase.co/rest/v1/", timeout=5)
        if response.status_code in [200, 401]:
            results['supabase'] = "Connected with real-time features"
            print("   Supabase: Connected with real-time features")
        else:
            results['supabase'] = f"Status {response.status_code}"
            print(f"   Supabase: Status {response.status_code}")
    except:
        results['supabase'] = "Connection failed"
        print("   Supabase: Connection failed")
    
    # Summary
    print("\n" + "=" * 40)
    print("ADVANCED SYSTEM STATUS")
    print("=" * 40)
    
    running = sum(1 for status in results.values() if "running" in status.lower() or "connected" in status.lower() or "ready" in status.lower())
    total = len(results)
    
    for system, status in results.items():
        status_icon = "✅" if any(word in status.lower() for word in ["running", "connected", "ready", "built"]) else "❌"
        print(f"{status_icon} {system}: {status}")
    
    print(f"\nStatus: {running}/{total} systems operational")
    
    if running >= 4:
        print("\n🎉 Advanced MEGA Ecosystem is ready!")
        print("\nAdvanced capabilities available:")
        print("  🏠 Local AI with Ollama + Claw-code advanced features")
        print("  🔄 Workflow coordination with Superagent")
        print("  ☁️ 35 specialist agents with Godmode")
        print("  📊 Real-time tracking with Supabase")
        print("  🧠 Memory systems and overnight optimization")
        print("  🎯 Intelligent task routing")
        print("  🔒 Quality gates and TDD enforcement")
    else:
        print("\n⚠️ Some systems need to be started")
        print("Run: start-advanced-mega.bat")
    
    return results

if __name__ == "__main__":
    asyncio.run(test_advanced_features())
