# Superagent Setup Guide
## Bot-ANX + Superpowers Integration

This guide shows you how to combine Bot-ANX's execution capabilities with Superpowers' systematic methodology to create a powerful "superagent" for development automation.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     SUPERAGENT SYSTEM                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐         ┌─────────────────┐               │
│  │   Superpowers   │◄───────►│    Bot-ANX      │               │
│  │  (Methodology)  │         │  (Execution)    │               │
│  │                 │         │                 │               │
│  │ • Brainstorming │         │ • ClickUp API   │               │
│  │ • Planning      │         │ • GitHub API    │               │
│  │ • TDD Workflow  │         │ • Vercel API    │               │
│  │ • Code Review   │         │ • Claude AI     │               │
│  │ • Git Worktrees │         │ • WebSocket     │               │
│  │ • Verification  │         │ • CLI Interface │               │
│  └─────────────────┘         └─────────────────┘               │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              Integration Layer                              │ │
│  │ • Skill Bridge  • Task Router  • State Sync  • CLI Wrapper │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

### System Requirements
- Python 3.11+
- Node.js 20+
- Yarn package manager
- MongoDB (local or Atlas)
- Git

### API Tokens Required
- **ClickUp API Token**: Personal token from ClickUp profile
- **GitHub Fine-grained PAT**: With `contents:rw`, `pull_requests:rw`
- **Vercel API Token**: From Vercel account settings
- **Emergent LLM Key**: For Claude Sonnet 4.5 access

## Installation Steps

### 1. Setup Bot-ANX Backend

```bash
# Navigate to bot-anx directory
cd bot-anx/backend

# Install Python dependencies
pip install -r requirements.txt --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

# Configure environment
cp .env .env.local
```

Edit `.env.local` with your credentials:
```bash
# MongoDB
MONGO_URL=mongodb://localhost:27017/autodev

# LLM Integration
EMERGENT_LLM_KEY=sk-emergent-your-key-here

# ClickUp Integration
CLICKUP_TOKEN=pk_your_clickup_token
CLICKUP_TEAM_ID=your_team_id
CLICKUP_LIST_ID=your_list_id  # Optional

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
USE_MOCK_APIS=true  # Start with mock mode
```

### 2. Setup Bot-ANX Frontend

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
yarn install

# Start development server
yarn start  # Runs on http://localhost:3000
```

### 3. Start Bot-ANX Backend

```bash
# Return to backend directory
cd ../backend

# Start FastAPI server
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### 4. Install Superpowers

Choose your platform:

#### Claude Code
```bash
/plugin install superpowers@claude-plugins-official
```

#### Cursor
```bash
/add-plugin superpowers
```

#### OpenCode
```bash
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
```

### 5. Add Integration Skills

Copy the integration skills to your Superpowers installation:

```bash
# Copy integration skills
cp -r skills/clickup-integration ~/.superpowers/skills/
cp -r skills/ticket-driven-development ~/.superpowers/skills/
cp -r skills/automated-deployment ~/.superpowers/skills/

# Or for workspace-level installation
cp -r skills/clickup-integration .superpowers/skills/
cp -r skills/ticket-driven-development .superpowers/skills/
cp -r skills/automated-deployment .superpowers/skills/
```

## Configuration

### 1. ClickUp Setup

1. **Get API Token**:
   - Go to ClickUp → Profile → Apps → Personal Token
   - Copy the token (starts with `pk_`)

2. **Find Team ID**:
   - Look at your ClickUp URL: `app.clickup.com/{team_id}/...`
   - Copy the team ID

3. **Optional List ID**:
   - To restrict to specific list, get list ID from URL

### 2. GitHub Setup

1. **Create Fine-grained PAT**:
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
   - Create token with repository access
   - Grant permissions: `contents:write`, `pull_requests:write`

2. **Repository Configuration**:
   - Set owner (your username or organization)
   - Set repository name

### 3. Vercel Setup

1. **Get API Token**:
   - Go to Vercel → Account Settings → Tokens
   - Create new token

2. **Find Project ID**:
   - Go to your project → Settings → General
   - Copy Project ID

### 4. Test Configuration

```bash
# Test Bot-ANX integrations
cd bot-anx/backend
python -m cli auth

# Should show all integrations as connected
```

## Usage Workflows

### Workflow 1: Manual Ticket Processing

```bash
# 1. Sync tickets from ClickUp
python -m cli sync
python -m cli tickets

# 2. Select a ticket and create plan
python -m cli plan CU-1001

# 3. Execute with approval
python -m cli run CU-1001 --approve

# 4. Monitor progress
python -m cli tail

# 5. Deploy when ready
python -m cli deploy <run_id>
```

### Workflow 2: Automated Superagent

```bash
# Run complete workflow with integration script
python superagent-integration.py

# Or specify specific ticket
python superagent-integration.py CU-1001
```

### Workflow 3: IDE Integration

In your IDE (Claude Code, Cursor, etc.):

1. **Start with Brainstorming**:
   ```
   I have a ClickUp ticket CU-1001 to implement. Let's use the ticket-driven-development workflow.
   ```

2. **The agent will**:
   - Invoke `clickup-integration` skill
   - Sync and analyze the ticket
   - Apply `brainstorming` methodology
   - Create detailed plan with `writing-plans`
   - Execute via Bot-ANX integration
   - Monitor and deploy automatically

## Safety Features

### Safe Mode (Recommended for Start)
- **Plan Approval**: Human approval required before execution
- **Deploy Approval**: Human approval required before deployment
- **Dry Run**: Simulates changes without real file modifications
- **Mock APIs**: Uses test data instead of real API calls

### Disable Safety (Production Use)
```bash
# In .env.local
SAFE_MODE=false
DRY_RUN=false
USE_MOCK_APIS=false
```

## Monitoring & Debugging

### Real-time Monitoring
```bash
# Stream live logs
python -m cli tail

# Check recent activity
python -m cli logs --limit 50

# Check integration status
python -m cli auth
```

### WebSocket Monitoring
- Bot-ANX provides WebSocket endpoint: `ws://localhost:8001/api/ws/logs`
- Real-time progress updates during execution
- Integration with IDE terminals

### Dashboard Monitoring
- Access React dashboard: http://localhost:3000
- Visual progress tracking
- Configuration management
- Deployment history

## Troubleshooting

### Common Issues

#### Bot-ANX Backend Won't Start
```bash
# Check MongoDB connection
mongosh mongodb://localhost:27017/autodev

# Check Python dependencies
pip install -r requirements.txt --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

# Check environment variables
python -c "from config import settings; print(settings)"
```

#### Integration Authentication Fails
```bash
# Verify tokens
python -m cli auth

# Test individual integrations
curl -H "Authorization: pk_your_token" https://api.clickup.com/api/v2/user
curl -H "Authorization: Bearer your_github_token" https://api.github.com/user
curl -H "Authorization: Bearer your_vercel_token" https://api.vercel.com/v2/user
```

#### Superpowers Skills Not Loading
```bash
# Check skill installation
ls ~/.superpowers/skills/  # or .superpowers/skills/

# Verify skill format
head ~/.superpowers/skills/clickup-integration/SKILL.md
```

### Debug Mode

Enable debug logging:
```bash
# In .env.local
LOG_LEVEL=DEBUG

# Restart backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload --log-level debug
```

## Advanced Configuration

### Custom Prompts
Modify Bot-ANX prompts in `backend/agents/prompts.py`:
```python
SYSTEM_PLANNER = (
    "You are AutoDev, enhanced with Superpowers methodology. "
    "Apply TDD principles and systematic planning..."
)
```

### Webhook Integration
Set up ClickUp webhooks to trigger automatic processing:
```python
# Add to backend/routes/webhooks.py
@router.post("/clickup-webhook")
async def handle_clickup_webhook(payload: dict):
    # Trigger superagent workflow on ticket updates
    pass
```

### Custom Skills
Create domain-specific skills:
```bash
mkdir skills/my-custom-skill
# Add SKILL.md with integration logic
```

## Performance Optimization

### Caching
- Bot-ANX caches Claude plans to reduce token usage
- MongoDB stores plan cache and execution history
- In-memory LRU cache for frequently accessed data

### Parallel Execution
- Use Superpowers' `dispatching-parallel-agents` for concurrent work
- Bot-ANX supports multiple simultaneous task runs
- WebSocket allows monitoring multiple executions

### Resource Management
- Configure MongoDB connection pooling
- Set appropriate timeouts for API calls
- Monitor memory usage during large executions

## Security Best Practices

### Token Management
- Store tokens in environment variables only
- Use fine-grained permissions (GitHub PATs)
- Rotate tokens regularly
- Never commit tokens to version control

### Network Security
- Run Bot-ANX backend on localhost only
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Monitor for suspicious activity

### Code Safety
- Always start with safe mode enabled
- Use dry run for testing changes
- Review generated code before deployment
- Maintain rollback procedures

## Success Metrics

Track these metrics to measure superagent effectiveness:

### Development Velocity
- Time from ticket creation to deployment
- Number of tickets processed per day
- Reduction in manual deployment steps

### Quality Metrics
- Test coverage maintained/improved
- Deployment success rate
- Post-deployment issue frequency
- Code review feedback quality

### Team Productivity
- Developer satisfaction scores
- Time saved on routine tasks
- Reduced context switching
- Improved focus on high-value work

## Next Steps

1. **Start with Mock Mode**: Test the complete workflow safely
2. **Enable One Integration**: Start with ClickUp only
3. **Add Real Deployments**: Enable GitHub and Vercel gradually
4. **Customize Workflows**: Adapt skills to your team's needs
5. **Scale Up**: Add more team members and repositories

## Support & Community

- **Bot-ANX Issues**: Create issues in the bot-anx repository
- **Superpowers Community**: Join the Discord server
- **Integration Help**: Check the integration-plan.md for detailed architecture
- **Custom Development**: Extend both systems for your specific needs

---

**Remember**: This integration combines the systematic methodology of Superpowers with the execution power of Bot-ANX. Start conservatively with safe mode enabled, then gradually increase automation as you build confidence in the system.