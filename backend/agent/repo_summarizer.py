"""
1INTERPRETER Repository Summarizer
AI-powered repository analysis and summarization
"""
import os
import git
import time
from pathlib import Path
from typing import Dict, List, Any

import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from llm.llm_wrapper import get_llm

class RepoSummarizer:
    """AI-enhanced repository analysis and summarization"""
    
    def __init__(self):
        self.llm = get_llm()
        self.workspace_dir = Path("workspace")
        self.workspace_dir.mkdir(exist_ok=True)
    
    def clone_and_analyze(self, repo_url: str) -> Dict[str, Any]:
        """Clone repository and perform comprehensive analysis"""
        
        start_time = time.time()
        
        try:
            # Extract repo name from URL
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            clone_path = self.workspace_dir / repo_name
            
            # Clone repository
            if clone_path.exists():
                import shutil
                shutil.rmtree(clone_path)
            
            print(f"🔄 Cloning repository: {repo_url}")
            repo = git.Repo.clone_from(repo_url, clone_path)
            
            # Analyze repository
            analysis = self._analyze_repository(clone_path)
            
            # Get AI insights
            ai_summary = self._get_ai_summary(analysis, repo_url)
            
            execution_time = time.time() - start_time
            
            summary = f"""📁 Repository Analysis Complete:
🔗 URL: {repo_url}
📊 Files: {analysis['file_stats']['total_files']}
🐍 Python Files: {analysis['file_stats']['python_files']}
📝 Lines: {analysis['code_stats']['total_lines']}
⏱️ Time: {execution_time:.2f}s"""
            
            return {
                "success": True,
                "summary": summary,
                "repository": repo_url,
                "clone_path": str(clone_path),
                "analysis": analysis,
                "ai_summary": ai_summary,
                "execution_time": execution_time
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "summary": f"❌ Repository analysis failed: {str(e)}"
            }
    
    def _analyze_repository(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze repository structure and content"""
        
        analysis = {
            "file_stats": self._analyze_file_structure(repo_path),
            "code_stats": self._analyze_code_content(repo_path),
            "project_info": self._detect_project_type(repo_path),
            "dependencies": self._analyze_dependencies(repo_path)
        }
        
        return analysis
    
    def _analyze_file_structure(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze file structure and organization"""
        
        stats = {
            "total_files": 0,
            "python_files": 0,
            "javascript_files": 0,
            "config_files": 0,
            "documentation_files": 0,
            "test_files": 0,
            "directories": 0
        }
        
        for item in repo_path.rglob("*"):
            if item.is_dir():
                stats["directories"] += 1
            elif item.is_file():
                stats["total_files"] += 1
                
                suffix = item.suffix.lower()
                name = item.name.lower()
                
                if suffix == ".py":
                    stats["python_files"] += 1
                    if "test" in name:
                        stats["test_files"] += 1
                elif suffix in [".js", ".jsx", ".ts", ".tsx"]:
                    stats["javascript_files"] += 1
                elif suffix in [".json", ".yml", ".yaml", ".toml", ".ini"]:
                    stats["config_files"] += 1
                elif suffix in [".md", ".rst", ".txt"] or name in ["readme", "license"]:
                    stats["documentation_files"] += 1
        
        return stats
    
    def _analyze_code_content(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze code content and complexity"""
        
        stats = {
            "total_lines": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "functions": 0,
            "classes": 0
        }
        
        for py_file in repo_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8')
                lines = content.splitlines()
                
                stats["total_lines"] += len(lines)
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        stats["blank_lines"] += 1
                    elif line.startswith("#"):
                        stats["comment_lines"] += 1
                    else:
                        stats["code_lines"] += 1
                        
                        # Simple function/class counting
                        if line.startswith("def "):
                            stats["functions"] += 1
                        elif line.startswith("class "):
                            stats["classes"] += 1
                            
            except:
                continue
        
        return stats
    
    def _detect_project_type(self, repo_path: Path) -> Dict[str, Any]:
        """Detect project type and framework"""
        
        project_info = {
            "type": "unknown",
            "framework": "unknown",
            "language": "unknown",
            "build_tool": "unknown"
        }
        
        # Check for Python projects
        if (repo_path / "requirements.txt").exists() or (repo_path / "setup.py").exists():
            project_info["language"] = "python"
            project_info["type"] = "python_project"
            
            # Check for specific frameworks
            if (repo_path / "manage.py").exists():
                project_info["framework"] = "django"
            elif any(f.name == "app.py" for f in repo_path.rglob("app.py")):
                project_info["framework"] = "flask"
            elif (repo_path / "pyproject.toml").exists():
                project_info["build_tool"] = "poetry"
        
        # Check for Node.js projects
        elif (repo_path / "package.json").exists():
            project_info["language"] = "javascript"
            project_info["type"] = "node_project"
            
            try:
                import json
                with open(repo_path / "package.json") as f:
                    package_data = json.load(f)
                    dependencies = package_data.get("dependencies", {})
                    
                    if "react" in dependencies:
                        project_info["framework"] = "react"
                    elif "vue" in dependencies:
                        project_info["framework"] = "vue"
                    elif "express" in dependencies:
                        project_info["framework"] = "express"
            except:
                pass
        
        return project_info
    
    def _analyze_dependencies(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze project dependencies"""
        
        dependencies = {
            "python": [],
            "javascript": [],
            "total_count": 0
        }
        
        # Python dependencies
        req_file = repo_path / "requirements.txt"
        if req_file.exists():
            try:
                content = req_file.read_text()
                deps = [line.split("==")[0].split(">=")[0].strip() 
                       for line in content.splitlines() 
                       if line.strip() and not line.startswith("#")]
                dependencies["python"] = deps[:10]  # Limit to top 10
                dependencies["total_count"] += len(deps)
            except:
                pass
        
        # JavaScript dependencies
        package_file = repo_path / "package.json"
        if package_file.exists():
            try:
                import json
                with open(package_file) as f:
                    package_data = json.load(f)
                    deps = list(package_data.get("dependencies", {}).keys())
                    dependencies["javascript"] = deps[:10]  # Limit to top 10
                    dependencies["total_count"] += len(deps)
            except:
                pass
        
        return dependencies
    
    def _get_ai_summary(self, analysis: Dict[str, Any], repo_url: str) -> str:
        """Generate AI-powered repository summary"""
        
        try:
            prompt = f"""
Analyze this repository and provide a comprehensive summary:

REPOSITORY: {repo_url}

FILE STRUCTURE:
- Total Files: {analysis['file_stats']['total_files']}
- Python Files: {analysis['file_stats']['python_files']}
- Test Files: {analysis['file_stats']['test_files']}
- Documentation: {analysis['file_stats']['documentation_files']}

PROJECT INFO:
- Type: {analysis['project_info']['type']}
- Language: {analysis['project_info']['language']}
- Framework: {analysis['project_info']['framework']}

CODE METRICS:
- Total Lines: {analysis['code_stats']['total_lines']}
- Functions: {analysis['code_stats']['functions']}
- Classes: {analysis['code_stats']['classes']}

DEPENDENCIES:
- Python: {', '.join(analysis['dependencies']['python'][:5])}
- Total Dependencies: {analysis['dependencies']['total_count']}

Provide:
1. Project purpose and description
2. Technical assessment
3. Code quality evaluation
4. Recommended next steps
5. Potential improvements
"""
            
            result = self.llm.generate_response(prompt, "", "code_analysis")
            return result["content"]
            
        except:
            return f"""Repository Summary:
- Language: {analysis['project_info']['language']}
- Framework: {analysis['project_info']['framework']}  
- Files: {analysis['file_stats']['total_files']}
- Lines of Code: {analysis['code_stats']['total_lines']}
- Dependencies: {analysis['dependencies']['total_count']}

AI analysis unavailable. Basic metrics provided."""

if __name__ == "__main__":
    summarizer = RepoSummarizer()
    result = summarizer.clone_and_analyze("https://github.com/example/repo.git")
    print(result["summary"])
