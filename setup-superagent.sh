#!/bin/bash
set -e

# Ultimate Superagent Setup Script
# Combines Superpowers + Bot-ANX + AnesusBot into one powerful system

echo "🚀 Ultimate Superagent Setup"
echo "============================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
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

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check for required tools
    local missing_tools=()
    
    if ! command -v git &> /dev/null; then
        missing_tools+=("git")
    fi
    
    if ! command -v node &> /dev/null; then
        missing_tools+=("node")
    fi
    
    if ! command -v npm &> /dev/null; then
        missing_tools+=("npm")
    fi
    
    if ! command -v python3 &> /dev/null; then
        missing_tools+=("python3")
    fi
    
    if ! command -v pip3 &> /dev/null; then
        missing_tools+=("pip3")
    fi
    
    if ! command -v cargo &> /dev/null; then
        missing_tools+=("cargo (Rust)")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        echo ""
        echo "Please install the missing tools and run this script again."
        echo ""
        echo "Installation guides:"
        echo "• Git: https://git-scm.com/downloads"
        echo "• Node.js: https://nodejs.org/en/download/"
        echo "• Python: https://www.python.org/downloads/"
        echo "• Rust: https://rustup.rs/"
        exit 1
    fi
    
    log_success "All prerequisites are installed"
}

# Setup Superpowers
setup_superpowers() {
    log_info "Setting up Superpowers methodology system..."
    
    # Superpowers is already cloned in the current directory
    if [ ! -d "skills" ]; then
        log_warning "Skills directory not found, creating basic structure"
        mkdir -p skills
    fi
    
    # Verify skills are available
    local skills_count=$(find skills -name "SKILL.md" | wc -l)
    log_success "Superpowers setup complete ($skills_count skills available)"
}

# Setup Bot-ANX
setup_bot_anx() {
    log_info "Setting up Bot-ANX integration system..."
    
    if [ ! -d "bot-anx" ]; then
        log_error "Bot-ANX directory not found. Please ensure it's cloned."
        return 1
    fi
    
    cd bot-anx/backend
    
    # Install Python dependencies
    log_info "Installing Bot-ANX Python dependencies..."
    pip3 install -r requirements.txt --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/ || {
        log_warning "Failed to install some dependencies, continuing..."
    }
    
    # Create environment file if it doesn't exist
    if [ ! -f ".env.local" ]; then
        log_info "Creating Bot-ANX environment configuration..."
        cp .env .env.local 2>/dev/null || {
            cat > .env.local << EOF
# MongoDB
MONGO_URL=mongodb://localhost:27017/autodev

# LLM Integration
EMERGENT_LLM_KEY=sk-emergent-your-key-here

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
USE_MOCK_APIS=true
EOF
        }
        log_warning "Please edit bot-anx/backend/.env.local with your API tokens"
    fi
    
    cd ../..
    log_success "Bot-ANX setup complete"
}

# Setup AnesusBot
setup_anesusbot() {
    log_info "Setting up AnesusBot high-performance runtime..."
    
    if [ ! -d "anesusbot" ]; then
        log_error "AnesusBot directory not found. Please ensure it's cloned."
        return 1
    fi
    
    cd anesusbot/rust
    
    # Build AnesusBot
    log_info "Building AnesusBot Rust workspace..."
    cargo build --workspace || {
        log_error "Failed to build AnesusBot"
        cd ../..
        return 1
    }
    
    # Test the build
    log_info "Testing AnesusBot installation..."
    if ./target/debug/claw --version &> /dev/null; then
        log_success "AnesusBot build successful"
    else
        log_warning "AnesusBot build completed but binary test failed"
    fi
    
    cd ../..
}

# Setup integration coordinator
setup_coordinator() {
    log_info "Setting up Superagent coordinator..."
    
    # Install rust-script if not available
    if ! command -v rust-script &> /dev/null; then
        log_info "Installing rust-script..."
        cargo install rust-script || {
            log_warning "Failed to install rust-script, coordinator will need manual compilation"
        }
    fi
    
    # Make coordinator executable
    chmod +x superagent-coordinator.rs
    
    # Create default configuration
    if [ ! -f "superagent-config.json" ]; then
        log_info "Creating default superagent configuration..."
        cat > superagent-config.json << EOF
{
  "superpowers": {
    "skills_path": "./skills",
    "methodology": "systematic",
    "tdd_enforced": true
  },
  "bot_anx": {
    "api_url": "http://localhost:8001/api",
    "clickup_token": "",
    "github_token": "",
    "vercel_token": "",
    "safe_mode": true
  },
  "anesusbot": {
    "binary_path": "./anesusbot/rust/target/debug/claw",
    "providers": ["anthropic", "openai"],
    "max_workers": 4,
    "plugins_enabled": true,
    "mcp_servers": ["filesystem", "git", "web"]
  },
  "integration": {
    "event_streaming": true,
    "quality_gates": "strict",
    "monitoring": "real_time",
    "coordination": "advanced"
  }
}
EOF
    fi
    
    log_success "Superagent coordinator setup complete"
}

# Create helper scripts
create_helper_scripts() {
    log_info "Creating helper scripts..."
    
    # Start script
    cat > start-superagent.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Ultimate Superagent System"
echo "======================================"

# Start Bot-ANX backend
echo "Starting Bot-ANX backend..."
cd bot-anx/backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload &
BOT_ANX_PID=$!
cd ../..

# Wait for Bot-ANX to start
sleep 5

# Start superagent coordinator
echo "Starting Superagent coordinator..."
./superagent-coordinator.rs start --config superagent-config.json &
COORDINATOR_PID=$!

echo ""
echo "✅ Superagent system started!"
echo "• Bot-ANX backend: http://localhost:8001"
echo "• Coordinator PID: $COORDINATOR_PID"
echo ""
echo "Press Ctrl+C to stop all services"

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping Superagent system..."
    kill $BOT_ANX_PID 2>/dev/null
    kill $COORDINATOR_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for processes
wait
EOF
    
    chmod +x start-superagent.sh
    
    # Status script
    cat > status-superagent.sh << 'EOF'
#!/bin/bash
echo "📊 Superagent System Status"
echo "=========================="

# Check Bot-ANX
if curl -s http://localhost:8001/api/config/status > /dev/null 2>&1; then
    echo "✅ Bot-ANX: Running (http://localhost:8001)"
else
    echo "❌ Bot-ANX: Not running"
fi

# Check AnesusBot
if [ -f "anesusbot/rust/target/debug/claw" ]; then
    echo "✅ AnesusBot: Binary available"
else
    echo "❌ AnesusBot: Binary not found"
fi

# Check Superpowers
skills_count=$(find skills -name "SKILL.md" 2>/dev/null | wc -l)
echo "✅ Superpowers: $skills_count skills available"

# Check coordinator
if [ -f "superagent-coordinator.rs" ]; then
    echo "✅ Coordinator: Available"
else
    echo "❌ Coordinator: Not found"
fi

echo ""
echo "Use './start-superagent.sh' to start the system"
EOF
    
    chmod +x status-superagent.sh
    
    # Process ticket script
    cat > process-ticket.sh << 'EOF'
#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Usage: $0 <ticket_id> [--safe-mode]"
    echo "Example: $0 CU-1001 --safe-mode"
    exit 1
fi

TICKET_ID=$1
SAFE_MODE=""

if [ "$2" = "--safe-mode" ]; then
    SAFE_MODE="--safe-mode"
fi

echo "🎫 Processing ticket: $TICKET_ID"
./superagent-coordinator.rs process-ticket $TICKET_ID $SAFE_MODE
EOF
    
    chmod +x process-ticket.sh
    
    log_success "Helper scripts created"
}

# Create documentation
create_documentation() {
    log_info "Creating documentation..."
    
    cat > SUPERAGENT_QUICKSTART.md << 'EOF'
# Superagent Quick Start Guide

## What is Superagent?

Superagent combines three powerful systems:
- **Superpowers**: Systematic development methodology
- **Bot-ANX**: ClickUp + GitHub + Vercel integration
- **AnesusBot**: High-performance Rust runtime

## Quick Start

### 1. Check System Status
```bash
./status-superagent.sh
```

### 2. Start the System
```bash
./start-superagent.sh
```

### 3. Process a Ticket
```bash
./process-ticket.sh CU-1001 --safe-mode
```

### 4. Monitor Status
```bash
./superagent-coordinator.rs status --follow
```

## Configuration

Edit `superagent-config.json` to configure:
- API tokens (ClickUp, GitHub, Vercel)
- System settings
- Integration options

## API Tokens Setup

1. **ClickUp**: Get token from Profile → Apps → Personal Token
2. **GitHub**: Create fine-grained PAT with repo access
3. **Vercel**: Get token from Account Settings → Tokens
4. **Anthropic**: Get API key from console.anthropic.com

Add these to `bot-anx/backend/.env.local`

## Troubleshooting

### Bot-ANX won't start
- Check MongoDB is running
- Verify Python dependencies installed
- Check `.env.local` configuration

### AnesusBot build fails
- Ensure Rust is installed (`rustup.rs`)
- Check internet connection for dependencies
- Try `cargo clean` then rebuild

### Integration issues
- Verify all API tokens are correct
- Check network connectivity
- Review logs in terminal output

## Advanced Usage

### Custom Workflows
```bash
./superagent-coordinator.rs workflow-create my-workflow \
  --steps "brainstorm,plan,implement,test,deploy" \
  --quality-gates strict
```

### Batch Processing
```bash
./superagent-coordinator.rs batch \
  --priority high \
  --max-concurrent 4
```

## Support

- Check logs for error messages
- Verify all prerequisites are installed
- Ensure API tokens have correct permissions
- Test individual systems before integration
EOF
    
    log_success "Documentation created"
}

# Main setup function
main() {
    echo "This script will set up the Ultimate Superagent system by combining:"
    echo "• Superpowers (systematic methodology)"
    echo "• Bot-ANX (ClickUp + GitHub + Vercel integration)"
    echo "• AnesusBot (high-performance Rust runtime)"
    echo ""
    
    read -p "Continue with setup? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
    
    echo ""
    
    check_prerequisites
    setup_superpowers
    setup_bot_anx
    setup_anesusbot
    setup_coordinator
    create_helper_scripts
    create_documentation
    
    echo ""
    log_success "🎉 Ultimate Superagent setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Edit bot-anx/backend/.env.local with your API tokens"
    echo "2. Run './status-superagent.sh' to check system status"
    echo "3. Run './start-superagent.sh' to start the system"
    echo "4. Read SUPERAGENT_QUICKSTART.md for usage guide"
    echo ""
    echo "For help: ./superagent-coordinator.rs --help"
}

# Run main function
main "$@"