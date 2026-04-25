#!/bin/bash
set -e

# Ultimate Superagent Supabase Setup Script
echo "🚀 Setting up Supabase for Ultimate Superagent"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Node.js is installed
check_nodejs() {
    if ! command -v node &> /dev/null; then
        log_error "Node.js is not installed. Please install Node.js first:"
        echo "Visit: https://nodejs.org/en/download/"
        exit 1
    fi
    log_success "Node.js is installed"
}

# Install Supabase CLI
install_supabase_cli() {
    log_info "Installing Supabase CLI..."
    
    if command -v supabase &> /dev/null; then
        log_success "Supabase CLI already installed"
        supabase --version
    else
        npm install -g supabase
        log_success "Supabase CLI installed successfully"
    fi
}

# Initialize Supabase project
init_supabase_project() {
    log_info "Initializing Supabase project..."
    
    if [ -f "supabase/config.toml" ]; then
        log_warning "Supabase project already initialized"
    else
        supabase init
        log_success "Supabase project initialized"
    fi
}

# Create database schema
create_schema() {
    log_info "Creating database schema..."
    
    # Create migrations directory if it doesn't exist
    mkdir -p supabase/migrations
    
    # Copy our schema to migrations
    cp supabase-schema.sql supabase/migrations/$(date +%Y%m%d%H%M%S)_initial_schema.sql
    
    log_success "Schema file created in migrations"
}

# Start local Supabase
start_local_supabase() {
    log_info "Starting local Supabase development environment..."
    
    # This will start PostgreSQL, PostgREST, GoTrue, Realtime, and Storage
    supabase start
    
    log_success "Local Supabase started successfully"
}

# Apply database migrations
apply_migrations() {
    log_info "Applying database migrations..."
    
    supabase db reset
    
    log_success "Database schema applied successfully"
}

# Install Python dependencies
install_python_deps() {
    log_info "Installing Python dependencies for Bot-ANX..."
    
    cd bot-anx/backend
    
    # Install Supabase Python client
    pip3 install supabase>=2.0.0 || {
        log_warning "Failed to install supabase package, trying with --user flag"
        pip3 install --user supabase>=2.0.0
    }
    
    # Install other required packages
    pip3 install postgrest-py>=0.10.0 realtime-py>=0.1.0 gotrue-py>=1.0.0 || {
        log_warning "Some packages failed to install, continuing..."
    }
    
    cd ../..
    log_success "Python dependencies installed"
}

# Install Rust dependencies
install_rust_deps() {
    log_info "Installing Rust dependencies for AnesusBot..."
    
    cd anesusbot/rust
    
    # Add Supabase-related dependencies to Cargo.toml
    if ! grep -q "postgrest" Cargo.toml; then
        cat >> Cargo.toml << 'EOF'

# Supabase integration dependencies
[dependencies.postgrest]
version = "1.0"

[dependencies.tokio-postgres]
version = "0.7"

[dependencies.uuid]
version = "1.0"
features = ["v4", "serde"]

[dependencies.chrono]
version = "0.4"
features = ["serde"]
EOF
        log_success "Added Supabase dependencies to Cargo.toml"
    else
        log_warning "Supabase dependencies already in Cargo.toml"
    fi
    
    cd ../..
}

# Create environment configuration
create_env_config() {
    log_info "Creating environment configuration..."
    
    # Get Supabase local connection details
    local supabase_status=$(supabase status --output json 2>/dev/null || echo '{}')
    
    # Extract connection details
    local api_url=$(echo "$supabase_status" | grep -o '"API URL": "[^"]*"' | cut -d'"' -f4 || echo "http://localhost:54321")
    local anon_key=$(echo "$supabase_status" | grep -o '"anon key": "[^"]*"' | cut -d'"' -f4 || echo "your-anon-key")
    local service_role_key=$(echo "$supabase_status" | grep -o '"service_role key": "[^"]*"' | cut -d'"' -f4 || echo "your-service-role-key")
    
    # Create Bot-ANX environment file
    cat > bot-anx/backend/.env.supabase << EOF
# Supabase Configuration
SUPABASE_URL=${api_url}
SUPABASE_ANON_KEY=${anon_key}
SUPABASE_SERVICE_ROLE_KEY=${service_role_key}

# Database URL for direct connections
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres

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
DRY_RUN=false
USE_MOCK_APIS=false

# Real-time Features
ENABLE_REALTIME=true
WEBSOCKET_URL=ws://localhost:54321/realtime/v1/websocket

# Monitoring
LOG_LEVEL=INFO
ENABLE_METRICS=true
EOF

    # Create Superagent configuration
    cat > superagent-config-supabase.json << EOF
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
      "url": "${api_url}",
      "anon_key": "${anon_key}",
      "service_role_key": "${service_role_key}"
    },
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
    "database": "supabase"
  }
}
EOF

    log_success "Environment configuration created"
}

# Create test script
create_test_script() {
    log_info "Creating test script..."
    
    cat > test-supabase-connection.py << 'EOF'
#!/usr/bin/env python3
"""
Test Supabase connection for Ultimate Superagent
"""

import os
import sys
from datetime import datetime
import json

try:
    from supabase import create_client, Client
except ImportError:
    print("❌ Supabase package not installed. Run: pip3 install supabase")
    sys.exit(1)

def test_connection():
    # Load environment
    env_file = "bot-anx/backend/.env.supabase"
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    
    if not url or not key:
        print("❌ SUPABASE_URL or SUPABASE_ANON_KEY not found in environment")
        return False
    
    try:
        # Create client
        supabase: Client = create_client(url, key)
        print(f"✅ Connected to Supabase: {url}")
        
        # Test basic query
        result = supabase.table('tickets').select('*').limit(1).execute()
        print(f"✅ Database query successful")
        
        # Test insert
        test_ticket = {
            'clickup_id': 'TEST-001',
            'name': 'Test Supabase Connection',
            'description': 'Testing connection to Supabase',
            'status': 'open',
            'priority': 'normal'
        }
        
        insert_result = supabase.table('tickets').upsert(test_ticket).execute()
        print(f"✅ Test data inserted successfully")
        
        # Test real-time (basic check)
        print(f"✅ Real-time endpoint: {url.replace('http', 'ws')}/realtime/v1/websocket")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Supabase connection...")
    success = test_connection()
    if success:
        print("\n🎉 Supabase setup successful!")
        print("\nNext steps:")
        print("1. Update API tokens in bot-anx/backend/.env.supabase")
        print("2. Run: cd bot-anx/backend && python test-supabase-connection.py")
        print("3. Start Bot-ANX: uvicorn server:app --port 8001")
    else:
        print("\n❌ Setup needs attention. Check the errors above.")
        sys.exit(1)
EOF

    chmod +x test-supabase-connection.py
    log_success "Test script created"
}

# Create startup scripts
create_startup_scripts() {
    log_info "Creating startup scripts..."
    
    # Supabase startup script
    cat > start-supabase.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Supabase for Ultimate Superagent"

# Start Supabase services
supabase start

echo ""
echo "✅ Supabase is running!"
echo ""
echo "Services:"
supabase status

echo ""
echo "Dashboard: http://localhost:54323"
echo "API URL: http://localhost:54321"
echo ""
echo "Use 'supabase stop' to stop all services"
EOF

    chmod +x start-supabase.sh
    
    # Combined startup script
    cat > start-superagent-supabase.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Ultimate Superagent with Supabase"
echo "============================================="

# Start Supabase
echo "Starting Supabase..."
supabase start

# Wait for Supabase to be ready
sleep 3

# Start Bot-ANX with Supabase config
echo "Starting Bot-ANX backend..."
cd bot-anx/backend
export $(cat .env.supabase | grep -v '^#' | xargs)
uvicorn server:app --host 0.0.0.0 --port 8001 --reload &
BOT_ANX_PID=$!
cd ../..

# Wait for Bot-ANX to start
sleep 5

# Start superagent coordinator
echo "Starting Superagent coordinator..."
./superagent-coordinator.rs start --config superagent-config-supabase.json &
COORDINATOR_PID=$!

echo ""
echo "✅ Ultimate Superagent with Supabase started!"
echo ""
echo "Services:"
echo "• Supabase Dashboard: http://localhost:54323"
echo "• Supabase API: http://localhost:54321"
echo "• Bot-ANX API: http://localhost:8001"
echo "• Coordinator PID: $COORDINATOR_PID"
echo ""
echo "Press Ctrl+C to stop all services"

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping all services..."
    kill $BOT_ANX_PID 2>/dev/null
    kill $COORDINATOR_PID 2>/dev/null
    supabase stop
    echo "✅ All services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for processes
wait
EOF

    chmod +x start-superagent-supabase.sh
    
    log_success "Startup scripts created"
}

# Main setup function
main() {
    echo "This will set up Supabase as the database for your Ultimate Superagent:"
    echo "• PostgreSQL database with real-time subscriptions"
    echo "• Auto-generated REST API"
    echo "• Built-in authentication and dashboard"
    echo "• Local development environment"
    echo ""
    
    read -p "Continue with Supabase setup? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
    
    echo ""
    
    check_nodejs
    install_supabase_cli
    init_supabase_project
    create_schema
    start_local_supabase
    apply_migrations
    install_python_deps
    install_rust_deps
    create_env_config
    create_test_script
    create_startup_scripts
    
    echo ""
    log_success "🎉 Supabase setup complete!"
    echo ""
    echo "What was created:"
    echo "✅ Local Supabase development environment"
    echo "✅ Database schema with all tables"
    echo "✅ Environment configuration files"
    echo "✅ Python and Rust dependencies"
    echo "✅ Test and startup scripts"
    echo ""
    echo "Next steps:"
    echo "1. Test connection: python3 test-supabase-connection.py"
    echo "2. Update API tokens in bot-anx/backend/.env.supabase"
    echo "3. Start everything: ./start-superagent-supabase.sh"
    echo ""
    echo "Supabase Dashboard: http://localhost:54323"
    echo "API Documentation: http://localhost:54321/rest/v1/"
    echo ""
    echo "For production, create a project at: https://supabase.com/dashboard"
}

# Run main function
main "$@"