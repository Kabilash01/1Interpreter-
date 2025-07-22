"""
1INTERPRETER Static Analyzer
AI-powered static code analysis and quality assessment
"""
import ast
import time
from pathlib import Path
from typing import Dict, List, Any

import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from llm.llm_wrapper import get_llm

class StaticAnalyzer:
    """AI-enhanced static code analysis"""
    
    def __init__(self):
        self.llm = get_llm()
    
    def analyze_codebase(self, project_path: str = ".") -> Dict[str, Any]:
        """Perform comprehensive static analysis"""
        
        start_time = time.time()
        project_path = Path(project_path)
        
        try:
            # Basic metrics
            metrics = self._calculate_metrics(project_path)
            
            # Code quality analysis
            quality_issues = self._analyze_quality(project_path)
            
            # Security analysis
            security_issues = self._analyze_security(project_path)
            
            # AI insights
            ai_analysis = self._get_ai_insights(metrics, quality_issues, security_issues)
            
            execution_time = time.time() - start_time
            
            summary = f"""🔍 Static Analysis Complete:
📊 Files: {metrics['file_count']} | Lines: {metrics['line_count']}
⚠️ Issues: {len(quality_issues)} quality, {len(security_issues)} security
🧠 AI Insights: Generated recommendations
⏱️ Time: {execution_time:.2f}s"""
            
            return {
                "success": True,
                "summary": summary,
                "metrics": metrics,
                "quality_issues": quality_issues,
                "security_issues": security_issues,
                "ai_analysis": ai_analysis,
                "execution_time": execution_time
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "summary": f"❌ Analysis failed: {str(e)}"
            }
    
    def _calculate_metrics(self, project_path: Path) -> Dict[str, Any]:
        """Calculate basic code metrics"""
        
        metrics = {
            "file_count": 0,
            "line_count": 0,
            "function_count": 0,
            "class_count": 0,
            "complexity": 0
        }
        
        for py_file in project_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8')
                tree = ast.parse(content)
                
                metrics["file_count"] += 1
                metrics["line_count"] += len(content.splitlines())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        metrics["function_count"] += 1
                        metrics["complexity"] += 1
                    elif isinstance(node, ast.ClassDef):
                        metrics["class_count"] += 1
                    elif isinstance(node, (ast.If, ast.While, ast.For)):
                        metrics["complexity"] += 1
                        
            except:
                continue
        
        return metrics
    
    def _analyze_quality(self, project_path: Path) -> List[Dict[str, Any]]:
        """Analyze code quality issues"""
        
        issues = []
        
        for py_file in project_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8')
                lines = content.splitlines()
                
                # Check for long lines
                for i, line in enumerate(lines, 1):
                    if len(line) > 100:
                        issues.append({
                            "file": str(py_file),
                            "line": i,
                            "type": "long_line",
                            "severity": "minor",
                            "message": f"Line too long ({len(line)} characters)"
                        })
                
                # Check for TODO/FIXME comments
                for i, line in enumerate(lines, 1):
                    if any(keyword in line.upper() for keyword in ["TODO", "FIXME", "HACK"]):
                        issues.append({
                            "file": str(py_file),
                            "line": i,
                            "type": "technical_debt",
                            "severity": "minor",
                            "message": "Technical debt comment found"
                        })
                
            except:
                continue
        
        return issues
    
    def _analyze_security(self, project_path: Path) -> List[Dict[str, Any]]:
        """Analyze potential security issues"""
        
        security_issues = []
        
        dangerous_patterns = [
            ("eval(", "code_injection"),
            ("exec(", "code_injection"), 
            ("subprocess.call", "command_injection"),
            ("os.system", "command_injection"),
            ("pickle.load", "deserialization"),
            ("input(", "user_input")
        ]
        
        for py_file in project_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8')
                lines = content.splitlines()
                
                for i, line in enumerate(lines, 1):
                    for pattern, issue_type in dangerous_patterns:
                        if pattern in line:
                            security_issues.append({
                                "file": str(py_file),
                                "line": i,
                                "type": issue_type,
                                "severity": "high" if issue_type == "code_injection" else "medium",
                                "message": f"Potential {issue_type} vulnerability"
                            })
                            
            except:
                continue
        
        return security_issues
    
    def _get_ai_insights(self, metrics: Dict, quality_issues: List, security_issues: List) -> str:
        """Get AI-powered analysis insights"""
        
        try:
            prompt = f"""
Analyze this Python codebase metrics and provide insights:

METRICS:
- Files: {metrics['file_count']}
- Lines of Code: {metrics['line_count']}
- Functions: {metrics['function_count']}
- Classes: {metrics['class_count']}
- Complexity Score: {metrics['complexity']}

ISSUES FOUND:
- Quality Issues: {len(quality_issues)}
- Security Issues: {len(security_issues)}

Provide analysis on:
1. Overall code health
2. Areas for improvement
3. Security recommendations
4. Performance considerations
"""
            
            result = self.llm.generate_response(prompt, "", "code_analysis")
            return result["content"]
            
        except:
            return "AI analysis unavailable. Basic metrics analysis completed."

if __name__ == "__main__":
    analyzer = StaticAnalyzer()
    result = analyzer.analyze_codebase()
    print(result["summary"])
