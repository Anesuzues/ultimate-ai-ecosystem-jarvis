---
name: clickup-integration
description: Integrate ClickUp ticket management with development workflow using Bot-ANX
---

## When to Use

This skill activates when:
- User mentions ClickUp tickets, tasks, or project management
- Working with ticket-driven development workflows
- Need to sync development work with ClickUp project tracking
- Managing ticket status updates and deployments

## Prerequisites

- Bot-ANX backend running (default: http://localhost:8001)
- ClickUp API token configured in Bot-ANX settings
- Team ID and optional List ID configured

## Workflow

### 1. Authentication Check
First, verify Bot-ANX integration status:
```bash
cd bot-anx/backend
python -m cli auth
```

### 2. Sync Tickets
Pull latest assigned tickets from ClickUp:
```bash
python -m cli sync
python -m cli tickets
```

### 3. Ticket Analysis
For each ticket, analyze:
- **Priority**: urgent, high, normal, low
- **Status**: open, in_progress, review, done, blocked
- **Acceptance Criteria**: Specific requirements to meet
- **Comments**: Additional context from team members
- **Tags**: Frontend, backend, bug, feature, etc.

### 4. Integration with Superpowers Workflow

#### 4.1 Brainstorming Phase
- Use ticket description and acceptance criteria as brainstorming input
- Refine requirements through Socratic questioning
- Validate understanding against ClickUp comments

#### 4.2 Planning Phase
- Generate detailed implementation plan
- Map plan steps to ticket acceptance criteria
- Ensure all requirements are covered

#### 4.3 Execution Phase
- Create task run in Bot-ANX:
```bash
python -m cli run <ticket_id> --approve
```
- Monitor progress via WebSocket:
```bash
python -m cli tail
```

#### 4.4 Deployment Phase
- Deploy completed work:
```bash
python -m cli deploy <run_id>
```
- Update ticket status in ClickUp automatically

### 5. Quality Gates

Before deployment, ensure:
- [ ] All acceptance criteria met
- [ ] Tests passing (TDD compliance)
- [ ] Code review completed
- [ ] Deployment URL accessible

### 6. Ticket Updates

Bot-ANX automatically:
- Updates ticket status to "in_progress" when execution starts
- Adds deployment URL as comment when deployed
- Closes ticket when deployment is successful

## Commands Reference

| Command | Purpose |
|---------|---------|
| `cli auth` | Check integration status |
| `cli sync` | Sync tickets from ClickUp |
| `cli tickets` | List available tickets |
| `cli plan <id>` | Generate execution plan |
| `cli run <id>` | Execute ticket with approval |
| `cli deploy <run_id>` | Deploy completed work |
| `cli logs` | View recent activity |
| `cli tail` | Stream live progress |

## Error Handling

### Common Issues:
1. **Authentication Failed**: Check ClickUp API token and team ID
2. **No Tickets Found**: Verify list ID or assignment filters
3. **Deployment Failed**: Check GitHub and Vercel credentials
4. **WebSocket Connection**: Ensure Bot-ANX backend is running

### Troubleshooting:
- Use mock mode for testing: Enable "Mock APIs" in Bot-ANX settings
- Check logs: `python -m cli logs` for recent activity
- Verify config: `python -m cli auth` for integration status

## Integration Benefits

- **Seamless Workflow**: Ticket → Code → Deploy → Update
- **Real-time Tracking**: Live progress via WebSocket
- **Quality Assurance**: Superpowers methodology + Bot-ANX execution
- **Team Visibility**: Automatic status updates in ClickUp
- **Audit Trail**: Complete history of development activities

## Best Practices

1. **Start with Mock Mode**: Test workflow without real API calls
2. **Use Safe Mode**: Require approval before execution and deployment
3. **Monitor Progress**: Keep WebSocket tail running during execution
4. **Verify Deployments**: Check deployment URLs before closing tickets
5. **Update Regularly**: Sync tickets frequently to stay current

## Red Flags

These thoughts mean you should use this skill:

| Thought | Reality |
|---------|---------|
| "Let me check the ClickUp ticket" | Use this skill to sync and analyze |
| "I need to update the ticket status" | Bot-ANX handles this automatically |
| "How do I deploy this change?" | Use the deployment workflow |
| "I want to track development progress" | WebSocket monitoring provides this |
| "This needs project management integration" | This skill provides full integration |