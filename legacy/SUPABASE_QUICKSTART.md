# 🚀 Supabase Setup for Ultimate Superagent - Quick Start

## What You're Getting

**Supabase replaces MongoDB** and gives you:
- ✅ **Managed PostgreSQL** - No Docker containers needed
- ✅ **Real-time subscriptions** - Live updates as workflows progress
- ✅ **Auto-generated REST API** - Instant CRUD operations
- ✅ **Built-in dashboard** - Visual interface for monitoring
- ✅ **Authentication & security** - Row-level security policies
- ✅ **Free tier** - Generous limits for development

## Quick Setup (Windows)

### Option 1: Automated Setup (Recommended)
```powershell
# Run the PowerShell setup script
.\setup-supabase-windows.ps1
```

### Option 2: Manual Setup
```powershell
# 1. Install Supabase CLI
npm install -g supabase

# 2. Initialize project
supabase init

# 3. Start local development
supabase start

# 4. Apply schema
supabase db reset
```

## What Gets Created

### 1. **Database Tables**
- `tickets` - ClickUp ticket storage
- `task_runs` - Workflow execution tracking
- `deployments` - Vercel deployment records
- `superagent_events` - Real-time event logging
- `workers` - AnesusBot worker management
- `quality_gates` - Quality assurance tracking
- `plan_cache` - AI plan caching

### 2. **Configuration Files**
- `bot-anx/backend/.env.supabase` - Environment variables
- `superagent-config-supabase.json` - System configuration
- `test-supabase-connection.py` - Connection test script

### 3. **Startup Scripts**
- `start-supabase.bat` - Start Supabase only
- `start-superagent-supabase.bat` - Start complete system

## Testing Your Setup

### 1. Test Database Connection
```bash
python test-supabase-connection.py
```

**Expected Output:**
```
🧪 Testing Supabase connection...
✅ Connected to Supabase: http://localhost:54321
✅ Database query successful
✅ Test data inserted successfully
✅ Real-time endpoint: ws://localhost:54321/realtime/v1/websocket

🎉 Supabase setup successful!
```

### 2. Check Supabase Dashboard
Open: http://localhost:54323

You should see:
- **Table Editor** - Browse your data
- **SQL Editor** - Run custom queries
- **API Docs** - Auto-generated documentation
- **Authentication** - User management
- **Storage** - File management

### 3. Test API Endpoints
```bash
# Get all tickets
curl http://localhost:54321/rest/v1/tickets

# Get specific ticket
curl http://localhost:54321/rest/v1/tickets?clickup_id=eq.TEST-001

# Real-time subscription test (in browser console)
const supabase = createClient('http://localhost:54321', 'your-anon-key')
supabase.channel('test').on('postgres_changes', {
  event: '*', schema: 'public', table: 'tickets'
}, (payload) => console.log('Change received!', payload)).subscribe()
```

## Integration with Bot-ANX

### 1. **Replace MongoDB Calls**
The `supabase_client.py` provides a drop-in replacement:

```python
# OLD (MongoDB)
from db import get_db
db = get_db()
await db.tickets.insert_one(ticket_data)

# NEW (Supabase)
from supabase_client import get_supabase_client
client = get_supabase_client()
await client.store_ticket(ticket_data)
```

### 2. **Real-time Updates**
```python
# Setup real-time subscriptions
def handle_realtime_event(payload):
    print(f"Real-time update: {payload}")

client.setup_realtime_subscriptions(handle_realtime_event)
```

### 3. **Environment Variables**
Update `bot-anx/backend/.env.supabase`:
```bash
# Required
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# Your API tokens
CLICKUP_TOKEN=pk_your_clickup_token
GITHUB_TOKEN=ghp_your_github_token
VERCEL_TOKEN=your_vercel_token
ANTHROPIC_API_KEY=sk-ant-your_key_here
```

## Starting Your Superagent

### Complete System Startup
```bash
# Start everything at once
start-superagent-supabase.bat
```

This starts:
1. **Supabase** (PostgreSQL + API + Dashboard)
2. **Bot-ANX Backend** (FastAPI server)
3. **Superagent Coordinator** (Rust coordination system)

### Individual Services
```bash
# Just Supabase
start-supabase.bat

# Just Bot-ANX (after Supabase is running)
cd bot-anx/backend
uvicorn server:app --port 8001 --reload

# Just Coordinator (after both are running)
./superagent-coordinator.rs start --config superagent-config-supabase.json
```

## Real-time Monitoring

### 1. **Supabase Dashboard**
- **URL**: http://localhost:54323
- **View**: Live data changes, query performance, API usage

### 2. **Real-time Events**
Watch live updates in the dashboard:
- New tickets synced from ClickUp
- Task runs created and updated
- Workers spawned and status changes
- Deployments started and completed

### 3. **API Monitoring**
```bash
# Watch API calls in real-time
curl -N http://localhost:54321/rest/v1/superagent_events?select=*&order=timestamp.desc&limit=10
```

## Production Deployment

### 1. **Create Supabase Project**
1. Go to https://supabase.com/dashboard
2. Create new project
3. Get your project URL and keys
4. Update environment variables

### 2. **Deploy Schema**
```bash
# Push local schema to production
supabase db push

# Or apply migrations
supabase db reset --db-url "your-production-url"
```

### 3. **Update Configuration**
Replace localhost URLs with production URLs in:
- `bot-anx/backend/.env.supabase`
- `superagent-config-supabase.json`

## Troubleshooting

### Common Issues

#### 1. **Supabase won't start**
```bash
# Check Docker is running
docker --version

# Check ports aren't in use
netstat -an | findstr :54321
netstat -an | findstr :54322
netstat -an | findstr :54323

# Reset Supabase
supabase stop
supabase start
```

#### 2. **Connection failed**
```bash
# Check Supabase status
supabase status

# Test direct connection
curl http://localhost:54321/rest/v1/

# Check environment variables
python -c "import os; print(os.environ.get('SUPABASE_URL'))"
```

#### 3. **Python packages missing**
```bash
# Install Supabase client
pip install supabase

# Install additional packages
pip install postgrest-py realtime-py gotrue-py
```

#### 4. **Real-time not working**
- Check WebSocket URL in environment
- Verify anon key has correct permissions
- Test WebSocket connection in browser console

### Getting Help

1. **Check Supabase logs**: `supabase logs`
2. **Check Bot-ANX logs**: Look at uvicorn output
3. **Test individual components**: Use test scripts
4. **Verify configuration**: Check all environment variables

## Benefits Over MongoDB

| Feature | MongoDB | Supabase | Winner |
|---------|---------|----------|---------|
| **Setup** | Docker + Config | `supabase start` | ✅ **Supabase** |
| **Real-time** | Manual WebSocket | Built-in subscriptions | ✅ **Supabase** |
| **API** | Custom endpoints | Auto-generated REST | ✅ **Supabase** |
| **Dashboard** | Build yourself | Included | ✅ **Supabase** |
| **Authentication** | Manual | Built-in | ✅ **Supabase** |
| **Scaling** | Manual | Auto-scaling | ✅ **Supabase** |
| **Monitoring** | Custom | Built-in | ✅ **Supabase** |
| **Backups** | Manual | Automatic | ✅ **Supabase** |

## Next Steps

1. ✅ **Setup Complete** - Run the setup script
2. 🔧 **Configure APIs** - Add your ClickUp, GitHub, Vercel tokens
3. 🧪 **Test Integration** - Run test scripts
4. 🚀 **Start System** - Launch your superagent
5. 📊 **Monitor Progress** - Watch real-time updates
6. 🌐 **Deploy Production** - Move to Supabase cloud

**Your Ultimate Superagent is now powered by Supabase! 🎉**