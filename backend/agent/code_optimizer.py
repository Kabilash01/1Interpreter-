"""
1INTERPRETER Code Optimizer  
AI-powered code analysis and optimization engine
"""
import os
import ast
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from llm.llm_wrapper import get_llm

class CodeOptimizer:
    """AI-powered code optimization and improvement suggestions"""
    
    def __init__(self):
        self.llm = get_llm()
        self.reports_dir = Path("optimization_reports")
        self.reports_dir.mkdir(exist_ok=True)
    
    def optimize_codebase(self, project_path: str = ".") -> Dict[str, Any]:
        """Perform comprehensive code optimization analysis"""
        
        start_time = time.time()
        project_path = Path(project_path)
        
        try:
            # Analyze project structure
            project_analysis = self._analyze_project_structure(project_path)
            
            # Perform code analysis
            code_analysis = self._analyze_code_quality(project_path)
            
            # Get AI optimization suggestions
            ai_suggestions = self._get_ai_optimization_suggestions(project_analysis, code_analysis)
            
            # Generate optimization report
            report = self._generate_optimization_report(
                project_analysis, code_analysis, ai_suggestions
            )
            
            # Save report
            report_file = self._save_optimization_report(report)
            
            execution_time = time.time() - start_time
            
            summary = f"""⚡ Code Optimization Analysis Complete:
📁 Project: {project_path.name}
📊 Files Analyzed: {project_analysis['total_files']}
📈 Issues Found: {len(code_analysis.get('issues', []))}
💡 AI Suggestions: {len(ai_suggestions.get('suggestions', []))}
⏱️ Analysis Time: {execution_time:.2f}s
📄 Report: {report_file}"""
            
            return {
                "success": True,
                "summary": summary,
                "report_file": str(report_file),
                "project_analysis": project_analysis,
                "code_analysis": code_analysis,
                "ai_suggestions": ai_suggestions,
                "execution_time": execution_time
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "summary": f"❌ Code optimization failed: {str(e)}"
            }
    
    def _analyze_project_structure(self, project_path: Path) -> Dict[str, Any]:
        """Analyze overall project structure and metrics"""
        
        analysis = {
            "total_files": 0,
            "python_files": 0,
            "lines_of_code": 0,
            "complexity_score": 0,
            "file_sizes": [],
            "large_files": [],
            "empty_files": [],
            "structure": {
                "has_tests": False,
                "has_docs": False,
                "has_requirements": False,
                "has_config": False
            }
        }
        
        # Analyze Python files
        python_files = list(project_path.rglob("*.py"))
        analysis["python_files"] = len(python_files)
        analysis["total_files"] = len(list(project_path.rglob("*")))
        
        for py_file in python_files:
            try:
                content = py_file.read_text(encoding='utf-8')
                lines = len(content.splitlines())
                analysis["lines_of_code"] += lines
                
                file_size = py_file.stat().st_size
                analysis["file_sizes"].append(file_size)
                
                # Check for large files (>500 lines or >50KB)
                if lines > 500 or file_size > 50000:
                    analysis["large_files"].append(str(py_file))
                
                # Check for empty files
                if lines < 5:
                    analysis["empty_files"].append(str(py_file))
                
                # Calculate complexity (simple metric)
                complexity = self._calculate_file_complexity(content)
                analysis["complexity_score"] += complexity
                
            except Exception:
                continue
        
        # Check project structure
        analysis["structure"]["has_tests"] = any(
            p.exists() for p in [project_path / "tests", project_path / "test"]
        )
        analysis["structure"]["has_docs"] = any(
            p.exists() for p in [project_path / "docs", project_path / "README.md"]
        )
        analysis["structure"]["has_requirements"] = (project_path / "requirements.txt").exists()
        analysis["structure"]["has_config"] = any(
            (project_path / f).exists() for f in ["setup.py", "pyproject.toml", "setup.cfg"]
        )
        
        return analysis
    
    def _calculate_file_complexity(self, content: str) -> int:
        """Calculate simple complexity score for a Python file"""
        try:
            tree = ast.parse(content)
            complexity = 0
            
            for node in ast.walk(tree):
                # Count decision points
                if isinstance(node, (ast.If, ast.While, ast.For, ast.Try)):
                    complexity += 1
                elif isinstance(node, ast.FunctionDef):
                    complexity += 1
                elif isinstance(node, ast.ClassDef):
                    complexity += 2
            
            return complexity
        except:
            return 0
    
    def _analyze_code_quality(self, project_path: Path) -> Dict[str, Any]:
        """Analyze code quality and identify issues"""
        
        issues = []
        quality_metrics = {
            "long_functions": 0,
            "deep_nesting": 0,
            "missing_docstrings": 0,
            "too_many_parameters": 0,
            "duplicate_code": 0
        }
        
        python_files = list(project_path.rglob("*.py"))
        
        for py_file in python_files:
            try:
                content = py_file.read_text(encoding='utf-8')
                tree = ast.parse(content)
                
                # Analyze functions
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Check function length
                        func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                        if func_lines > 50:
                            quality_metrics["long_functions"] += 1
                            issues.append({
                                "file": str(py_file),
                                "line": node.lineno,
                                "type": "long_function",
                                "message": f"Function '{node.name}' is too long ({func_lines} lines)"
                            })
                        
                        # Check parameter count
                        param_count = len(node.args.args)
                        if param_count > 6:
                            quality_metrics["too_many_parameters"] += 1
                            issues.append({
                                "file": str(py_file),
                                "line": node.lineno,
                                "type": "too_many_parameters",
                                "message": f"Function '{node.name}' has too many parameters ({param_count})"
                            })
                        
                        # Check for docstring
                        if not ast.get_docstring(node):
                            quality_metrics["missing_docstrings"] += 1
                            issues.append({
                                "file": str(py_file),
                                "line": node.lineno,
                                "type": "missing_docstring",
                                "message": f"Function '{node.name}' missing docstring"
                            })
                    
                    # Check for deep nesting
                    if self._check_deep_nesting(node):
                        quality_metrics["deep_nesting"] += 1
                        issues.append({
                            "file": str(py_file),
                            "line": getattr(node, 'lineno', 0),
                            "type": "deep_nesting",
                            "message": "Code has deep nesting (>4 levels)"
                        })
                        
            except Exception as e:
                issues.append({
                    "file": str(py_file),
                    "line": 0,
                    "type": "parse_error",
                    "message": f"Could not parse file: {str(e)}"
                })
        
        return {
            "issues": issues,
            "quality_metrics": quality_metrics,
            "total_issues": len(issues)
        }
    
    def _check_deep_nesting(self, node) -> bool:
        """Check if code has deep nesting levels"""
        def count_nesting_level(n, level=0):
            if isinstance(n, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                level += 1
                if level > 4:
                    return True
            
            for child in ast.iter_child_nodes(n):
                if count_nesting_level(child, level):
                    return True
            return False
        
        return count_nesting_level(node)
    
    def _get_ai_optimization_suggestions(self, project_analysis: Dict[str, Any], 
                                       code_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI-powered optimization suggestions"""
        
        try:
            # Create comprehensive analysis prompt
            prompt = f"""
Analyze this Python project and provide optimization recommendations:

PROJECT METRICS:
- Total Files: {project_analysis['total_files']}
- Python Files: {project_analysis['python_files']}
- Lines of Code: {project_analysis['lines_of_code']}
- Complexity Score: {project_analysis['complexity_score']}
- Large Files: {len(project_analysis['large_files'])}

PROJECT STRUCTURE:
- Has Tests: {project_analysis['structure']['has_tests']}
- Has Documentation: {project_analysis['structure']['has_docs']}
- Has Requirements: {project_analysis['structure']['has_requirements']}

CODE QUALITY ISSUES:
- Long Functions: {code_analysis['quality_metrics']['long_functions']}
- Deep Nesting: {code_analysis['quality_metrics']['deep_nesting']}
- Missing Docstrings: {code_analysis['quality_metrics']['missing_docstrings']}
- Too Many Parameters: {code_analysis['quality_metrics']['too_many_parameters']}
- Total Issues: {code_analysis['total_issues']}

Provide specific, actionable optimization recommendations covering:
1. Code structure improvements
2. Performance optimizations
3. Maintainability enhancements
4. Best practices implementation
5. Testing strategy
6. Documentation improvements
"""
            
            ai_result = self.llm.generate_response(prompt, "", "optimization")
            
            # Parse AI suggestions into categories
            suggestions = self._parse_ai_suggestions(ai_result["content"])
            
            return {
                "ai_analysis": ai_result["content"],
                "suggestions": suggestions,
                "priority_recommendations": self._prioritize_recommendations(
                    project_analysis, code_analysis
                )
            }
            
        except Exception as e:
            return {
                "ai_analysis": f"AI analysis failed: {str(e)}",
                "suggestions": self._get_fallback_suggestions(project_analysis, code_analysis),
                "priority_recommendations": []
            }
    
    def _parse_ai_suggestions(self, ai_content: str) -> List[Dict[str, Any]]:
        """Parse AI suggestions into structured format"""
        
        suggestions = []
        lines = ai_content.split('\\n')
        
        current_category = "General"
        current_suggestion = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for category headers
            if any(keyword in line.lower() for keyword in 
                   ['structure', 'performance', 'maintainability', 'testing', 'documentation']):
                current_category = line
                continue
            
            # Check for numbered or bulleted items
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '*')):
                if current_suggestion:
                    suggestions.append({
                        "category": current_category,
                        "description": current_suggestion,
                        "priority": "medium"
                    })
                current_suggestion = line
            else:
                current_suggestion += " " + line
        
        # Add last suggestion
        if current_suggestion:
            suggestions.append({
                "category": current_category,
                "description": current_suggestion,
                "priority": "medium"
            })
        
        return suggestions
    
    def _get_fallback_suggestions(self, project_analysis: Dict[str, Any], 
                                code_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate fallback suggestions when AI is unavailable"""
        
        suggestions = []
        
        # Structure suggestions
        if not project_analysis["structure"]["has_tests"]:
            suggestions.append({
                "category": "Testing",
                "description": "Add comprehensive test suite using pytest",
                "priority": "high"
            })
        
        if not project_analysis["structure"]["has_docs"]:
            suggestions.append({
                "category": "Documentation",
                "description": "Add README.md and inline documentation",
                "priority": "medium"
            })
        
        # Code quality suggestions
        if code_analysis["quality_metrics"]["long_functions"] > 0:
            suggestions.append({
                "category": "Code Structure",
                "description": "Break down long functions into smaller, focused functions",
                "priority": "high"
            })
        
        if code_analysis["quality_metrics"]["missing_docstrings"] > 5:
            suggestions.append({
                "category": "Documentation",
                "description": "Add docstrings to functions and classes",
                "priority": "medium"
            })
        
        if len(project_analysis["large_files"]) > 0:
            suggestions.append({
                "category": "Code Structure", 
                "description": "Split large files into smaller modules",
                "priority": "medium"
            })
        
        return suggestions
    
    def _prioritize_recommendations(self, project_analysis: Dict[str, Any], 
                                  code_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate priority recommendations based on analysis"""
        
        recommendations = []
        
        # High priority: Critical structural issues
        if not project_analysis["structure"]["has_tests"]:
            recommendations.append({
                "priority": "HIGH",
                "category": "Testing",
                "action": "Implement comprehensive test suite",
                "impact": "Improves code reliability and maintainability"
            })
        
        if code_analysis["total_issues"] > 20:
            recommendations.append({
                "priority": "HIGH", 
                "category": "Code Quality",
                "action": "Address code quality issues systematically",
                "impact": "Reduces bugs and improves maintainability"
            })
        
        # Medium priority: Performance and structure
        if project_analysis["complexity_score"] > 100:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Performance",
                "action": "Reduce code complexity through refactoring",
                "impact": "Improves performance and readability"
            })
        
        if len(project_analysis["large_files"]) > 3:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Structure",
                "action": "Split large files into smaller modules",
                "impact": "Improves code organization and maintainability"
            })
        
        # Low priority: Documentation and polish
        if not project_analysis["structure"]["has_docs"]:
            recommendations.append({
                "priority": "LOW",
                "category": "Documentation",
                "action": "Add comprehensive documentation",
                "impact": "Improves developer experience and onboarding"
            })
        
        return recommendations
    
    def _generate_optimization_report(self, project_analysis: Dict[str, Any],
                                    code_analysis: Dict[str, Any],
                                    ai_suggestions: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive optimization report"""
        
        return {
            "timestamp": time.time(),
            "project_name": "Unknown",
            "analysis": {
                "project_metrics": project_analysis,
                "code_quality": code_analysis,
                "ai_insights": ai_suggestions
            },
            "summary": {
                "total_files": project_analysis["total_files"],
                "lines_of_code": project_analysis["lines_of_code"],
                "complexity_score": project_analysis["complexity_score"],
                "total_issues": code_analysis["total_issues"],
                "suggestions_count": len(ai_suggestions.get("suggestions", []))
            }
        }
    
    def _save_optimization_report(self, report: Dict[str, Any]) -> Path:
        """Save optimization report to file"""
        
        timestamp = int(time.time())
        report_file = self.reports_dir / f"optimization_report_{timestamp}.json"
        
        import json
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return report_file

if __name__ == "__main__":
    optimizer = CodeOptimizer()
    result = optimizer.optimize_codebase()
    
    if result["success"]:
        print(result["summary"])
    else:
        print(f"❌ Error: {result['error']}")
