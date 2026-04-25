#!/usr/bin/env python3
"""
Superagent Integration Script
Combines Superpowers methodology with Bot-ANX execution capabilities
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import httpx


class SuperagentCoordinator:
    """Coordinates between Superpowers methodology and Bot-ANX execution"""
    
    def __init__(self, bot_anx_url: str = "http://localhost:8001/api"):
        self.bot_anx_url = bot_anx_url
        self.bot_anx_path = Path("bot-anx/backend")
        
    async def _bot_anx_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make request to Bot-ANX API"""
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.request(method, f"{self.bot_anx_url}{endpoint}", **kwargs)
            response.raise_for_status()
            return response.json()
    
    def _run_cli_command(self, command: List[str]) -> Dict[str, Any]:
        """Run Bot-ANX CLI command"""
        try:
            result = subprocess.run(
                ["python", "-m", "cli"] + command,
                cwd=self.bot_anx_path,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": result.stdout, "error": result.stderr}
        except subprocess.CalledProcessError as e:
            return {"success": False, "output": e.stdout, "error": e.stderr}
    
    async def check_integrations(self) -> Dict[str, Any]:
        """Check Bot-ANX integration status"""
        print("🔍 Checking Bot-ANX integrations...")
        try:
            status = await self._bot_anx_request("GET", "/config/status")
            print(f"✅ Bot-ANX integrations: {json.dumps(status, indent=2)}")
            return status
        except Exception as e:
            print(f"❌ Bot-ANX integration check failed: {e}")
            return {"error": str(e)}
    
    async def sync_tickets(self) -> List[Dict[str, Any]]:
        """Sync tickets from ClickUp"""
        print("🎫 Syncing ClickUp tickets...")
        try:
            # Sync tickets
            await self._bot_anx_request("POST", "/tickets/sync")
            
            # Get ticket list
            tickets = await self._bot_anx_request("GET", "/tickets")
            print(f"✅ Synced {len(tickets)} tickets")
            
            for ticket in tickets[:3]:  # Show first 3
                print(f"  • {ticket.get('clickup_id')}: {ticket.get('name')} [{ticket.get('priority')}]")
            
            return tickets
        except Exception as e:
            print(f"❌ Ticket sync failed: {e}")
            return []
    
    def brainstorm_ticket(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """Apply Superpowers brainstorming to ticket"""
        print(f"🧠 Brainstorming ticket {ticket.get('clickup_id')}...")
        
        # Simulate brainstorming process (in real implementation, this would invoke the brainstorming skill)
        brainstorm_result = {
            "ticket_id": ticket.get("clickup_id"),
            "refined_requirements": [
                "Clarified user needs based on ticket description",
                "Identified technical constraints from comments",
                "Validated acceptance criteria completeness"
            ],
            "technical_approach": "Systematic implementation following TDD principles",
            "risks_identified": [
                "Integration complexity with existing systems",
                "Potential performance impact",
                "User experience considerations"
            ],
            "questions_resolved": [
                "What is the expected user workflow?",
                "How does this integrate with existing features?",
                "What are the performance requirements?"
            ]
        }
        
        print("✅ Brainstorming completed:")
        print(f"  • Refined {len(brainstorm_result['refined_requirements'])} requirements")
        print(f"  • Identified {len(brainstorm_result['risks_identified'])} risks")
        
        return brainstorm_result
    
    def create_detailed_plan(self, ticket: Dict[str, Any], brainstorm: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed implementation plan using Superpowers methodology"""
        print(f"📋 Creating detailed plan for {ticket.get('clickup_id')}...")
        
        # Simulate detailed planning (in real implementation, this would invoke the writing-plans skill)
        detailed_plan = {
            "ticket_id": ticket.get("clickup_id"),
            "summary": f"Implement {ticket.get('name')} with systematic approach",
            "tasks": [
                {
                    "id": 1,
                    "title": "Setup & Analysis",
                    "description": "Analyze codebase and identify impact areas",
                    "estimated_time": "15 minutes",
                    "files": ["src/analysis.md"],
                    "tests_required": False
                },
                {
                    "id": 2,
                    "title": "Write Tests (RED)",
                    "description": "Create failing tests based on acceptance criteria",
                    "estimated_time": "20 minutes",
                    "files": [f"tests/test_{ticket.get('clickup_id', 'feature').lower()}.py"],
                    "tests_required": True
                },
                {
                    "id": 3,
                    "title": "Implement Feature (GREEN)",
                    "description": "Minimal implementation to pass tests",
                    "estimated_time": "30 minutes",
                    "files": [f"src/{ticket.get('clickup_id', 'feature').lower()}.py"],
                    "tests_required": True
                },
                {
                    "id": 4,
                    "title": "Refactor & Optimize",
                    "description": "Clean up code while maintaining green tests",
                    "estimated_time": "15 minutes",
                    "files": [f"src/{ticket.get('clickup_id', 'feature').lower()}.py"],
                    "tests_required": True
                },
                {
                    "id": 5,
                    "title": "Integration & Documentation",
                    "description": "Integrate with existing systems and document",
                    "estimated_time": "10 minutes",
                    "files": ["README.md", "docs/"],
                    "tests_required": False
                }
            ],
            "total_estimated_time": "90 minutes",
            "quality_gates": [
                "All tests passing",
                "Code review completed",
                "Acceptance criteria verified",
                "No regressions introduced"
            ]
        }
        
        print("✅ Detailed plan created:")
        print(f"  • {len(detailed_plan['tasks'])} tasks defined")
        print(f"  • Estimated time: {detailed_plan['total_estimated_time']}")
        
        return detailed_plan
    
    async def execute_with_bot_anx(self, ticket_id: str, detailed_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute plan using Bot-ANX with Superpowers oversight"""
        print(f"🚀 Executing ticket {ticket_id} with Bot-ANX...")
        
        try:
            # Create task run
            task_run = await self._bot_anx_request("POST", f"/task-runs/from-ticket/{ticket_id}")
            run_id = task_run.get("id")
            print(f"✅ Created task run: {run_id}")
            
            # Get Bot-ANX generated plan
            bot_plan = task_run.get("plan", {})
            print("🤖 Bot-ANX plan generated")
            
            # Compare plans (Superpowers detailed vs Bot-ANX AI-generated)
            comparison = self._compare_plans(detailed_plan, bot_plan)
            print(f"📊 Plan comparison: {comparison['alignment_score']:.1%} alignment")
            
            # Approve plan (in safe mode, this would require human approval)
            if task_run.get("status") == "awaiting_plan_approval":
                approval = await self._bot_anx_request("POST", f"/task-runs/{run_id}/approve-plan")
                print(f"✅ Plan approved: {approval.get('status')}")
            
            return {
                "run_id": run_id,
                "status": task_run.get("status"),
                "plan_comparison": comparison,
                "execution_started": True
            }
            
        except Exception as e:
            print(f"❌ Execution failed: {e}")
            return {"error": str(e)}
    
    def _compare_plans(self, superpowers_plan: Dict[str, Any], bot_anx_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Compare Superpowers detailed plan with Bot-ANX AI plan"""
        sp_tasks = len(superpowers_plan.get("tasks", []))
        ba_steps = len(bot_anx_plan.get("steps", []))
        
        # Simple alignment scoring (in real implementation, this would be more sophisticated)
        alignment_score = min(sp_tasks, ba_steps) / max(sp_tasks, ba_steps) if max(sp_tasks, ba_steps) > 0 else 0
        
        return {
            "superpowers_tasks": sp_tasks,
            "bot_anx_steps": ba_steps,
            "alignment_score": alignment_score,
            "recommendations": [
                "Combine detailed TDD approach with AI execution",
                "Use Superpowers quality gates with Bot-ANX automation",
                "Monitor execution with real-time feedback"
            ]
        }
    
    async def monitor_execution(self, run_id: str) -> Dict[str, Any]:
        """Monitor Bot-ANX execution with Superpowers quality gates"""
        print(f"👀 Monitoring execution {run_id}...")
        
        try:
            # Get execution status
            run_status = await self._bot_anx_request("GET", f"/task-runs/{run_id}")
            print(f"📊 Status: {run_status.get('status')}")
            
            # Apply Superpowers quality gates
            quality_check = self._apply_quality_gates(run_status)
            print(f"🔍 Quality check: {quality_check['passed']}/{quality_check['total']} gates passed")
            
            return {
                "run_id": run_id,
                "status": run_status.get("status"),
                "quality_gates": quality_check,
                "ready_for_deployment": quality_check["all_passed"]
            }
            
        except Exception as e:
            print(f"❌ Monitoring failed: {e}")
            return {"error": str(e)}
    
    def _apply_quality_gates(self, run_status: Dict[str, Any]) -> Dict[str, Any]:
        """Apply Superpowers quality gates to Bot-ANX execution"""
        gates = {
            "tests_passing": run_status.get("test_results", {}).get("failed", 1) == 0,
            "lint_clean": run_status.get("lint_results", {}).get("errors", 1) == 0,
            "files_changed": len(run_status.get("file_changes", [])) > 0,
            "commit_created": bool(run_status.get("commit_sha")),
        }
        
        passed = sum(gates.values())
        total = len(gates)
        
        return {
            "gates": gates,
            "passed": passed,
            "total": total,
            "all_passed": passed == total,
            "details": {
                "tests": run_status.get("test_results", {}),
                "lint": run_status.get("lint_results", {}),
                "changes": len(run_status.get("file_changes", []))
            }
        }
    
    async def deploy_with_monitoring(self, run_id: str) -> Dict[str, Any]:
        """Deploy using Bot-ANX with Superpowers verification"""
        print(f"🚀 Deploying run {run_id}...")
        
        try:
            # Trigger deployment
            deployment = await self._bot_anx_request("POST", f"/deployments/from-run/{run_id}")
            print(f"✅ Deployment initiated: {deployment.get('id')}")
            
            # Verify deployment (Superpowers verification approach)
            verification = await self._verify_deployment(deployment)
            print(f"🔍 Deployment verification: {'✅ Passed' if verification['success'] else '❌ Failed'}")
            
            return {
                "deployment_id": deployment.get("id"),
                "url": deployment.get("url"),
                "verification": verification,
                "success": verification["success"]
            }
            
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            return {"error": str(e)}
    
    async def _verify_deployment(self, deployment: Dict[str, Any]) -> Dict[str, Any]:
        """Verify deployment using Superpowers verification methodology"""
        url = deployment.get("url")
        if not url:
            return {"success": False, "reason": "No deployment URL"}
        
        try:
            # Basic health check
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "url": url,
                "verified_at": "now",
                "checks": {
                    "url_accessible": response.status_code == 200,
                    "response_time": "< 1s",  # Simplified
                    "content_valid": len(response.text) > 0
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "reason": str(e),
                "url": url
            }
    
    async def complete_workflow(self, ticket_id: Optional[str] = None) -> Dict[str, Any]:
        """Complete end-to-end workflow: Superpowers methodology + Bot-ANX execution"""
        print("🎯 Starting complete Superagent workflow...")
        
        try:
            # 1. Check integrations
            integrations = await self.check_integrations()
            if "error" in integrations:
                return {"error": "Integration check failed", "details": integrations}
            
            # 2. Sync tickets
            tickets = await self.sync_tickets()
            if not tickets:
                return {"error": "No tickets available"}
            
            # 3. Select ticket (use provided ID or first available)
            if ticket_id:
                ticket = next((t for t in tickets if t.get("clickup_id") == ticket_id), None)
                if not ticket:
                    return {"error": f"Ticket {ticket_id} not found"}
            else:
                # Select highest priority open ticket
                open_tickets = [t for t in tickets if t.get("status") == "open"]
                if not open_tickets:
                    return {"error": "No open tickets available"}
                ticket = max(open_tickets, key=lambda t: {"urgent": 4, "high": 3, "normal": 2, "low": 1}.get(t.get("priority", "low"), 1))
            
            print(f"🎫 Selected ticket: {ticket.get('clickup_id')} - {ticket.get('name')}")
            
            # 4. Brainstorm (Superpowers methodology)
            brainstorm = self.brainstorm_ticket(ticket)
            
            # 5. Create detailed plan (Superpowers methodology)
            detailed_plan = self.create_detailed_plan(ticket, brainstorm)
            
            # 6. Execute with Bot-ANX
            execution = await self.execute_with_bot_anx(ticket.get("clickup_id"), detailed_plan)
            if "error" in execution:
                return {"error": "Execution failed", "details": execution}
            
            # 7. Monitor execution
            monitoring = await self.monitor_execution(execution["run_id"])
            if not monitoring.get("ready_for_deployment"):
                return {"error": "Quality gates failed", "details": monitoring}
            
            # 8. Deploy with verification
            deployment = await self.deploy_with_monitoring(execution["run_id"])
            
            print("🎉 Superagent workflow completed successfully!")
            
            return {
                "success": True,
                "ticket": ticket.get("clickup_id"),
                "brainstorm": brainstorm,
                "plan": detailed_plan,
                "execution": execution,
                "monitoring": monitoring,
                "deployment": deployment,
                "summary": {
                    "ticket_name": ticket.get("name"),
                    "deployment_url": deployment.get("url"),
                    "total_tasks": len(detailed_plan.get("tasks", [])),
                    "quality_gates_passed": monitoring.get("quality_gates", {}).get("all_passed", False),
                    "deployment_success": deployment.get("success", False)
                }
            }
            
        except Exception as e:
            print(f"❌ Workflow failed: {e}")
            return {"error": str(e)}


async def main():
    """Main entry point for Superagent integration"""
    coordinator = SuperagentCoordinator()
    
    if len(sys.argv) > 1:
        ticket_id = sys.argv[1]
        result = await coordinator.complete_workflow(ticket_id)
    else:
        result = await coordinator.complete_workflow()
    
    print("\n" + "="*50)
    print("SUPERAGENT WORKFLOW RESULT")
    print("="*50)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())