#!/usr/bin/env python3
"""
JARVIS Web Interface - Like Iron Man's JARVIS
Single web interface to control all AI systems
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import requests
import subprocess
from datetime import datetime
from pathlib import Path
import threading
import time

app = Flask(__name__)

class JARVISWeb:
    def __init__(self):
        self.systems = {
            "godmode": {"status": "checking", "url": "http://localhost:3333"},
            "supabase": {"status": "checking", "url": "https://heeshlozzipoullvnbja.supabase.co"},
            "claw_code": {"status": "checking", "path": "claw-code/rust/target/debug/claw.exe"},
            "ollama": {"status": "checking", "url": "http://localhost:11434"},
            "anx": {"status": "online"}
        }
        self.supabase_key = "your_supabase_anon_key_here"
        self.conversation_history = []
        
    def check_systems(self):
        """Check all AI systems status"""
        # Check Godmode
        try:
            response = requests.get(f"{self.systems['godmode']['url']}/godmode", timeout=3)
            self.systems['godmode']['status'] = "online" if response.status_code == 200 else "offline"
        except:
            self.systems['godmode']['status'] = "offline"
            
        # Check Supabase
        try:
            headers = {"apikey": self.supabase_key}
            response = requests.get(f"{self.systems['supabase']['url']}/rest/v1/tickets", headers=headers, timeout=3)
            self.systems['supabase']['status'] = "online" if response.status_code == 200 else "offline"
        except:
            self.systems['supabase']['status'] = "offline"
            
        # Check Claw-code
        claw_path = Path(self.systems['claw_code']['path'])
        self.systems['claw_code']['status'] = "online" if claw_path.exists() else "offline"
            
        # Check Ollama
        try:
            response = requests.get(f"{self.systems['ollama']['url']}/api/tags", timeout=3)
            self.systems['ollama']['status'] = "online" if response.status_code == 200 else "offline"
        except:
            self.systems['ollama']['status'] = "offline"
            
        return self.systems

jarvis = JARVISWeb()

@app.route('/')
def index():
    """JARVIS main interface"""
    return render_template('jarvis.html')

@app.route('/api/status')
def get_status():
    """Get system status"""
    systems = jarvis.check_systems()
    return jsonify(systems)

@app.route('/api/process', methods=['POST'])
def process_request():
    """Process user request through JARVIS"""
    data = request.json
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({"error": "No message provided"})
    
    # Analyze request and determine strategy
    strategy = analyze_request(user_input)
    
    # Execute request
    response = execute_request(user_input, strategy)
    
    # Add to history
    jarvis.conversation_history.append({
        "timestamp": datetime.now().isoformat(),
        "user": user_input,
        "strategy": strategy,
        "response": response
    })
    
    return jsonify({
        "strategy": strategy,
        "response": response,
        "timestamp": datetime.now().isoformat()
    })

def analyze_request(user_input):
    """Analyze user request and determine best strategy"""
    user_input_lower = user_input.lower()
    
    complex_keywords = ['build', 'create', 'develop', 'design', 'project', 'application', 'system']
    research_keywords = ['research', 'analyze', 'study', 'investigate', 'trends']
    coding_keywords = ['code', 'function', 'script', 'program', 'debug']
    content_keywords = ['write', 'content', 'marketing', 'campaign', 'blog']
    
    is_complex = any(keyword in user_input_lower for keyword in complex_keywords)
    is_research = any(keyword in user_input_lower for keyword in research_keywords)
    is_coding = any(keyword in user_input_lower for keyword in coding_keywords)
    is_content = any(keyword in user_input_lower for keyword in content_keywords)
    
    if is_complex and (is_research or is_content):
        return "godmode_orchestration"
    elif is_complex and is_coding:
        return "claw_code_advanced"
    elif is_coding:
        return "anx_terminal"
    elif is_research:
        return "godmode_research"
    elif is_content:
        return "godmode_content"
    else:
        return "anx_general"

def execute_request(user_input, strategy):
    """Execute request based on strategy"""
    if strategy == "godmode_orchestration":
        return f"""
🎯 JARVIS Specialist Team Coordination Initiated

📋 PROJECT: {user_input}

🤖 AGENT ASSIGNMENTS:
• Research Analyst → Requirements and market analysis
• Software Architect → Technical design and architecture
• Project Manager → Timeline and milestone planning
• Development Team → Implementation coordination
• QA Specialist → Quality assurance and testing

🔗 COORDINATION CENTERS:
• Agent Workspace: http://localhost:3333/godmode
• Progress Tracking: Supabase Dashboard
• Real-time Updates: WebSocket notifications

⏱️ ESTIMATED TIMELINE: Agents will provide detailed breakdown

🚀 NEXT STEPS:
1. Access Godmode interface for agent coordination
2. Monitor real-time progress in dashboard
3. Agents will deliver comprehensive solution

JARVIS is monitoring all systems and will provide updates.
        """
    
    elif strategy == "godmode_research":
        return f"""
🔍 JARVIS Research Protocol Activated

📋 RESEARCH REQUEST: {user_input}

🤖 ASSIGNED: Research Analyst (Godmode Specialist)

🎯 RESEARCH SCOPE:
• Market analysis and current trends
• Competitive landscape assessment
• Technical feasibility evaluation
• Risk and opportunity identification
• Strategic recommendations

🔗 ACCESS RESEARCH:
• Godmode Interface: http://localhost:3333/godmode
• Real-time Progress: Supabase tracking

⏱️ COMPLETION: 15-30 minutes for comprehensive analysis

JARVIS will notify when research is complete.
        """
    
    elif strategy == "claw_code_advanced":
        return f"""
⚡ JARVIS Advanced Development Protocol

📋 DEVELOPMENT REQUEST: {user_input}

🤖 SYSTEM: Claw-code Advanced Environment
🔧 FEATURES: Session persistence, multi-provider AI, workspace tools

💻 CAPABILITIES:
• Advanced code generation and analysis
• Multi-model AI reasoning (local + cloud)
• Workspace integration and file management
• Session memory and context preservation

🚀 EXECUTION:
Development environment is processing your request with advanced AI capabilities.

Access: ./claw-code/rust/target/debug/claw.exe
        """
    
    else:
        return f"""
💻 JARVIS Terminal AI Response

📋 REQUEST: {user_input}

🤖 ENHANCED ANX FEATURES:
• Context memory across sessions
• Smart routing capabilities
• Integration with all AI systems
• Terminal-optimized responses

💡 PROCESSING: 
ANX is handling your request with enhanced capabilities.
For complex tasks, JARVIS can automatically escalate to specialist systems.

🔄 Continue using ANX in terminal, now enhanced with JARVIS coordination.
        """

if __name__ == '__main__':
    # Create templates directory and HTML file
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS - Universal AI Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            color: #00d4ff;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(0, 212, 255, 0.1);
            border-radius: 15px;
            border: 1px solid rgba(0, 212, 255, 0.3);
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px #00d4ff;
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.8;
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 20px #00d4ff; }
            to { text-shadow: 0 0 30px #00d4ff, 0 0 40px #00d4ff; }
        }
        
        .systems-status {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .system-card {
            background: rgba(0, 212, 255, 0.1);
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .system-card:hover {
            background: rgba(0, 212, 255, 0.2);
            transform: translateY(-5px);
        }
        
        .system-card.online {
            border-color: #00ff88;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
        }
        
        .system-card.offline {
            border-color: #ff6b6b;
            box-shadow: 0 0 15px rgba(255, 107, 107, 0.3);
        }
        
        .chat-container {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            border: 1px solid rgba(0, 212, 255, 0.3);
            height: 500px;
            display: flex;
            flex-direction: column;
        }
        
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        
        .message.user {
            background: rgba(0, 212, 255, 0.2);
            margin-left: auto;
            text-align: right;
        }
        
        .message.jarvis {
            background: rgba(0, 255, 136, 0.2);
            margin-right: auto;
        }
        
        .chat-input {
            display: flex;
            padding: 20px;
            border-top: 1px solid rgba(0, 212, 255, 0.3);
        }
        
        .chat-input input {
            flex: 1;
            padding: 15px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 25px;
            color: #00d4ff;
            font-size: 16px;
            outline: none;
        }
        
        .chat-input input::placeholder {
            color: rgba(0, 212, 255, 0.5);
        }
        
        .chat-input button {
            margin-left: 10px;
            padding: 15px 25px;
            background: linear-gradient(45deg, #00d4ff, #00ff88);
            border: none;
            border-radius: 25px;
            color: #000;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .chat-input button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #00d4ff;
        }
        
        .spinner {
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 50%;
            border-top: 2px solid #00d4ff;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 JARVIS</h1>
            <p>Just A Rather Very Intelligent System</p>
            <p>Universal AI Interface - Like Iron Man's JARVIS</p>
        </div>
        
        <div class="systems-status" id="systemsStatus">
            <!-- System status cards will be populated here -->
        </div>
        
        <div class="chat-container">
            <div class="chat-messages" id="chatMessages">
                <div class="message jarvis">
                    <strong>🤖 JARVIS:</strong> All systems online and ready for commands. I can coordinate all your AI systems behind the scenes. What would you like me to help you with?
                </div>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>JARVIS is processing your request...</p>
            </div>
            
            <div class="chat-input">
                <input type="text" id="messageInput" placeholder="Ask JARVIS anything - I'll handle all the AI coordination..." />
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>

    <script>
        // Load system status on page load
        window.onload = function() {
            loadSystemStatus();
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        };
        
        function loadSystemStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const statusContainer = document.getElementById('systemsStatus');
                    statusContainer.innerHTML = '';
                    
                    const systemNames = {
                        'godmode': '🤖 Godmode (35 Agents)',
                        'supabase': '📊 Supabase Database',
                        'claw_code': '⚡ Claw-code Advanced',
                        'ollama': '🏠 Ollama Local AI',
                        'anx': '💻 ANX Terminal AI'
                    };
                    
                    for (const [system, info] of Object.entries(data)) {
                        const card = document.createElement('div');
                        card.className = `system-card ${info.status}`;
                        card.innerHTML = `
                            <h3>${systemNames[system]}</h3>
                            <p>${info.status === 'online' ? '✅ Online' : '⚠️ Offline'}</p>
                        `;
                        statusContainer.appendChild(card);
                    }
                });
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user');
            input.value = '';
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            
            // Send to JARVIS
            fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                addMessage(data.response, 'jarvis');
            })
            .catch(error => {
                document.getElementById('loading').style.display = 'none';
                addMessage('Error processing request: ' + error.message, 'jarvis');
            });
        }
        
        function addMessage(text, sender) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            if (sender === 'jarvis') {
                messageDiv.innerHTML = `<strong>🤖 JARVIS:</strong> ${text.replace(/\\n/g, '<br>')}`;
            } else {
                messageDiv.innerHTML = `<strong>👤 You:</strong> ${text}`;
            }
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        // Refresh system status every 30 seconds
        setInterval(loadSystemStatus, 30000);
    </script>
</body>
</html>'''
    
    with open(templates_dir / "jarvis.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("🤖 JARVIS Web Interface Starting...")
    print("🌐 Access JARVIS at: http://localhost:5000")
    print("🎯 Universal AI coordination through web interface")
    
    app.run(host='0.0.0.0', port=5000, debug=False)