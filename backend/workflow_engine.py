"""
1INTERPRETER Workflow Engine
Advanced workflow definition, management and execution system
"""
import json
import time
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from llm.llm_wrapper import get_llm
from llm.agent_engine import get_agent_engine

class WorkflowEngine:
    """Advanced workflow orchestration and management"""
    
    def __init__(self):
        self.llm = get_llm()
        self.agent_engine = get_agent_engine()
        self.workflows_dir = Path("workflows")
        self.workflow_executions_dir = Path("workflow_executions")
        
        self.workflows_dir.mkdir(exist_ok=True)
        self.workflow_executions_dir.mkdir(exist_ok=True)
        
        self.loaded_workflows = {}
        self.load_existing_workflows()
    
    def load_existing_workflows(self):
        """Load all existing workflow definitions"""
        for workflow_file in self.workflows_dir.glob("*.json"):
            try:
                with open(workflow_file, 'r') as f:
                    workflow_data = json.load(f)
                    self.loaded_workflows[workflow_data["name"]] = workflow_data
                print(f"📋 Loaded workflow: {workflow_data['name']}")
            except Exception as e:
                print(f"❌ Error loading workflow {workflow_file}: {str(e)}")
    
    def create_workflow(self, name: str, description: str, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a new workflow definition"""
        
        workflow_id = str(uuid.uuid4())
        
        workflow_definition = {
            "id": workflow_id,
            "name": name,
            "description": description,
            "created": datetime.now().isoformat(),
            "version": "1.0.0",
            "steps": steps,
            "metadata": {
                "total_steps": len(steps),
                "estimated_duration": self._estimate_duration(steps),
                "dependencies": self._extract_dependencies(steps)
            },
            "execution_history": []
        }
        
        # Save workflow
        workflow_file = self.workflows_dir / f"{name.lower().replace(' ', '_')}.json"
        with open(workflow_file, 'w') as f:
            json.dump(workflow_definition, f, indent=2)
        
        # Add to loaded workflows
        self.loaded_workflows[name] = workflow_definition
        
        print(f"📋 Workflow '{name}' created with {len(steps)} steps")
        return workflow_definition
    
    def create_devops_pipeline_workflow(self, repo_url: str = "") -> str:
        """Create a comprehensive DevOps pipeline workflow"""
        
        workflow_name = f"DevOps Pipeline {int(time.time())}"
        
        steps = [
            {
                "id": "step_1",
                "name": "Repository Clone",
                "type": "repository",
                "action": "clone",
                "parameters": {
                    "repository_url": repo_url,
                    "target_directory": "workspace",
                    "timeout": 300
                },
                "on_success": "step_2",
                "on_failure": "abort",
                "retry_count": 2
            },
            {
                "id": "step_2", 
                "name": "Code Analysis",
                "type": "analysis",
                "action": "static_analysis",
                "parameters": {
                    "target": "workspace",
                    "include_security": True,
                    "generate_report": True
                },
                "on_success": "step_3",
                "on_failure": "step_3",  # Continue even if analysis has issues
                "dependencies": ["step_1"]
            },
            {
                "id": "step_3",
                "name": "Test Generation",
                "type": "testing",
                "action": "generate_tests",
                "parameters": {
                    "framework": "pytest",
                    "coverage_threshold": 80,
                    "generate_mocks": True
                },
                "on_success": "step_4",
                "on_failure": "step_4",  # Continue to Docker even without tests
                "dependencies": ["step_1"]
            },
            {
                "id": "step_4",
                "name": "Docker Configuration",
                "type": "containerization",
                "action": "generate_docker_files",
                "parameters": {
                    "optimization_level": "production",
                    "include_kubernetes": True,
                    "security_hardening": True
                },
                "on_success": "step_5",
                "on_failure": "abort",
                "dependencies": ["step_1", "step_2"]
            },
            {
                "id": "step_5",
                "name": "Deployment Strategy",
                "type": "deployment",
                "action": "create_deployment_config",
                "parameters": {
                    "target_platform": "kubernetes",
                    "environment": "production",
                    "scaling_config": "auto"
                },
                "on_success": "step_6",
                "on_failure": "step_6",  # Continue to optimization
                "dependencies": ["step_4"]
            },
            {
                "id": "step_6",
                "name": "Code Optimization",
                "type": "optimization",
                "action": "optimize_codebase",
                "parameters": {
                    "performance_analysis": True,
                    "security_review": True,
                    "generate_recommendations": True
                },
                "on_success": "complete",
                "on_failure": "complete",  # End workflow regardless
                "dependencies": ["step_2"]
            }
        ]
        
        workflow = self.create_workflow(
            name=workflow_name,
            description=f"Comprehensive DevOps pipeline for repository: {repo_url or 'local project'}",
            steps=steps
        )
        
        return workflow["name"]
    
    def execute_workflow(self, workflow_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a workflow with comprehensive tracking"""
        
        if workflow_name not in self.loaded_workflows:
            return {
                "success": False,
                "error": f"Workflow '{workflow_name}' not found",
                "execution_id": None
            }
        
        workflow = self.loaded_workflows[workflow_name]
        execution_id = str(uuid.uuid4())
        
        start_time = time.time()
        
        execution_record = {
            "execution_id": execution_id,
            "workflow_name": workflow_name,
            "workflow_id": workflow["id"],
            "start_time": start_time,
            "parameters": parameters or {},
            "steps_executed": [],
            "current_step": None,
            "status": "running",
            "results": {},
            "errors": []
        }
        
        try:
            print(f"🚀 Starting workflow execution: {workflow_name}")
            
            # Execute workflow steps
            step_results = self._execute_workflow_steps(workflow["steps"], parameters or {}, execution_record)
            
            # Update execution record
            execution_record["status"] = "completed" if step_results["success"] else "failed"
            execution_record["end_time"] = time.time()
            execution_record["duration"] = execution_record["end_time"] - start_time
            execution_record["results"] = step_results
            
            # Save execution record
            self._save_execution_record(execution_record)
            
            # Update workflow history
            workflow["execution_history"].append({
                "execution_id": execution_id,
                "timestamp": datetime.now().isoformat(),
                "status": execution_record["status"],
                "duration": execution_record["duration"]
            })
            
            # Save updated workflow
            self._save_workflow(workflow)
            
            summary = f"""✅ Workflow Execution Complete:
📋 Workflow: {workflow_name}
🆔 Execution ID: {execution_id}
📊 Steps: {len(execution_record['steps_executed'])}/{len(workflow['steps'])}
⏱️ Duration: {execution_record['duration']:.2f}s
📄 Status: {execution_record['status']}"""
            
            return {
                "success": step_results["success"],
                "execution_id": execution_id,
                "summary": summary,
                "results": step_results,
                "execution_record": execution_record
            }
            
        except Exception as e:
            execution_record["status"] = "error"
            execution_record["end_time"] = time.time()
            execution_record["duration"] = execution_record["end_time"] - start_time
            execution_record["errors"].append(str(e))
            
            self._save_execution_record(execution_record)
            
            return {
                "success": False,
                "execution_id": execution_id,
                "error": str(e),
                "summary": f"❌ Workflow execution failed: {str(e)}"
            }
    
    def _execute_workflow_steps(self, steps: List[Dict], parameters: Dict, execution_record: Dict) -> Dict[str, Any]:
        """Execute workflow steps with dependency management"""
        
        completed_steps = set()
        step_results = {}
        
        # Create execution order based on dependencies
        execution_order = self._resolve_dependencies(steps)
        
        for step_id in execution_order:
            step = next((s for s in steps if s["id"] == step_id), None)
            if not step:
                continue
            
            execution_record["current_step"] = step_id
            
            try:
                print(f"🔄 Executing step: {step['name']}")
                
                # Execute step
                result = self._execute_single_step(step, parameters)
                
                step_results[step_id] = result
                execution_record["steps_executed"].append({
                    "step_id": step_id,
                    "step_name": step["name"],
                    "status": "success" if result["success"] else "failed",
                    "duration": result.get("duration", 0),
                    "timestamp": datetime.now().isoformat()
                })
                
                completed_steps.add(step_id)
                
                # Handle step result
                if result["success"]:
                    if step.get("on_success") == "abort":
                        break
                else:
                    if step.get("on_failure") == "abort":
                        return {
                            "success": False,
                            "error": f"Step '{step['name']}' failed: {result.get('error', 'Unknown error')}",
                            "completed_steps": completed_steps,
                            "step_results": step_results
                        }
                
            except Exception as e:
                step_results[step_id] = {
                    "success": False,
                    "error": str(e)
                }
                
                execution_record["errors"].append(f"Step {step_id}: {str(e)}")
                
                if step.get("on_failure") == "abort":
                    return {
                        "success": False,
                        "error": f"Step '{step['name']}' error: {str(e)}",
                        "completed_steps": completed_steps,
                        "step_results": step_results
                    }
        
        return {
            "success": True,
            "completed_steps": completed_steps,
            "step_results": step_results,
            "total_steps": len(steps)
        }
    
    def _execute_single_step(self, step: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        
        start_time = time.time()
        step_type = step.get("type", "general")
        action = step.get("action", "unknown")
        step_params = step.get("parameters", {})
        
        try:
            if step_type == "repository":
                if action == "clone":
                    repo_url = step_params.get("repository_url", parameters.get("repository_url", ""))
                    result = self.agent_engine.execute_agent_task(
                        agent_name="repo_agent",
                        task=f"Clone repository: {repo_url}",
                        context=repo_url,
                        task_type="code_analysis"
                    )
            
            elif step_type == "analysis":
                result = self.agent_engine.execute_agent_task(
                    agent_name="analysis_agent",
                    task="Perform static code analysis",
                    context="",
                    task_type="code_analysis"
                )
            
            elif step_type == "testing":
                result = self.agent_engine.execute_agent_task(
                    agent_name="test_agent", 
                    task="Generate comprehensive test suite",
                    context="",
                    task_type="test_generation"
                )
            
            elif step_type == "containerization":
                result = self.agent_engine.execute_agent_task(
                    agent_name="docker_agent",
                    task="Generate Docker deployment configuration",
                    context="",
                    task_type="docker_generation"
                )
            
            elif step_type == "deployment":
                result = self.agent_engine.execute_agent_task(
                    agent_name="deploy_agent",
                    task="Create deployment strategy",
                    context="",
                    task_type="deployment"
                )
            
            elif step_type == "optimization":
                result = self.agent_engine.execute_agent_task(
                    agent_name="optimizer_agent",
                    task="Optimize codebase performance",
                    context="",
                    task_type="optimization"
                )
            
            else:
                # Generic step execution
                result = {
                    "success": True,
                    "content": f"✅ {step['name']} completed successfully",
                    "agent": "generic"
                }
            
            result["duration"] = time.time() - start_time
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "duration": time.time() - start_time
            }
    
    def _resolve_dependencies(self, steps: List[Dict]) -> List[str]:
        """Resolve step dependencies and create execution order"""
        
        # Simple dependency resolution (topological sort)
        step_map = {step["id"]: step for step in steps}
        visited = set()
        execution_order = []
        
        def visit_step(step_id):
            if step_id in visited:
                return
            
            visited.add(step_id)
            step = step_map.get(step_id)
            
            if step:
                # Visit dependencies first
                dependencies = step.get("dependencies", [])
                for dep in dependencies:
                    if dep in step_map:
                        visit_step(dep)
                
                execution_order.append(step_id)
        
        # Visit all steps
        for step in steps:
            visit_step(step["id"])
        
        return execution_order
    
    def _estimate_duration(self, steps: List[Dict]) -> int:
        """Estimate workflow execution duration in seconds"""
        
        base_duration = 30  # Base 30 seconds per step
        
        duration_map = {
            "repository": 60,    # Clone operations take longer
            "analysis": 45,      # Analysis can be time-consuming
            "testing": 90,       # Test generation takes time
            "containerization": 30,
            "deployment": 45,
            "optimization": 60
        }
        
        total_duration = 0
        for step in steps:
            step_type = step.get("type", "general")
            total_duration += duration_map.get(step_type, base_duration)
        
        return total_duration
    
    def _extract_dependencies(self, steps: List[Dict]) -> List[str]:
        """Extract workflow dependencies"""
        
        all_deps = set()
        for step in steps:
            step_type = step.get("type")
            if step_type:
                all_deps.add(step_type)
        
        return list(all_deps)
    
    def _save_execution_record(self, execution_record: Dict):
        """Save workflow execution record"""
        
        execution_file = self.workflow_executions_dir / f"execution_{execution_record['execution_id']}.json"
        with open(execution_file, 'w') as f:
            json.dump(execution_record, f, indent=2, default=str)
    
    def _save_workflow(self, workflow: Dict):
        """Save workflow definition"""
        
        workflow_file = self.workflows_dir / f"{workflow['name'].lower().replace(' ', '_')}.json"
        with open(workflow_file, 'w') as f:
            json.dump(workflow, f, indent=2, default=str)
    
    def list_workflows(self) -> Dict[str, Dict[str, Any]]:
        """List all available workflows"""
        return self.loaded_workflows
    
    def get_workflow_info(self, workflow_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed workflow information"""
        return self.loaded_workflows.get(workflow_name)
    
    def delete_workflow(self, workflow_name: str) -> bool:
        """Delete a workflow"""
        
        if workflow_name in self.loaded_workflows:
            # Remove from memory
            del self.loaded_workflows[workflow_name]
            
            # Remove file
            workflow_file = self.workflows_dir / f"{workflow_name.lower().replace(' ', '_')}.json"
            if workflow_file.exists():
                workflow_file.unlink()
            
            print(f"🗑️ Workflow '{workflow_name}' deleted")
            return True
        return False

# Global workflow engine instance
workflow_engine = None

def get_workflow_engine() -> WorkflowEngine:
    """Get global workflow engine instance"""
    global workflow_engine
    if workflow_engine is None:
        workflow_engine = WorkflowEngine()
    return workflow_engine

if __name__ == "__main__":
    engine = get_workflow_engine()
    workflow_name = engine.create_devops_pipeline_workflow("https://github.com/example/repo.git")
    result = engine.execute_workflow(workflow_name)
    print(result["summary"])
