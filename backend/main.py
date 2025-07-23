"""
1INTERPRETER Backend Main
Core backend service for AI-powered DevOps automation
"""
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add backend to path for imports
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

try:
    from llm.llm_wrapper import get_llm, test_llm_connection
    from llm.agent_engine import get_agent_engine
    from agent.docker_deployer import DockerDeployer
    from agent.code_optimizer import CodeOptimizer
    from agent.test_generator import TestGenerator
    from agent.static_analyzer import StaticAnalyzer
    from agent.repo_summarizer import RepoSummarizer
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔧 Attempting alternative import method...")
    
    # Alternative import approach
    import importlib.util
    
    def load_module_from_path(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    # Load modules directly
    llm_wrapper = load_module_from_path("llm_wrapper", backend_path / "llm" / "llm_wrapper.py")
    get_llm = llm_wrapper.get_llm
    test_llm_connection = getattr(llm_wrapper, 'test_llm_connection', None)

class Backend:
    """Main backend service for 1INTERPRETER"""
    
    def __init__(self):
        self.llm = get_llm()
        self.agent_engine = get_agent_engine()
        
        # Initialize specialized agents
        self.docker_deployer = DockerDeployer()
        self.code_optimizer = CodeOptimizer()
        self.test_generator = TestGenerator()
        self.static_analyzer = StaticAnalyzer()
        self.repo_summarizer = RepoSummarizer()
        
        print("1INTERPRETER Backend initialized")
    
    def execute_command(self, command: str, argument: str = "") -> Dict[str, Any]:
        """Execute a backend command"""
        
        start_time = time.time()
        
        try:
            if command == "clone":
                return self.handle_clone(argument)
            elif command == "analyze":
                return self.handle_analyze(argument)
            elif command == "tests":
                return self.handle_tests(argument)
            elif command == "docker":
                return self.handle_docker(argument)
            elif command == "deploy":
                return self.handle_deploy(argument)
            elif command == "optimize":
                return self.handle_optimize(argument)
            elif command == "agent":
                return self.handle_agent_creation(argument)
            elif command == "status":
                return self.handle_status()
            else:
                return {
                    "success": False,
                    "error": f"Unknown command: {command}",
                    "content": "",
                    "duration": time.time() - start_time
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": "",
                "duration": time.time() - start_time
            }
    
    def handle_clone(self, repo_url: str) -> Dict[str, Any]:
        """Handle repository cloning and initial analysis"""
        if not repo_url:
            return {"success": False, "error": "Repository URL required"}
        
        try:
            # Use repo summarizer to clone and analyze
            result = self.repo_summarizer.clone_and_analyze(repo_url)
            
            return {
                "success": True,
                "content": f"Repository cloned and analyzed: {repo_url}\\n{result['summary']}",
                "data": result,
                "repository": repo_url
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Clone failed: {str(e)}",
                "content": ""
            }
    
    def handle_analyze(self, target: str) -> Dict[str, Any]:
        """Handle code analysis"""
        try:
            result = self.static_analyzer.analyze_codebase(target or ".")
            
            return {
                "success": True,
                "content": f"Code analysis completed\\n{result['summary']}",
                "data": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Analysis failed: {str(e)}",
                "content": ""
            }
    
    def handle_tests(self, target: str) -> Dict[str, Any]:
        """Handle test generation and execution"""
        try:
            result = self.test_generator.generate_tests(target or ".")
            
            return {
                "success": True,
                "content": f"✅ Tests generated and executed\\n{result['summary']}",
                "data": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Test generation failed: {str(e)}",
                "content": ""
            }
    
    def handle_docker(self, project_path: str) -> Dict[str, Any]:
        """Handle Docker deployment file generation"""
        try:
            result = self.docker_deployer.generate_deployment_files(project_path or ".")
            
            return {
                "success": True,
                "content": f"🐳 Docker deployment files created\\n{result['summary']}",
                "data": result,
                "files_created": result.get('files', [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Docker generation failed: {str(e)}",
                "content": ""
            }
    
    def handle_deploy(self, target: str) -> Dict[str, Any]:
        """Handle deployment operations"""
        try:
            # Create deployment strategy using AI
            deployment_result = self.llm.create_deployment_strategy(
                project_info=f"Deploy project from: {target or 'current directory'}",
                target="kubernetes"
            )
            
            return {
                "success": True,
                "content": f"🚀 Deployment strategy created\\n{deployment_result['content']}",
                "data": deployment_result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Deployment failed: {str(e)}",
                "content": ""
            }
    
    def handle_optimize(self, target: str) -> Dict[str, Any]:
        """Handle code optimization"""
        try:
            result = self.code_optimizer.optimize_codebase(target or ".")
            
            return {
                "success": True,
                "content": f"⚡ Code optimization completed\\n{result['summary']}",
                "data": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Optimization failed: {str(e)}",
                "content": ""
            }
    
    def handle_agent_creation(self, agent_spec: str) -> Dict[str, Any]:
        """Handle AI agent creation"""
        try:
            # Parse agent specification (format: name:purpose:language)
            parts = agent_spec.split(":")
            if len(parts) < 2:
                return {
                    "success": False,
                    "error": "Agent spec format: name:purpose:language",
                    "content": ""
                }
            
            name = parts[0]
            purpose = parts[1] 
            language = parts[2] if len(parts) > 2 else "python"
            
            agent_config = self.agent_engine.create_agent(name, purpose, language)
            
            return {
                "success": True,
                "content": f"🤖 Agent '{name}' created successfully",
                "data": agent_config
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Agent creation failed: {str(e)}",
                "content": ""
            }
    
    def handle_status(self) -> Dict[str, Any]:
        """Handle system status check"""
        try:
            # Test LLM connection
            llm_status = test_llm_connection()
            
            # Get agent count
            agents = self.agent_engine.list_agents()
            
            status_info = {
                "llm_connected": llm_status,
                "agent_count": len(agents),
                "backend_version": "1.0.0",
                "timestamp": time.time()
            }
            
            return {
                "success": True,
                "content": f"✅ 1INTERPRETER Backend Status:\\nLLM Connected: {llm_status}\\nActive Agents: {len(agents)}",
                "data": status_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Status check failed: {str(e)}",
                "content": ""
            }

def main():
    """Main entry point for backend commands"""
    parser = argparse.ArgumentParser(description="1INTERPRETER Backend")
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("argument", nargs="?", default="", help="Command argument")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Initialize backend
    backend = Backend()
    
    # Execute command
    result = backend.execute_command(args.command, args.argument)
    
    # Output result
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False).encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
    else:
        if result["success"]:
            # Handle Unicode encoding issues
            content = result.get("content", "")
            try:
                print(content)
            except UnicodeEncodeError:
                # Fallback: remove Unicode characters
                import re
                clean_content = re.sub(r'[^\x00-\x7F]+', '', content)
                print(clean_content)
        else:
            error = result.get('error', 'Unknown error')
            try:
                print(f"Error: {error}")
            except UnicodeEncodeError:
                import re
                clean_error = re.sub(r'[^\x00-\x7F]+', '', error)
                print(f"Error: {clean_error}")
            sys.exit(1)

if __name__ == "__main__":
    main()
