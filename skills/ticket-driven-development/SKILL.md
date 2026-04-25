---
name: ticket-driven-development
description: Complete ticket-to-deployment workflow combining Superpowers methodology with Bot-ANX execution
---

## When to Use

This skill activates when:
- Starting work on a ClickUp ticket
- Need end-to-end ticket → deployment automation
- Want to combine systematic development with project management
- Working in teams with ClickUp + GitHub + Vercel workflow

## Prerequisites

- Bot-ANX backend configured and running
- ClickUp, GitHub, and Vercel integrations set up
- Superpowers skills available (brainstorming, planning, TDD, etc.)

## Complete Workflow

### Phase 1: Ticket Analysis & Brainstorming

#### 1.1 Sync and Select Ticket
```bash
# Sync latest tickets
cd bot-anx/backend
python -m cli sync
python -m cli tickets

# Select ticket by priority and complexity
```

#### 1.2 Brainstorming Session
**Invoke: `brainstorming` skill**

Use ticket information as brainstorming input:
- **Ticket Name**: Primary objective
- **Description**: Context and background
- **Acceptance Criteria**: Success metrics
- **Comments**: Team insights and constraints
- **Tags**: Technical domain (frontend, backend, etc.)

Refine understanding through Socratic questioning:
- What problem does this solve for users?
- What are the technical constraints?
- How does this fit with existing architecture?
- What could go wrong?

### Phase 2: Planning & Design

#### 2.1 Create Implementation Plan
**Invoke: `writing-plans` skill**

Generate detailed plan considering:
- Ticket acceptance criteria as requirements
- Bot-ANX's file change capabilities
- Integration with existing codebase
- Testing requirements (TDD compliance)

#### 2.2 Plan Validation
Generate Bot-ANX plan for comparison:
```bash
python -m cli plan <ticket_id>
```

Merge insights from both planning approaches:
- Superpowers: Detailed task breakdown
- Bot-ANX: AI-generated execution steps
- Combined: Comprehensive implementation strategy

### Phase 3: Execution Setup

#### 3.1 Git Worktree Setup
**Invoke: `using-git-worktrees` skill**

Create isolated workspace:
```bash
# Create branch matching Bot-ANX naming
git worktree add ../ticket-<clickup_id> -b autodev/<clickup_id>
cd ../ticket-<clickup_id>
```

#### 3.2 Initialize Task Run
```bash
# Create task run in Bot-ANX
python -m cli run <ticket_id>
```

### Phase 4: Test-Driven Development

#### 4.1 TDD Enforcement
**Invoke: `test-driven-development` skill**

For each planned change:
1. **RED**: Write failing test based on acceptance criteria
2. **GREEN**: Implement minimal code to pass
3. **REFACTOR**: Clean up while keeping tests green

#### 4.2 Bot-ANX Execution Integration
```bash
# Monitor Bot-ANX execution in parallel
python -m cli tail

# Approve plan when ready
python -m cli approve <run_id>
```

### Phase 5: Code Review & Quality Gates

#### 5.1 Pre-Deployment Review
**Invoke: `requesting-code-review` skill**

Review checklist:
- [ ] All acceptance criteria implemented
- [ ] Tests passing (RED-GREEN-REFACTOR followed)
- [ ] Code follows project conventions
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed

#### 5.2 Bot-ANX Execution Results
Verify Bot-ANX simulation results:
- File changes align with plan
- Lint results clean
- Test results positive
- Commit message descriptive

### Phase 6: Deployment & Monitoring

#### 6.1 Deployment Execution
```bash
# Deploy via Bot-ANX
python -m cli deploy <run_id>
```

#### 6.2 Real-time Monitoring
Monitor deployment progress:
- WebSocket logs for real-time updates
- GitHub PR creation and merge
- Vercel deployment status
- ClickUp ticket updates

#### 6.3 Verification
**Invoke: `verification-before-completion` skill**

Verify deployment success:
- [ ] Deployment URL accessible
- [ ] Functionality works as expected
- [ ] Acceptance criteria met in production
- [ ] No regressions introduced

### Phase 7: Completion & Cleanup

#### 7.1 Ticket Closure
Bot-ANX automatically:
- Updates ClickUp ticket status
- Adds deployment URL as comment
- Closes ticket when verified

#### 7.2 Worktree Cleanup
**Invoke: `finishing-a-development-branch` skill**

Clean up development environment:
```bash
# Return to main workspace
cd ../main-workspace
git worktree remove ../ticket-<clickup_id>
```

## Integration Points

### Superpowers → Bot-ANX
- Brainstorming insights → Ticket refinement
- Detailed plans → Bot-ANX execution guidance
- TDD requirements → Test validation
- Code review → Quality gates

### Bot-ANX → Superpowers
- Ticket data → Brainstorming input
- AI plans → Planning validation
- Execution logs → Progress monitoring
- Deployment results → Verification data

## Monitoring & Feedback

### Real-time Tracking
```bash
# Stream live progress
python -m cli tail

# Check specific run status
python -m cli logs
```

### Quality Metrics
Track across tickets:
- Time from ticket → deployment
- Test coverage and pass rates
- Code review feedback
- Deployment success rates

## Error Recovery

### Common Failure Points:
1. **Plan Approval Timeout**: Manual intervention required
2. **Test Failures**: Return to TDD cycle
3. **Deployment Issues**: Check Vercel/GitHub integration
4. **Ticket Sync Problems**: Verify ClickUp credentials

### Recovery Strategies:
- Use Bot-ANX safe mode for risky changes
- Maintain git worktree isolation
- Keep deployment rollback options
- Document lessons learned

## Benefits

### Development Velocity:
- Automated ticket → deployment pipeline
- Parallel execution with quality gates
- Real-time progress visibility
- Reduced context switching

### Quality Assurance:
- TDD enforcement throughout
- Systematic code review process
- Automated testing integration
- Deployment verification

### Team Collaboration:
- Transparent progress tracking
- Automatic status updates
- Consistent development methodology
- Audit trail for all changes

## Best Practices

1. **Start Small**: Begin with low-risk tickets
2. **Use Safe Mode**: Require approvals for learning
3. **Monitor Actively**: Keep WebSocket tail running
4. **Document Patterns**: Capture successful workflows
5. **Iterate Process**: Refine based on team feedback

## Red Flags

| Thought | Use This Skill |
|---------|----------------|
| "I have a ClickUp ticket to implement" | Yes - full workflow |
| "Need to deploy this change" | Yes - deployment phase |
| "Want automated project management" | Yes - ticket integration |
| "This is too complex for manual process" | Yes - systematic approach |
| "Team needs visibility into progress" | Yes - real-time monitoring |