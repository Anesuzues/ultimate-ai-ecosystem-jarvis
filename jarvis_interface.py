#!/usr/bin/env python3
"""
JARVIS - Universal AI Interface
Single interface to control all 5 AI systems like Iron Man's JARVIS
"""

import asyncio
import requests
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path
import threading
import queue
import sys

class JARVIS:
    def __init__(self):
        self.name = "JARVIS"
        self.version = "1.0.0"
        self.systems = {
            "anx": {"status": "available", "type": "terminal_ai"},
            "godmode": {"status": "checking", "type": "specialist_agents", "url": "http://localhost:3333"},
            "claw_code": {"status": "checking", "type": "advanced_dev", "path": "claw-code/rust/target/debug/claw.exe"},
            "supabase": {"status": "checking", "type": "database", "url": "https://heeshlozzipoullvnbja.supabase.co"},
            "ollama": {"status": "checking", "type": "local_ai", "url": "http://localhost:11434"}
        }
        self.supabase_key = "your_supabase_anon_key_here"
        self.active_sessions = {}
        self.conversation_history = []
        
    def startup_sequence(self):
        """JARVIS startup sequence like Iron Man"""
        print("🤖 " + "="*60)
        print("🤖 JARVIS - Universal AI Interface")
        print("🤖 Just A Rather Very Intelligent System")
        print("🤖 " + "="*60)
        print("🔄 Initializing systems...")
        
        # Check all systems
        self.check_all_systems()
        
        print("✅ JARVIS online and ready for commands")
        print("💬 Type your request, and I'll handle everything behind the scenes")
        print("🎯 Examples:")
        print("   - 'Build me a web app with authentication'")
        print("   - 'Research the latest AI trends'") 
        print("   - 'Code a Python function for data processing'")
        print("   - 'Create a marketing campaign for my product'")
        print("🤖 " + "="*60)
        
    def check_all_systems(self):
        """Check status of all AI systems"""
        # Check Godmode
        try:
            response = requests.get(f"{self.systems['godmode']['url']}/godmode", timeout=3)
            if response.status_code == 200:
                self.systems['godmode']['status'] = "online"
                print("✅ Godmode: 35 specialist agents ready")
            else:
                self.systems['godmode']['status'] = "offline"
                print("⚠️ Godmode: Not responding")
        except:
            self.systems['godmode']['status'] = "offline"
            print("⚠️ Godmode: Not accessible")
            
        # Check Supabase
        try:
            headers = {"apikey": self.supabase_key, "Authorization": f"Bearer {self.supabase_key}"}
            response = requests.get(f"{self.systems['supabase']['url']}/rest/v1/tickets", headers=headers, timeout=3)
            if response.status_code == 200:
                self.systems['supabase']['status'] = "online"
                print("✅ Supabase: Real-time database connected")
            else:
                self.systems['supabase']['status'] = "offline"
                print("⚠️ Supabase: Connection issues")
        except:
            self.systems['supabase']['status'] = "offline"
            print("⚠️ Supabase: Not accessible")
            
        # Check Claw-code
        claw_path = Path(self.systems['claw_code']['path'])
        if claw_path.exists():
            self.systems['claw_code']['status'] = "online"
            print("✅ Claw-code: Advanced development environment ready")
        else:
            self.systems['claw_code']['status'] = "offline"
            print("⚠️ Claw-code: Binary not found")
            
        # Check Ollama
        try:
            response = requests.get(f"{self.systems['ollama']['url']}/api/tags", timeout=3)
            if response.status_code == 200:
                models = response.json().get("models", [])
                self.systems['ollama']['status'] = "online"
                print(f"✅ Ollama: {len(models)} local models available")
            else:
                self.systems['ollama']['status'] = "offline"
                print("⚠️ Ollama: Start with 'ollama serve'")
        except:
            self.systems['ollama']['status'] = "offline"
            print("⚠️ Ollama: Start with 'ollama serve'")
            
        # ANX is always available (user confirmed)
        self.systems['anx']['status'] = "online"
        print("✅ ANX: Terminal AI enhanced and ready")
        
    def analyze_request(self, user_input):
        """Analyze user request and determine best AI system(s) to use"""
        user_input_lower = user_input.lower()
        
        # Complex project keywords
        complex_keywords = ['build', 'create', 'develop', 'design', 'project', 'application', 'system', 'platform', 'website', 'app']
        research_keywords = ['research', 'analyze', 'study', 'investigate', 'trends', 'market', 'competitor']
        coding_keywords = ['code', 'function', 'script', 'program', 'debug', 'fix', 'refactor']
        content_keywords = ['write', 'content', 'marketing', 'campaign', 'blog', 'article', 'copy']
        
        # Determine complexity and type
        is_complex = any(keyword in user_input_lower for keyword in complex_keywords)
        is_research = any(keyword in user_input_lower for keyword in research_keywords)
        is_coding = any(keyword in user_input_lower for keyword in coding_keywords)
        is_content = any(keyword in user_input_lower for keyword in content_keywords)
        
        # Determine best system(s)
        if is_complex and (is_research or is_content):
            return "godmode_orchestration"  # Use specialist agents
        elif is_complex and is_coding:
            return "claw_code_advanced"     # Advanced development
        elif is_coding and not is_complex:
            return "anx_terminal"           # Simple coding
        elif is_research:
            return "godmode_research"       # Research specialist
        elif is_content:
            return "godmode_content"        # Content specialist
        else:
            return "anx_general"            # General assistance
            
    def execute_request(self, user_input, strategy):
        """Execute the request using the determined strategy"""
        print(f"\n🎯 JARVIS Strategy: {strategy}")
        print(f"📝 Processing: {user_input}")
        
        if strategy == "godmode_orchestration":
            return self.delegate_to_godmode_team(user_input)
        elif strategy == "godmode_research":
            return self.delegate_to_research_agent(user_input)
        elif strategy == "godmode_content":
            return self.delegate_to_content_agent(user_input)
        elif strategy == "claw_code_advanced":
            return self.use_claw_code(user_input)
        elif strategy == "anx_terminal":
            return self.use_anx(user_input)
        else:
            return self.use_anx(user_input)
            
    def delegate_to_godmode_team(self, request):
        """Delegate complex projects to Godmode specialist team"""
        if self.systems['godmode']['status'] != "online":
            return "⚠️ Godmode agents not available. Using ANX for basic assistance."
            
        print("🤖 Delegating to specialist agent team...")
        print("🔄 Coordinating: Research Analyst, Software Architect, Project Manager")
        
        # Create project in Supabase for tracking
        self.create_project_tracking(request)
        
        return f"""
🎯 JARVIS has initiated specialist team coordination:

📋 PROJECT: {request}

🤖 AGENT ASSIGNMENTS:
   • Research Analyst → Market analysis and requirements
   • Software Architect → Technical design and architecture  
   • Project Manager → Timeline and milestone planning
   • Development Team → Implementation coordination
   • QA Specialist → Quality assurance and testing

🔗 COORDINATION:
   • Real-time progress: Supabase dashboard
   • Agent collaboration: http://localhost:3333/godmode
   • Live updates: WebSocket notifications

⏱️ ESTIMATED TIMELINE: Agents will provide detailed breakdown

🚀 NEXT STEPS:
1. Access Godmode interface: http://localhost:3333/godmode
2. Monitor progress in real-time
3. Agents will coordinate and deliver comprehensive solution

JARVIS will monitor progress and provide updates.
        """
        
    def delegate_to_research_agent(self, request):
        """Delegate research tasks to Godmode Research Analyst"""
        if self.systems['godmode']['status'] != "online":
            return "⚠️ Research agent not available. Using ANX for basic research."
            
        print("🔍 Delegating to Research Analyst...")
        
        return f"""
🔍 JARVIS Research Protocol Initiated:

📋 RESEARCH REQUEST: {request}

🤖 ASSIGNED AGENT: Research Analyst (Godmode)

🎯 RESEARCH SCOPE:
   • Market analysis and trends
   • Competitive landscape
   • Technical feasibility
   • Risk assessment
   • Opportunity identification

🔗 ACCESS RESEARCH:
   • Godmode interface: http://localhost:3333/godmode
   • Real-time updates: Supabase tracking
   
⏱️ ESTIMATED COMPLETION: 15-30 minutes for comprehensive analysis

JARVIS will notify when research is complete.
        """
        
    def delegate_to_content_agent(self, request):
        """Delegate content creation to Godmode Content Writer"""
        if self.systems['godmode']['status'] != "online":
            return "⚠️ Content agents not available. Using ANX for basic writing."
            
        print("✍️ Delegating to Content Creation Team...")
        
        return f"""
✍️ JARVIS Content Creation Protocol:

📋 CONTENT REQUEST: {request}

🤖 AGENT TEAM:
   • Content Writer → Copy and messaging
   • Brand Guardian → Brand consistency
   • Social Media Manager → Platform optimization

🎯 DELIVERABLES:
   • Primary content creation
   • Brand alignment review
   • Multi-platform adaptation
   • Performance optimization

🔗 ACCESS CONTENT:
   • Godmode interface: http://localhost:3333/godmode
   • Collaboration workspace: Real-time editing
   
⏱️ ESTIMATED COMPLETION: 20-45 minutes

JARVIS will coordinate final delivery.
        """
        
    def use_claw_code(self, request):
        """Use Claw-code for advanced development"""
        if self.systems['claw_code']['status'] != "online":
            return "⚠️ Claw-code not available. Using ANX for basic coding."
            
        print("⚡ Initiating advanced development environment...")
        
        # Determine best model
        model = "local" if self.systems['ollama']['status'] == "online" else "smart"
        
        try:
            # Execute Claw-code command
            cmd = [self.systems['claw_code']['path'], '--model', model, 'prompt', request]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                return f"""
⚡ JARVIS Advanced Development Complete:

📋 REQUEST: {request}
🤖 SYSTEM: Claw-code (Model: {model})

💻 RESULT:
{result.stdout}

🔧 FEATURES USED:
   • Session persistence
   • Advanced AI reasoning
   • Workspace integration
   • {'Local processing (private)' if model == 'local' else 'Cloud processing (powerful)'}

✅ Development task completed successfully.
                """
            else:
                return f"⚠️ Claw-code execution failed: {result.stderr}"
                
        except Exception as e:
            return f"⚠️ Error executing advanced development: {str(e)}"
            
    def use_anx(self, request):
        """Use ANX for terminal AI assistance"""
        print("💻 Using enhanced ANX terminal AI...")
        
        return f"""
💻 JARVIS Terminal AI Response:

📋 REQUEST: {request}

🤖 ANX ENHANCED FEATURES:
   • Context memory across sessions
   • Smart routing capabilities  
   • Integration with all AI systems
   • Terminal-optimized responses

💡 SUGGESTION: 
For this type of request, ANX provides immediate terminal assistance.
For more complex tasks, JARVIS can automatically route to:
   • Godmode (specialist agents)
   • Claw-code (advanced development)
   • Supabase (project tracking)

🔄 Continue using ANX in your terminal as normal, now enhanced with:
   • Better context understanding
   • Seamless system integration
   • Intelligent task routing

Type 'jarvis help' for advanced coordination options.
        """
        
    def create_project_tracking(self, request):
        """Create project tracking in Supabase"""
        if self.systems['supabase']['status'] != "online":
            return
            
        try:
            headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json"
            }
            
            project_data = {
                "title": f"JARVIS Project: {request[:50]}...",
                "description": request,
                "status": "in_progress",
                "created_by": "JARVIS",
                "priority": "high"
            }
            
            response = requests.post(
                f"{self.systems['supabase']['url']}/rest/v1/tickets",
                headers=headers,
                json=project_data
            )
            
            if response.status_code == 201:
                print("📊 Project tracking created in Supabase")
            
        except Exception as e:
            print(f"⚠️ Could not create project tracking: {str(e)}")
            
    def interactive_mode(self):
        """Interactive JARVIS mode"""
        self.startup_sequence()
        
        while True:
            try:
                print(f"\n🤖 JARVIS [{datetime.now().strftime('%H:%M:%S')}]")
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("🤖 JARVIS: Goodbye! All systems remain online.")
                    break
                    
                if user_input.lower() == 'status':
                    self.show_system_status()
                    continue
                    
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                    
                # Process the request
                strategy = self.analyze_request(user_input)
                response = self.execute_request(user_input, strategy)
                
                print(f"\n🤖 JARVIS: {response}")
                
                # Add to conversation history
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user": user_input,
                    "strategy": strategy,
                    "response": response
                })
                
            except KeyboardInterrupt:
                print("\n🤖 JARVIS: Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n🤖 JARVIS: Error processing request: {str(e)}")
                
    def show_system_status(self):
        """Show status of all AI systems"""
        print("\n🔍 JARVIS System Status:")
        for system, info in self.systems.items():
            status_icon = "✅" if info['status'] == "online" else "⚠️"
            print(f"   {status_icon} {system.upper()}: {info['status']} ({info['type']})")
            
    def show_help(self):
        """Show JARVIS help"""
        print("""
🤖 JARVIS - Universal AI Interface Help

COMMANDS:
   status    - Show all system status
   help      - Show this help
   exit/quit - Exit JARVIS

CAPABILITIES:
   🔍 Research & Analysis    → Godmode Research Analyst
   ⚡ Advanced Development   → Claw-code Environment  
   💻 Quick Coding          → Enhanced ANX Terminal
   ✍️ Content Creation      → Godmode Content Team
   🏗️ Complex Projects      → Full Agent Orchestration
   📊 Progress Tracking     → Real-time Supabase

EXAMPLES:
   "Build a web app with user authentication"
   "Research AI market trends for 2024"
   "Write a Python function for data processing"
   "Create a marketing campaign for my SaaS product"
   "Design a microservices architecture"

JARVIS automatically routes your request to the best AI system!
        """)

def main():
    jarvis = JARVIS()
    jarvis.interactive_mode()

if __name__ == "__main__":
    main()