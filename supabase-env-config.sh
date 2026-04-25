#!/bin/bash
# Supabase Environment Configuration for Ultimate Superagent

echo "🗄️ Configuring Supabase for Ultimate Superagent"
echo "=============================================="

# Create updated .env.local for Bot-ANX with Supabase
cat > bot-anx/backend/.env.supabase << 'EOF'
# Supabase Configuration (replaces MongoDB)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Database URL (for any direct SQL needs)
DATABASE_URL=postgresql://postgres:your-password@db.your-project.supabase.co:5432/postgres

# LLM Integration
EMERGENT_LLM_KEY=sk-emergent-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# ClickUp Integration
CLICKUP_TOKEN=pk_your_clickup_token
CLICKUP_TEAM_ID=your_team_id
CLICKUP_LIST_ID=your_list_id

# GitHub Integration
GITHUB_TOKEN=ghp_your_github_token
GITHUB_OWNER=your_username
GITHUB_REPO=your_repo_name

# Vercel Integration
VERCEL_TOKEN=your_vercel_token
VERCEL_PROJECT_ID=your_project_id

# Safety Settings
SAFE_MODE=true
DRY_RUN=true
USE_MOCK_APIS=false

# Real-time Features
ENABLE_REALTIME=true
WEBSOCKET_URL=wss://your-project.supabase.co/realtime/v1/websocket

# Caching
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600

# Monitoring
LOG_LEVEL=INFO
ENABLE_METRICS=true
EOF

echo "✅ Created Supabase environment configuration"

# Update superagent-config.json for Supabase
cat > superagent-config-supabase.json << 'EOF'
{
  "superpowers": {
    "skills_path": "./skills",
    "methodology": "systematic",
    "tdd_enforced": true
  },
  "bot_anx": {
    "api_url": "http://localhost:8001/api",
    "database": {
      "type": "supabase",
      "url": "https://your-project.supabase.co",
      "anon_key": "your-anon-key",
      "service_role_key": "your-service-role-key"
    },
    "clickup_token": "",
    "github_token": "",
    "vercel_token": "",
    "safe_mode": true,
    "realtime_enabled": true
  },
  "anesusbot": {
    "binary_path": "./anesusbot/rust/target/debug/claw",
    "providers": ["anthropic", "openai"],
    "max_workers": 4,
    "plugins_enabled": true,
    "mcp_servers": ["filesystem", "git", "web", "supabase"]
  },
  "integration": {
    "event_streaming": true,
    "quality_gates": "strict",
    "monitoring": "real_time",
    "coordination": "advanced",
    "database": "supabase",
    "realtime_subscriptions": [
      "tickets",
      "task_runs", 
      "deployments",
      "superagent_events",
      "workers"
    ]
  }
}
EOF

echo "✅ Created Supabase-enabled superagent configuration"

# Install Supabase dependencies
echo "📦 Installing Supabase dependencies..."

# Python dependencies for Bot-ANX
cat > bot-anx/backend/requirements-supabase.txt << 'EOF'
# Existing requirements
fastapi
uvicorn
pydantic
httpx
typer
websockets
python-dotenv

# Supabase integration
supabase>=2.0.0
postgrest-py>=0.10.0
realtime-py>=0.1.0
gotrue-py>=1.0.0

# Additional utilities
asyncpg>=0.28.0
sqlalchemy>=2.0.0
alembic>=1.12.0
EOF

# Rust dependencies for AnesusBot Supabase integration
cat > anesusbot/rust/Cargo-supabase.toml << 'EOF'
[dependencies]
# Existing dependencies...

# Supabase integration
postgrest = "1.0"
tokio-postgres = "0.7"
serde_json = "1.0"
uuid = { version = "1.0", features = ["v4", "serde"] }
chrono = { version = "0.4", features = ["serde"] }

# Real-time subscriptions
tokio-tungstenite = "0.20"
futures-util = "0.3"
EOF

echo "✅ Created dependency files for Supabase integration"

# Create Supabase setup script
cat > setup-supabase.sh << 'EOF'
#!/bin/bash
echo "🚀 Setting up Supabase for Ultimate Superagent"

# Install Supabase CLI
if ! command -v supabase &> /dev/null; then
    echo "Installing Supabase CLI..."
    npm install -g supabase
fi

# Initialize Supabase project (if not already done)
if [ ! -f "supabase/config.toml" ]; then
    echo "Initializing Supabase project..."
    supabase init
fi

# Start local Supabase (for development)
echo "Starting local Supabase..."
supabase start

# Apply schema
echo "Applying database schema..."
supabase db reset

# Get local connection details
echo ""
echo "✅ Supabase setup complete!"
echo ""
echo "Local development URLs:"
supabase status

echo ""
echo "Update your .env.supabase file with these values:"
echo "SUPABASE_URL=http://localhost:54321"
echo "SUPABASE_ANON_KEY=[anon key from supabase status]"
echo "SUPABASE_SERVICE_ROLE_KEY=[service_role key from supabase status]"
EOF

chmod +x setup-supabase.sh

echo ""
echo "🎉 Supabase configuration complete!"
echo ""
echo "Next steps:"
echo "1. Run './setup-supabase.sh' to initialize Supabase"
echo "2. Update .env.supabase with your Supabase credentials"
echo "3. Apply the schema: 'supabase db reset'"
echo "4. Start Bot-ANX with Supabase: 'cd bot-anx/backend && python -m pip install -r requirements-supabase.txt'"
echo ""
echo "Supabase advantages:"
echo "✅ Real-time subscriptions for live updates"
echo "✅ Managed PostgreSQL (no Docker needed)"
echo "✅ Built-in authentication and RLS"
echo "✅ Edge functions for serverless compute"
echo "✅ File storage for artifacts"
echo "✅ Free tier with generous limits"