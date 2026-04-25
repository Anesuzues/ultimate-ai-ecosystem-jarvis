# 🛠️ Manual Setup Steps for Your Supabase Project

I can see you have your API keys, but we need to get the correct project URL. Let's do this step by step:

## Step 1: Get Correct Supabase URL

1. **Go to your Supabase Dashboard**: https://supabase.com/dashboard
2. **Find your project** (should be named something like "ultimate-superagent")
3. **Go to Settings > API**
4. **Copy the exact "Project URL"** - it should look like:
   ```
   https://abcdefghijklmnop.supabase.co
   ```

## Step 2: Update Configuration

Edit `bot-anx/backend/.env.supabase` and replace the SUPABASE_URL with your correct URL:

```bash
# Replace this line with your actual Project URL from Supabase dashboard
SUPABASE_URL=https://your-correct-project-id.supabase.co

# Your keys (already set)
SUPABASE_ANON_KEY=your_supabase_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=sb_publishable_mWuSlSezHjKLYqmUS6JNsQ_6lXsZ7uT

# Your API tokens (already set)
CLICKUP_TOKEN=your_clickup_token_here
GITHUB_TOKEN=your_github_token_here
```

## Step 3: Apply Database Schema

1. **Go to your Supabase Dashboard**
2. **Click on "SQL Editor"** in the left sidebar
3. **Copy the entire contents** of the file `supabase-schema.sql` (it's open in your editor)
4. **Paste it into the SQL Editor**
5. **Click "Run"** to execute the schema

## Step 4: Test Connection

```powershell
python test-supabase-connection.py
```

## Step 5: Start Your Superagent

```powershell
.\start-cloud-superagent.bat
```

## What to Look For

### In Supabase Dashboard (Settings > API):
- **Project URL**: `https://[project-id].supabase.co`
- **anon key**: `eyJ...` (starts with eyJ)
- **service_role key**: `eyJ...` (starts with eyJ, different from anon)

### After Schema Application:
You should see these tables in your Supabase dashboard:
- `tickets` - ClickUp ticket storage
- `task_runs` - Workflow execution tracking
- `deployments` - Vercel deployment records
- `superagent_events` - Real-time event logging
- `workers` - AnesusBot worker management
- `quality_gates` - Quality assurance tracking
- `plan_cache` - AI plan caching

## Troubleshooting

### If URL is wrong:
- Check Supabase dashboard Settings > API
- Make sure it's `https://` not `http://`
- Project ID should be 20 characters long

### If keys are wrong:
- anon key should start with `eyJ`
- service_role key should start with `eyJ`
- Both should be very long (hundreds of characters)

### If schema fails:
- Make sure you're in the SQL Editor
- Copy the ENTIRE contents of supabase-schema.sql
- Run it all at once

## Next Steps After Setup

1. **Test connection**: `python test-supabase-connection.py`
2. **Start backend**: `.\start-cloud-superagent.bat`
3. **Monitor progress**: Check Supabase dashboard for real-time updates
4. **Create test ticket**: Add a ticket in ClickUp to see the workflow

**Once this is working, your Ultimate Superagent will be at full capacity! 🚀**