---
name: automated-deployment
description: Automated deployment pipeline using Bot-ANX with Vercel, GitHub, and ClickUp integration
---

## When to Use

This skill activates when:
- Ready to deploy completed development work
- Need automated PR creation and merging
- Want Vercel deployment with status tracking
- Require ClickUp ticket updates post-deployment

## Prerequisites

- Bot-ANX backend running with integrations configured
- GitHub fine-grained PAT with `contents:rw`, `pull_requests:rw`
- Vercel API token and project ID
- ClickUp API token for status updates

## Deployment Workflow

### Phase 1: Pre-Deployment Validation

#### 1.1 Verify Readiness
Before deployment, ensure:
- [ ] All tests passing locally
- [ ] Code review completed
- [ ] Acceptance criteria met
- [ ] No merge conflicts

#### 1.2 Check Integration Status
```bash
cd bot-anx/backend
python -m cli auth
```

Verify all integrations are active:
- ✅ ClickUp: Connected with valid token
- ✅ GitHub: Repository access configured
- ✅ Vercel: Project ID and token set
- ✅ Bot-ANX: Backend running and responsive

### Phase 2: Deployment Execution

#### 2.1 Initiate Deployment
```bash
# Deploy completed task run
python -m cli deploy <run_id>
```

#### 2.2 Monitor Progress
Stream deployment logs:
```bash
# Real-time deployment monitoring
python -m cli tail
```

Expected deployment sequence:
1. **Branch Creation**: `autodev/<ticket_id>`
2. **PR Creation**: With generated title and description
3. **PR Merge**: Automatic squash merge to main
4. **Vercel Trigger**: Deployment initiated
5. **Status Monitoring**: Track deployment progress
6. **ClickUp Update**: Ticket status and URL updated

### Phase 3: Deployment Stages

#### 3.1 GitHub Integration
Bot-ANX automatically:
- Creates feature branch from main
- Commits changes with descriptive message
- Opens PR with:
  - Title: Ticket name
  - Body: Acceptance criteria and changes
  - Labels: Based on ticket tags

#### 3.2 Vercel Deployment
Deployment process:
- Triggered by main branch merge
- Build process monitored
- Deployment URL generated
- Status tracked until ready

#### 3.3 ClickUp Integration
Ticket updates:
- Status changed to "deployed" or "done"
- Deployment URL added as comment
- Completion timestamp recorded

### Phase 4: Verification & Monitoring

#### 4.1 Deployment Verification
**Invoke: `verification-before-completion` skill**

Verify deployment success:
```bash
# Check deployment status
curl -I <deployment_url>

# Verify functionality
# Test key user flows
# Check acceptance criteria in production
```

#### 4.2 Rollback Preparation
If issues detected:
- Document specific problems
- Prepare rollback strategy
- Notify team via ClickUp comments

## Configuration Management

### Safe Mode Settings
- **Safe Mode ON**: Requires manual approval before deployment
- **Dry Run ON**: Simulates deployment without real changes
- **Mock APIs ON**: Uses test data for development

### Production Settings
- **Safe Mode OFF**: Automatic deployment after approval
- **Dry Run OFF**: Real GitHub and Vercel operations
- **Mock APIs OFF**: Live API integrations

## Error Handling

### Common Deployment Issues

#### GitHub Errors:
- **403 Forbidden**: Check PAT permissions
- **Branch Exists**: Delete existing branch or use different name
- **Merge Conflicts**: Resolve conflicts manually

#### Vercel Errors:
- **Build Failed**: Check build logs in Vercel dashboard
- **Deployment Timeout**: Increase timeout or check resource limits
- **Domain Issues**: Verify custom domain configuration

#### ClickUp Errors:
- **Token Expired**: Refresh ClickUp API token
- **Ticket Not Found**: Verify ticket ID and permissions
- **Update Failed**: Check API rate limits

### Recovery Strategies

#### Partial Deployment Failure:
1. Check which stage failed via logs
2. Fix underlying issue
3. Retry deployment from failed stage
4. Update ClickUp manually if needed

#### Complete Deployment Failure:
1. Rollback GitHub changes if needed
2. Revert Vercel deployment
3. Update ClickUp ticket status
4. Document failure for team review

## Monitoring & Observability

### Real-time Monitoring
```bash
# Stream all deployment events
python -m cli tail

# Check recent deployment history
python -m cli logs --limit 50
```

### Deployment Metrics
Track across deployments:
- Time from approval to live
- Success/failure rates
- Build duration
- Rollback frequency

### Alerting
Set up notifications for:
- Deployment failures
- Long build times
- Vercel errors
- ClickUp sync issues

## Security Considerations

### Token Management:
- Use fine-grained GitHub PATs
- Rotate tokens regularly
- Store securely in environment variables
- Limit scope to minimum required

### Deployment Safety:
- Always use safe mode initially
- Test with dry run first
- Monitor deployment logs
- Have rollback plan ready

## Integration with Other Skills

### Pre-Deployment:
- **`test-driven-development`**: Ensure tests pass
- **`requesting-code-review`**: Quality gates
- **`verification-before-completion`**: Final checks

### Post-Deployment:
- **`finishing-a-development-branch`**: Cleanup
- **`receiving-code-review`**: Handle feedback
- **`systematic-debugging`**: If issues arise

## Best Practices

### Development:
1. **Test Locally First**: Verify changes work before deployment
2. **Use Staging**: Deploy to staging environment first
3. **Monitor Actively**: Watch deployment logs in real-time
4. **Document Changes**: Clear commit messages and PR descriptions

### Operations:
1. **Gradual Rollout**: Start with safe mode enabled
2. **Monitor Metrics**: Track deployment success rates
3. **Automate Rollbacks**: Prepare automated rollback procedures
4. **Team Communication**: Keep team informed of deployment status

### Security:
1. **Principle of Least Privilege**: Minimal required permissions
2. **Regular Audits**: Review access tokens and permissions
3. **Secure Storage**: Environment variables for sensitive data
4. **Monitoring**: Log and alert on security events

## Troubleshooting Guide

### Deployment Stuck:
```bash
# Check current status
python -m cli logs

# Verify integrations
python -m cli auth

# Manual intervention if needed
# Check GitHub PR status
# Check Vercel deployment dashboard
# Update ClickUp ticket manually
```

### Performance Issues:
- Check Vercel build logs
- Monitor resource usage
- Optimize build process
- Consider deployment regions

## Success Metrics

### Deployment Velocity:
- Average time from code complete to live
- Deployment frequency
- Lead time for changes

### Quality Metrics:
- Deployment success rate
- Rollback frequency
- Post-deployment issues

### Team Metrics:
- Developer satisfaction
- Time saved on manual deployments
- Reduced context switching

## Red Flags

| Thought | Use This Skill |
|---------|----------------|
| "Ready to deploy this change" | Yes - full deployment workflow |
| "Need to create a PR" | Yes - automated PR creation |
| "Want to update the ticket" | Yes - automatic ClickUp updates |
| "This deployment is risky" | Yes - use safe mode |
| "Need deployment monitoring" | Yes - real-time tracking |