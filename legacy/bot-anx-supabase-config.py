#!/usr/bin/env python3
"""
Bot-ANX Supabase Integration
Replace MongoDB with Supabase for better performance and real-time features
"""

import os
from supabase import create_client, Client
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

class SupabaseClient:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_ANON_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        
        self.supabase: Client = create_client(url, key)
    
    # Tickets Management
    async def store_ticket(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """Store ClickUp ticket in Supabase"""
        result = self.supabase.table('tickets').upsert({
            'clickup_id': ticket['clickup_id'],
            'name': ticket['name'],
            'description': ticket['description'],
            'status': ticket['status'],
            'priority': ticket['priority'],
            'acceptance_criteria': ticket.get('acceptance_criteria', []),
            'comments': ticket.get('comments', []),
            'tags': ticket.get('tags', []),
            'assignee': ticket.get('assignee'),
            'url': ticket.get('url'),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }).execute()
        
        return result.data[0] if result.data else None
    
    async def get_tickets(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get tickets from Supabase"""
        query = self.supabase.table('tickets').select('*')
        
        if status:
            query = query.eq('status', status)
        
        result = query.execute()
        return result.data
    
    async def get_ticket_by_id(self, clickup_id: str) -> Optional[Dict[str, Any]]:
        """Get specific ticket by ClickUp ID"""
        result = self.supabase.table('tickets').select('*').eq('clickup_id', clickup_id).execute()
        return result.data[0] if result.data else None
    
    # Task Runs Management
    async def create_task_run(self, task_run: Dict[str, Any]) -> Dict[str, Any]:
        """Create task run in Supabase"""
        result = self.supabase.table('task_runs').insert({
            'id': task_run['id'],
            'ticket_id': task_run['ticket_id'],
            'status': task_run['status'],
            'plan': task_run.get('plan', {}),
            'execution_results': task_run.get('execution_results', {}),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }).execute()
        
        return result.data[0] if result.data else None
    
    async def update_task_run(self, run_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update task run status"""
        updates['updated_at'] = datetime.utcnow().isoformat()
        
        result = self.supabase.table('task_runs').update(updates).eq('id', run_id).execute()
        return result.data[0] if result.data else None
    
    async def get_task_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get task run by ID"""
        result = self.supabase.table('task_runs').select('*').eq('id', run_id).execute()
        return result.data[0] if result.data else None
    
    # Deployments Management
    async def create_deployment(self, deployment: Dict[str, Any]) -> Dict[str, Any]:
        """Create deployment record"""
        result = self.supabase.table('deployments').insert({
            'id': deployment['id'],
            'task_run_id': deployment['task_run_id'],
            'url': deployment['url'],
            'status': deployment['status'],
            'vercel_deployment_id': deployment.get('vercel_deployment_id'),
            'github_pr_number': deployment.get('github_pr_number'),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }).execute()
        
        return result.data[0] if result.data else None
    
    # Plan Cache (replacing MongoDB plan_cache)
    async def cache_plan(self, cache_key: str, plan: Dict[str, Any]) -> None:
        """Cache AI-generated plan"""
        self.supabase.table('plan_cache').upsert({
            'cache_key': cache_key,
            'plan': plan,
            'created_at': datetime.utcnow().isoformat()
        }).execute()
    
    async def get_cached_plan(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached plan"""
        result = self.supabase.table('plan_cache').select('plan').eq('cache_key', cache_key).execute()
        return result.data[0]['plan'] if result.data else None
    
    # Real-time Events
    def subscribe_to_events(self, callback):
        """Subscribe to real-time events"""
        # Subscribe to task runs changes
        self.supabase.table('task_runs').on('*', callback).subscribe()
        
        # Subscribe to deployment changes  
        self.supabase.table('deployments').on('*', callback).subscribe()
    
    # Superagent Events (new table for integration)
    async def log_event(self, event: Dict[str, Any]) -> None:
        """Log superagent events for monitoring"""
        self.supabase.table('superagent_events').insert({
            'event_type': event['type'],
            'ticket_id': event.get('ticket_id'),
            'worker_id': event.get('worker_id'),
            'data': event.get('data', {}),
            'timestamp': datetime.utcnow().isoformat()
        }).execute()
    
    async def get_events(self, ticket_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent events"""
        query = self.supabase.table('superagent_events').select('*').order('timestamp', desc=True).limit(limit)
        
        if ticket_id:
            query = query.eq('ticket_id', ticket_id)
        
        result = query.execute()
        return result.data


# Integration with existing Bot-ANX code
class SupabaseIntegration:
    def __init__(self):
        self.client = SupabaseClient()
    
    async def replace_mongodb_calls(self):
        """Replace all MongoDB calls with Supabase equivalents"""
        
        # Example: Replace ticket storage
        # OLD: await db.tickets.insert_one(ticket_data)
        # NEW: await self.client.store_ticket(ticket_data)
        
        # Example: Replace plan caching
        # OLD: await db.plan_cache.update_one({"_id": key}, {"$set": {"plan": plan}}, upsert=True)
        # NEW: await self.client.cache_plan(key, plan)
        
        pass


if __name__ == "__main__":
    # Test the integration
    import asyncio
    
    async def test_supabase():
        client = SupabaseClient()
        
        # Test ticket storage
        test_ticket = {
            'clickup_id': 'CU-TEST-001',
            'name': 'Test Supabase Integration',
            'description': 'Testing Supabase as MongoDB replacement',
            'status': 'open',
            'priority': 'high',
            'acceptance_criteria': ['Integration works', 'Real-time updates work'],
            'tags': ['test', 'supabase']
        }
        
        stored = await client.store_ticket(test_ticket)
        print(f"✅ Stored ticket: {stored}")
        
        # Test retrieval
        retrieved = await client.get_ticket_by_id('CU-TEST-001')
        print(f"✅ Retrieved ticket: {retrieved}")
        
        # Test event logging
        await client.log_event({
            'type': 'test_event',
            'ticket_id': 'CU-TEST-001',
            'data': {'message': 'Supabase integration test'}
        })
        print("✅ Event logged")
    
    # Run test
    asyncio.run(test_supabase())