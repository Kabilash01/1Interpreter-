"""
1INTERPRETER Agent Engine
Core AI agent orchestration and management system
"""
import json
import time
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from llm.llm_wrapper import get_llm

class AgentEngine:
    """Core engine for managing and executing AI agents"""
    
    def __init__(self):
        self.llm = get_llm()
        self.agents_dir = Path("agents")
        self.agents_dir.mkdir(exist_ok=True)
        self.active_agents = {}
        self.load_existing_agents()
    
    def load_existing_agents(self):
        """Load all existing agent configurations"""
        for agent_file in self.agents_dir.glob("*.json"):
            try:
                with open(agent_file, 'r') as f:
                    agent_data = json.load(f)
                    self.active_agents[agent_data["name"]] = agent_data
                print(f"Loaded agent: {agent_data['name']}")
            except Exception as e:
                print(f"❌ Error loading agent {agent_file}: {str(e)}")
    
    def create_agent(self, name: str, purpose: str, language: str = "python", 
                    capabilities: List[str] = None) -> Dict[str, Any]:
        """Create a new AI agent with specified capabilities"""
        
        if capabilities is None:
            capabilities = ["code_analysis", "docker_generation", "test_creation", "optimization"]
        
        agent_config = {
            "id": str(uuid.uuid4()),
            "name": name,
            "purpose": purpose,
            "language": language,
            "capabilities": capabilities,
            "created": str(time.time()),
            "last_used": None,
            "usage_count": 0,
            "performance_metrics": {
                "success_rate": 0.0,
                "average_response_time": 0.0,
                "total_tasks": 0
            }
        }
        
        # Save agent configuration
        agent_file = self.agents_dir / f"{name.lower()}.json"
        with open(agent_file, 'w') as f:
            json.dump(agent_config, f, indent=2)
        
        # Add to active agents
        self.active_agents[name] = agent_config
        
        print(f"🤖 Agent '{name}' created successfully")
        return agent_config
    
    def execute_agent_task(self, agent_name: str, task: str, context: str = "", 
                          task_type: str = "general") -> Dict[str, Any]:
        """Execute a task using specified agent"""
        
        if agent_name not in self.active_agents:
            return {
                "success": False,
                "error": f"Agent '{agent_name}' not found",
                "content": "",
                "agent": agent_name
            }
        
        agent = self.active_agents[agent_name]
        start_time = time.time()
        
        # Check if agent has required capability
        if task_type not in agent["capabilities"] and task_type != "general":
            return {
                "success": False,
                "error": f"Agent '{agent_name}' doesn't have '{task_type}' capability",
                "content": "",
                "agent": agent_name
            }
        
        try:
            # Generate specialized prompt for the agent
            agent_prompt = f"""
You are {agent['name']}, an AI agent specialized in {agent['purpose']}.
Your primary programming language expertise is {agent['language']}.
Your capabilities include: {', '.join(agent['capabilities'])}.

Task: {task}
Context: {context}

Please provide a detailed, actionable response based on your specialization.
"""
            
            # Get AI response
            result = self.llm.generate_response(agent_prompt, context, task_type)
            
            # Update agent metrics
            execution_time = time.time() - start_time
            self.update_agent_metrics(agent_name, result["success"], execution_time)
            
            return {
                "success": result["success"],
                "content": result["content"],
                "agent": agent_name,
                "task_type": task_type,
                "execution_time": execution_time,
                "provider": result.get("provider", "unknown"),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.update_agent_metrics(agent_name, False, execution_time)
            
            return {
                "success": False,
                "error": str(e),
                "content": "",
                "agent": agent_name,
                "execution_time": execution_time
            }
    
    def update_agent_metrics(self, agent_name: str, success: bool, execution_time: float):
        """Update agent performance metrics"""
        if agent_name in self.active_agents:
            agent = self.active_agents[agent_name]
            metrics = agent["performance_metrics"]
            
            # Update metrics
            metrics["total_tasks"] += 1
            agent["usage_count"] += 1
            agent["last_used"] = str(time.time())
            
            # Update success rate
            if metrics["total_tasks"] == 1:
                metrics["success_rate"] = 1.0 if success else 0.0
            else:
                current_successes = metrics["success_rate"] * (metrics["total_tasks"] - 1)
                if success:
                    current_successes += 1
                metrics["success_rate"] = current_successes / metrics["total_tasks"]
            
            # Update average response time
            if metrics["total_tasks"] == 1:
                metrics["average_response_time"] = execution_time
            else:
                total_time = metrics["average_response_time"] * (metrics["total_tasks"] - 1)
                metrics["average_response_time"] = (total_time + execution_time) / metrics["total_tasks"]
            
            # Save updated metrics
            agent_file = self.agents_dir / f"{agent_name.lower()}.json"
            with open(agent_file, 'w') as f:
                json.dump(agent, f, indent=2)
    
    def get_agent_info(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about an agent"""
        return self.active_agents.get(agent_name)
    
    def list_agents(self) -> Dict[str, Dict[str, Any]]:
        """List all available agents"""
        return self.active_agents
    
    def delete_agent(self, agent_name: str) -> bool:
        """Delete an agent"""
        if agent_name in self.active_agents:
            # Remove from active agents
            del self.active_agents[agent_name]
            
            # Remove agent file
            agent_file = self.agents_dir / f"{agent_name.lower()}.json"
            if agent_file.exists():
                agent_file.unlink()
            
            print(f"🗑️ Agent '{agent_name}' deleted")
            return True
        return False
    
    def create_devops_pipeline_agent(self, repo_url: str = "") -> str:
        """Create a specialized DevOps pipeline agent"""
        agent_name = f"pipeline_{int(time.time())}"
        
        capabilities = [
            "code_analysis",
            "test_generation", 
            "docker_generation",
            "deployment",
            "optimization",
            "security_analysis"
        ]
        
        purpose = f"DevOps pipeline automation for repository: {repo_url or 'general'}"
        
        self.create_agent(agent_name, purpose, "python", capabilities)
        return agent_name
    
    def execute_pipeline_step(self, agent_name: str, step: str, repository_context: str = "") -> Dict[str, Any]:
        """Execute a specific pipeline step using an agent"""
        
        step_tasks = {
            "clone": ("Clone and analyze repository structure", "code_analysis"),
            "analyze": ("Perform comprehensive code analysis", "code_analysis"), 
            "tests": ("Generate and run comprehensive test suite", "test_generation"),
            "docker": ("Generate production-ready Docker configuration", "docker_generation"),
            "deploy": ("Create deployment strategy and configuration", "deployment"),
            "optimize": ("Analyze and optimize code performance", "optimization")
        }
        
        if step not in step_tasks:
            return {
                "success": False,
                "error": f"Unknown pipeline step: {step}",
                "content": ""
            }
        
        task_description, task_type = step_tasks[step]
        
        return self.execute_agent_task(
            agent_name=agent_name,
            task=task_description,
            context=repository_context,
            task_type=task_type
        )

# Global agent engine instance
agent_engine = None

def get_agent_engine() -> AgentEngine:
    """Get global agent engine instance"""
    global agent_engine
    if agent_engine is None:
        agent_engine = AgentEngine()
    return agent_engine

def test_agent_engine():
    """Test agent engine functionality"""
    try:
        engine = get_agent_engine()
        
        # Create test agent
        test_agent = engine.create_agent(
            name="test_agent",
            purpose="Testing agent functionality",
            language="python",
            capabilities=["code_analysis", "test_generation"]
        )
        
        print(f"✅ Test agent created: {test_agent['name']}")
        
        # Test task execution
        result = engine.execute_agent_task(
            agent_name="test_agent",
            task="Analyze this simple Python function",
            context="def hello_world(): return 'Hello, World!'",
            task_type="code_analysis"
        )
        
        if result["success"]:
            print("✅ Agent task execution test passed")
            print(f"Response: {result['content'][:100]}...")
        else:
            print("❌ Agent task execution test failed")
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent engine test error: {str(e)}")
        return False

if __name__ == "__main__":
    test_agent_engine()
