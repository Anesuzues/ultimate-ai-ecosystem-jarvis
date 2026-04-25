-- Supabase Cloud Schema for Ultimate Superagent
-- Cloud-compatible version (no superuser commands)

-- Tickets table (replaces MongoDB tickets collection)
CREATE TABLE IF NOT EXISTS tickets (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    clickup_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'open',
    priority TEXT NOT NULL DEFAULT 'normal',
    acceptance_criteria JSONB DEFAULT '[]'::jsonb,
    comments JSONB DEFAULT '[]'::jsonb,
    tags JSONB DEFAULT '[]'::jsonb,
    assignee TEXT,
    url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Task runs table (replaces MongoDB task_runs collection)
CREATE TABLE IF NOT EXISTS task_runs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ticket_id TEXT REFERENCES tickets(clickup_id),
    status TEXT NOT NULL DEFAULT 'created',
    plan JSONB DEFAULT '{}'::jsonb,
    execution_results JSONB DEFAULT '{}'::jsonb,
    worker_assignments JSONB DEFAULT '[]'::jsonb,
    quality_gates JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Deployments table (replaces MongoDB deployments collection)
CREATE TABLE IF NOT EXISTS deployments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    task_run_id UUID REFERENCES task_runs(id),
    url TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    vercel_deployment_id TEXT,
    github_pr_number INTEGER,
    github_pr_url TEXT,
    verification_results JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Plan cache table (replaces MongoDB plan_cache collection)
CREATE TABLE IF NOT EXISTS plan_cache (
    cache_key TEXT PRIMARY KEY,
    plan JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '24 hours')
);

-- Superagent events table (new - for real-time monitoring)
CREATE TABLE IF NOT EXISTS superagent_events (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    event_type TEXT NOT NULL,
    ticket_id TEXT,
    worker_id TEXT,
    task_id TEXT,
    data JSONB DEFAULT '{}'::jsonb,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Workers table (new - for AnesusBot worker management)
CREATE TABLE IF NOT EXISTS workers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    worker_id TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL DEFAULT 'idle',
    current_task_id TEXT,
    capabilities JSONB DEFAULT '[]'::jsonb,
    performance_metrics JSONB DEFAULT '{}'::jsonb,
    last_heartbeat TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Quality gates table (new - for tracking quality enforcement)
CREATE TABLE IF NOT EXISTS quality_gates (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    task_run_id UUID REFERENCES task_runs(id),
    gate_type TEXT NOT NULL, -- 'tdd', 'code_review', 'security', 'performance'
    status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'passed', 'failed'
    results JSONB DEFAULT '{}'::jsonb,
    executed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tickets_clickup_id ON tickets(clickup_id);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_priority ON tickets(priority);
CREATE INDEX IF NOT EXISTS idx_task_runs_ticket_id ON task_runs(ticket_id);
CREATE INDEX IF NOT EXISTS idx_task_runs_status ON task_runs(status);
CREATE INDEX IF NOT EXISTS idx_deployments_task_run_id ON deployments(task_run_id);
CREATE INDEX IF NOT EXISTS idx_deployments_status ON deployments(status);
CREATE INDEX IF NOT EXISTS idx_events_ticket_id ON superagent_events(ticket_id);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON superagent_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_type ON superagent_events(event_type);
CREATE INDEX IF NOT EXISTS idx_workers_status ON workers(status);
CREATE INDEX IF NOT EXISTS idx_quality_gates_task_run_id ON quality_gates(task_run_id);

-- Functions for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for automatic timestamp updates
DROP TRIGGER IF EXISTS update_tickets_updated_at ON tickets;
CREATE TRIGGER update_tickets_updated_at BEFORE UPDATE ON tickets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_task_runs_updated_at ON task_runs;
CREATE TRIGGER update_task_runs_updated_at BEFORE UPDATE ON task_runs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_deployments_updated_at ON deployments;
CREATE TRIGGER update_deployments_updated_at BEFORE UPDATE ON deployments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Views for common queries
CREATE OR REPLACE VIEW active_workflows AS
SELECT 
    t.clickup_id,
    t.name as ticket_name,
    t.priority,
    tr.id as task_run_id,
    tr.status as task_status,
    d.url as deployment_url,
    d.status as deployment_status,
    tr.created_at,
    tr.updated_at
FROM tickets t
LEFT JOIN task_runs tr ON t.clickup_id = tr.ticket_id
LEFT JOIN deployments d ON tr.id = d.task_run_id
WHERE tr.status NOT IN ('completed', 'failed')
ORDER BY tr.created_at DESC;

CREATE OR REPLACE VIEW workflow_metrics AS
SELECT 
    DATE_TRUNC('day', tr.created_at) as date,
    COUNT(*) as total_workflows,
    COUNT(CASE WHEN tr.status = 'completed' THEN 1 END) as completed,
    COUNT(CASE WHEN tr.status = 'failed' THEN 1 END) as failed,
    AVG(EXTRACT(EPOCH FROM (tr.updated_at - tr.created_at))/60) as avg_duration_minutes
FROM task_runs tr
GROUP BY DATE_TRUNC('day', tr.created_at)
ORDER BY date DESC;

-- Sample data for testing
INSERT INTO tickets (clickup_id, name, description, priority, acceptance_criteria) VALUES
('CU-1001', 'Add dark mode toggle', 'Implement dark mode for the application', 'high', 
 '["Toggle visible in settings", "Persists on reload", "No FOUC"]'::jsonb),
('CU-1002', 'Fix webhook validation', 'Fix HMAC signature validation bug', 'urgent',
 '["Signature uses raw bytes", "Unit tests added", "No regression"]'::jsonb),
('CU-1003', 'Add deployment badge', 'Show Vercel deployment status in README', 'normal',
 '["Badge in README", "Links to latest deployment"]'::jsonb)
ON CONFLICT (clickup_id) DO NOTHING;

-- Enable Row Level Security (RLS) - Supabase handles this automatically
-- The RLS policies will be managed through the Supabase dashboard

-- Note: Real-time subscriptions are enabled by default in Supabase
-- No need to manually configure publication settings