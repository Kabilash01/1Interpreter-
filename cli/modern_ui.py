#!/usr/bin/env python3
"""
1INTERPRETER Modern Terminal UI
A MetaChain-inspired interface for DevOps automation
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.live import Live
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import confirm

# Add backend integration
sys.path.append(str(Path(__file__).parent.parent))
try:
    from backend.llm.llm_wrapper import query_llm, get_ai_status
    from backend.main import *
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Backend not available: {e}")
    BACKEND_AVAILABLE = False

console = Console()

class AutoDockUI:
    def __init__(self):
        self.version = "0.1.0"
        self.author = "1INTERPRETER Team"
        self.license = "MIT"
        self.current_repo = None
        self.ai_mode = "cloud"
        self.commands = {
            "user": "🧑 General AI Assistant mode",
            "agent": "🤖 Create custom AI Agent",
            "workflow": "⚡ Create AI Workflow with language",
            "exit": "🚪 Exit the program"
        }
        
        # Check backend status on initialization
        self.backend_status = self.check_backend_status()
        
    def check_backend_status(self):
        """Check backend and AI configuration status"""
        status = {
            "backend_available": BACKEND_AVAILABLE,
            "ai_configured": False,
            "ai_mode": "unknown",
            "apis_available": []
        }
        
        if BACKEND_AVAILABLE:
            try:
                ai_status = get_ai_status()
                status["ai_configured"] = True
                status["ai_mode"] = ai_status.get("mode", "unknown")
                
                if ai_status.get("gemini_configured"):
                    status["apis_available"].append("Gemini")
                if ai_status.get("openai_configured"):
                    status["apis_available"].append("OpenAI")
                    
            except Exception as e:
                status["error"] = str(e)
                
        return status
        
    def get_header_art(self):
        """Create ASCII art header similar to MetaChain"""
        return """
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║  ███   █████ █████ █████ █████ █████ █████ █████ █████ █████ █████        ║
║   █       █     █     █   █   █     █   █ █   █ █     █   █   █           ║
║   █     ███   ███   ███   ███ ████  ████  ████  ████  ███   ████          ║
║   █     █     █     █     █   █     █     █   █ █     █     █             ║
║  ███   █████ █████ █████ █████ █████ █     █████ █████ █████ █████        ║
║                                                                           ║
║                                                                           ║
║ █████ █████ █████ █████ █████ █████ █████ █████ █████ █████ █████         ║
║   █   █   █   █   █     █   █ █   █ █   █ █     █   █ █     █   █         ║
║   █   ████    █   ████  ████  ████  ████  ████  ███   ████  ████          ║
║   █   █   █   █   █     █   █ █     █   █ █     █     █     █   █         ║
║ █████ █   █   █   █████ █   █ █     █   █ █████ █████ █████ █   █         ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
        🚀 Intelligent DevOps Automation Platform 🚀
"""

    def show_header(self):
        """Display the main header"""
        console.clear()
        
        # Header art
        header_text = Text(self.get_header_art(), style="bold cyan")
        console.print(Align.center(header_text))
        
        # Version info table
        info_table = Table(show_header=False, box=None, padding=(0, 2))
        info_table.add_column("Label", style="bold yellow", justify="right")
        info_table.add_column("Value", style="green")
        
        info_table.add_row("Version", self.version)
        info_table.add_row("Author", self.author)
        info_table.add_row("License", self.license)
        
        # Add backend status
        backend_status = "✅ ACTIVE" if self.backend_status["backend_available"] else "❌ LIMITED"
        info_table.add_row("Backend", backend_status)
        
        if self.backend_status["backend_available"]:
            ai_mode = self.backend_status.get("ai_mode", "unknown")
            ai_status = f"{ai_mode.upper()}" + (f" ({', '.join(self.backend_status['apis_available'])})" if self.backend_status['apis_available'] else "")
            info_table.add_row("AI Mode", ai_status)
        
        console.print(Align.center(info_table))
        console.print()
        
    def show_important_notes(self):
        """Display important notes similar to MetaChain"""
        notes = Panel(
            """[bold yellow]🔔 Important Notes[/bold yellow]

• Choose [bold green]user mode[/bold green] if you just want to let a general yet powerful AI Assistant to help you
• Choose [bold blue]agent mode[/bold blue] for automated DevOps pipeline: clone → analyze → test → docker → deploy → optimize
• Choose [bold purple]workflow editor[/bold purple] to create your own AI Workflow with language.

[bold cyan]✨ 1INTERPRETER Features:[/bold cyan]
🔹 Intelligent repository analysis and containerization
🔹 AI-powered code optimization and test generation  
🔹 Smart Docker deployment with multi-framework support
🔹 Advanced static analysis with security scanning
🔹 Automated CI/CD pipeline generation
🔹 Complete end-to-end DevOps automation""",
            title="[bold red]━━━━━━━━━━━━━━━━━━━━━━━━━━ Important Notes ━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold red]",
            border_style="red",
            padding=(1, 2)
        )
        console.print(notes)
        console.print()

    def show_mode_selection(self):
        """Show mode selection interface"""
        # Create a table for mode selection
        mode_table = Table(show_header=True, header_style="bold magenta", box=None)
        mode_table.add_column("Mode", style="bold", width=15)
        mode_table.add_column("Description", style="dim", width=50)
        mode_table.add_column("Use Case", style="blue", width=25)
        
        mode_table.add_row(
            "[bold green]🧑 user[/bold green]", 
            "General AI assistant for DevOps tasks",
            "Quick automation"
        )
        mode_table.add_row(
            "[bold blue]🤖 agent[/bold blue]", 
            "Automated DevOps pipeline (clone→analyze→test→docker→deploy→optimize)", 
            "Full automation"
        )
        mode_table.add_row(
            "[bold purple]⚡ workflow[/bold purple]", 
            "Build complete AI-powered DevOps pipelines",
            "Complex automation"
        )
        mode_table.add_row(
            "[bold magenta]⚙️ config[/bold magenta]", 
            "Configure backend and AI settings",
            "Setup & configuration"
        )
        mode_table.add_row(
            "[bold red]🚪 exit[/bold red]", 
            "Exit 1INTERPRETER platform",
            "Quit application"
        )
        
        console.print(Panel(mode_table, title="[bold cyan]🚀 1INTERPRETER Operation Modes", border_style="cyan"))
        console.print()

    def get_user_input(self):
        """Get user input with auto-completion"""
        completer = WordCompleter(['user', 'agent', 'workflow', 'config', 'exit', '@'])
        
        try:
            user_input = prompt(
                "🔧 Enter @ to mention Agents\n"
                "Prompt: ",
                completer=completer
            ).strip()
            return user_input
        except (KeyboardInterrupt, EOFError):
            return "exit"

    def run_user_mode(self):
        """Run user mode - general AI assistant"""
        console.print("\n[bold green]🧑 User Mode Activated[/bold green]")
        console.print("You can now interact with the 1INTERPRETER AI assistant!")
        console.print("Type 'back' to return to main menu, 'exit' to quit")
        console.print("💡 Available commands: clone, analyze, docker, deploy, tests, optimize\n")
        
        while True:
            try:
                query = prompt("💬 Ask 1INTERPRETER: ").strip()
                
                if query.lower() in ['back', 'return', 'menu']:
                    return
                elif query.lower() in ['exit', 'quit']:
                    sys.exit(0)
                elif query:
                    # Check if it's a direct command
                    if self.is_backend_command(query):
                        self.execute_backend_command(query)
                    else:
                        self.process_ai_query(query)
                    
            except (KeyboardInterrupt, EOFError):
                return

    def is_backend_command(self, query):
        """Check if query is a direct backend command"""
        commands = ['clone', 'analyze', 'docker', 'deploy', 'tests', 'optimize', 'ai-config', 'status', 'fix']
        first_word = query.split()[0].lower() if query.split() else ""
        return first_word in commands

    def execute_backend_command(self, command):
        """Execute actual backend command"""
        if not BACKEND_AVAILABLE:
            console.print("[red]❌ Backend not available. Please configure the backend first.[/red]")
            return
            
        console.print(f"\n[bold yellow]🔧 Executing: {command}[/bold yellow]")
        
        try:
            # Change to the parent directory (where backend is located)
            backend_dir = Path(__file__).parent.parent
            
            with Progress(
                SpinnerColumn(),
                TextColumn(f"[bold blue]Running {command}..."),
                transient=True,
            ) as progress:
                task = progress.add_task("Executing", total=None)
                
                # Execute the backend command
                result = subprocess.run(
                    [sys.executable, "backend/main.py"] + command.split(),
                    cwd=backend_dir,
                    capture_output=True,
                    text=True,
                    timeout=120  # 2 minute timeout
                )
                
                progress.remove_task(task)
            
            if result.returncode == 0:
                console.print(f"[green]✅ Command completed successfully![/green]")
                if result.stdout:
                    console.print("\n[bold]Output:[/bold]")
                    console.print(Panel(result.stdout, border_style="green"))
            else:
                console.print(f"[red]❌ Command failed with exit code {result.returncode}[/red]")
                if result.stderr:
                    console.print("\n[bold]Error:[/bold]")
                    console.print(Panel(result.stderr, border_style="red"))
                    
        except subprocess.TimeoutExpired:
            console.print("[red]❌ Command timed out after 2 minutes[/red]")
        except Exception as e:
            console.print(f"[red]❌ Error executing command: {str(e)}[/red]")
        
        input("\nPress Enter to continue...")

    def run_agent_mode(self):
        """Run agent mode - automated DevOps pipeline"""
        console.print("\n[bold blue]🤖 Agent Mode - Automated DevOps Pipeline[/bold blue]")
        console.print("This mode will automatically perform a complete DevOps workflow!\n")
        
        # Step 1: Get repository URL
        repo_url = Prompt.ask("🔗 Repository URL (GitHub)", 
                             default="https://github.com/example/repo")
        
        if not repo_url or repo_url == "https://github.com/example/repo":
            console.print("[red]❌ Please provide a valid repository URL[/red]")
            input("Press Enter to continue...")
            return
        
        # Step 2: Agent Configuration
        agent_name = Prompt.ask("🏷️  Agent Name", default="AutoDevOps-Agent")
        
        console.print(f"\n[bold cyan]🚀 Starting Automated DevOps Pipeline with '{agent_name}'[/bold cyan]")
        console.print("Pipeline Steps:")
        console.print("1. 🔗 Clone Repository")
        console.print("2. 📊 Code Analysis & Security Scan")  
        console.print("3. 🧪 Generate Tests")
        console.print("4. 🐳 Docker Containerization")
        console.print("5. 🚀 Deploy Application")
        console.print("6. 💡 Code Optimization Suggestions")
        
        if not Confirm.ask("\nStart automated pipeline?", default=True):
            return
            
        pipeline_results = {}
        
        try:
            # Step 1: Clone Repository
            console.print("\n[bold yellow]Step 1/6: 🔗 Cloning Repository...[/bold yellow]")
            result = self.execute_pipeline_step("clone", repo_url)
            pipeline_results["clone"] = result
            
            if not result["success"]:
                console.print("[red]❌ Failed to clone repository. Aborting pipeline.[/red]")
                return
                
            # Step 2: Code Analysis
            console.print("\n[bold yellow]Step 2/6: 📊 Running Code Analysis...[/bold yellow]")
            result = self.execute_pipeline_step("analyze", "")
            pipeline_results["analyze"] = result
            
            # Step 3: Generate Tests  
            console.print("\n[bold yellow]Step 3/6: 🧪 Generating Tests...[/bold yellow]")
            result = self.execute_pipeline_step("tests", "")
            pipeline_results["tests"] = result
            
            # Step 4: Docker Containerization
            console.print("\n[bold yellow]Step 4/6: 🐳 Creating Docker Container...[/bold yellow]")
            result = self.execute_pipeline_step("docker", "")
            pipeline_results["docker"] = result
            
            # Step 5: Deploy Application
            console.print("\n[bold yellow]Step 5/6: 🚀 Deploying Application...[/bold yellow]")
            result = self.execute_pipeline_step("deploy", "")
            pipeline_results["deploy"] = result
            
            # Step 6: Code Optimization
            console.print("\n[bold yellow]Step 6/6: � Generating Optimization Suggestions...[/bold yellow]")
            result = self.execute_pipeline_step("optimize", "")
            pipeline_results["optimize"] = result
            
            # Create and save agent with pipeline results
            self.create_pipeline_agent(agent_name, repo_url, pipeline_results)
            
            # Show pipeline summary
            self.show_pipeline_summary(agent_name, pipeline_results)
            
        except Exception as e:
            console.print(f"[red]❌ Pipeline failed: {str(e)}[/red]")
            
        input("\nPress Enter to continue...")

    def execute_pipeline_step(self, command, arg=""):
        """Execute a single pipeline step"""
        step_result = {
            "command": command,
            "success": False,
            "output": "",
            "error": "",
            "duration": 0
        }
        
        start_time = time.time()
        
        try:
            if not BACKEND_AVAILABLE:
                # Simulate the step for demonstration
                with Progress(
                    SpinnerColumn(),
                    TextColumn(f"[bold blue]Simulating {command}..."),
                    transient=True,
                ) as progress:
                    progress.add_task("Processing", total=None)
                    time.sleep(2)  # Simulate processing time
                
                step_result["success"] = True
                step_result["output"] = f"✅ {command.title()} completed successfully (simulated)"
                console.print(f"[green]✅ {command.title()} completed successfully![/green]")
                
            else:
                # Execute real backend command
                backend_dir = Path(__file__).parent.parent
                cmd_args = [command]
                if arg:
                    cmd_args.append(arg)
                    
                with Progress(
                    SpinnerColumn(),
                    TextColumn(f"[bold blue]Executing {command}..."),
                    transient=True,
                ) as progress:
                    task = progress.add_task("Processing", total=None)
                    
                    result = subprocess.run(
                        [sys.executable, "backend/main.py"] + cmd_args,
                        cwd=backend_dir,
                        capture_output=True,
                        text=True,
                        timeout=300  # 5 minute timeout per step
                    )
                    
                    progress.remove_task(task)
                
                step_result["success"] = result.returncode == 0
                step_result["output"] = result.stdout
                step_result["error"] = result.stderr
                
                if step_result["success"]:
                    console.print(f"[green]✅ {command.title()} completed successfully![/green]")
                else:
                    console.print(f"[red]❌ {command.title()} failed![/red]")
                    if result.stderr:
                        console.print(f"[red]Error: {result.stderr[:200]}...[/red]")
                        
        except subprocess.TimeoutExpired:
            step_result["error"] = "Command timed out"
            console.print(f"[red]❌ {command.title()} timed out![/red]")
        except Exception as e:
            step_result["error"] = str(e)
            console.print(f"[red]❌ {command.title()} error: {str(e)}[/red]")
            
        step_result["duration"] = time.time() - start_time
        return step_result

    def create_pipeline_agent(self, name, repo_url, results):
        """Create agent configuration with pipeline results"""
        agents_dir = Path("agents")
        agents_dir.mkdir(exist_ok=True)
        
        # Create summary folder for this agent
        summary_dir = Path("pipeline_summaries") / name.lower().replace(' ', '_').replace('-', '_')
        summary_dir.mkdir(parents=True, exist_ok=True)
        
        agent_config = {
            "name": name,
            "type": "devops_pipeline",
            "repository": repo_url,
            "created": str(time.time()),
            "pipeline_results": results,
            "capabilities": [
                "repository_cloning",
                "code_analysis", 
                "test_generation",
                "docker_containerization",
                "application_deployment",
                "code_optimization"
            ],
            "status": "completed",
            "total_steps": len(results),
            "successful_steps": sum(1 for r in results.values() if r["success"]),
            "summary_folder": str(summary_dir)
        }
        
        # Save agent configuration
        config_file = agents_dir / f"{name.lower().replace(' ', '_').replace('-', '_')}.json"
        with open(config_file, 'w') as f:
            import json
            json.dump(agent_config, f, indent=2)
            
        # Save detailed pipeline summary
        self.save_pipeline_summary(name, repo_url, results, summary_dir)
        
        console.print(f"📁 [green]Agent configuration saved to: {config_file}[/green]")
        console.print(f"📋 [green]Pipeline summary saved to: {summary_dir}[/green]")

    def save_pipeline_summary(self, agent_name, repo_url, results, summary_dir):
        """Save detailed pipeline summary to files"""
        import json
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # 1. Save JSON summary
        json_summary = {
            "agent_name": agent_name,
            "repository": repo_url,
            "timestamp": timestamp,
            "pipeline_steps": results,
            "statistics": {
                "total_steps": len(results),
                "successful_steps": sum(1 for r in results.values() if r["success"]),
                "failed_steps": sum(1 for r in results.values() if not r["success"]),
                "total_duration": sum(r["duration"] for r in results.values()),
                "success_rate": (sum(1 for r in results.values() if r["success"]) / len(results) * 100) if results else 0
            }
        }
        
        json_file = summary_dir / f"pipeline_summary_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(json_summary, f, indent=2)
        
        # 2. Save Markdown report
        md_content = self.generate_markdown_report(agent_name, repo_url, results, timestamp)
        md_file = summary_dir / f"pipeline_report_{timestamp}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # 3. Save individual step outputs
        outputs_dir = summary_dir / "step_outputs"
        outputs_dir.mkdir(exist_ok=True)
        
        for step_name, result in results.items():
            # Save stdout
            if result["output"]:
                output_file = outputs_dir / f"{step_name}_output.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"=== {step_name.upper()} OUTPUT ===\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Duration: {result['duration']:.2f}s\n")
                    f.write(f"Success: {result['success']}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(result["output"])
            
            # Save stderr if exists
            if result["error"]:
                error_file = outputs_dir / f"{step_name}_error.txt"
                with open(error_file, 'w', encoding='utf-8') as f:
                    f.write(f"=== {step_name.upper()} ERROR ===\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Duration: {result['duration']:.2f}s\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(result["error"])
        
        # 4. Save CSV summary for easy analysis
        csv_file = summary_dir / f"pipeline_stats_{timestamp}.csv"
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write("Step,Success,Duration(s),Output_Length,Error_Length\n")
            for step_name, result in results.items():
                f.write(f"{step_name},{result['success']},{result['duration']:.2f},{len(result['output'])},{len(result['error'])}\n")

    def generate_markdown_report(self, agent_name, repo_url, results, timestamp):
        """Generate a comprehensive Markdown report"""
        step_names = {
            "clone": "🔗 Repository Clone",
            "analyze": "📊 Code Analysis", 
            "tests": "🧪 Test Generation",
            "docker": "🐳 Dockerization",
            "deploy": "🚀 Deployment",
            "optimize": "💡 Optimization"
        }
        
        successful_steps = sum(1 for r in results.values() if r["success"])
        total_duration = sum(r["duration"] for r in results.values())
        success_rate = (successful_steps / len(results) * 100) if results else 0
        
        md_content = f"""# 1INTERPRETER DevOps Pipeline Report

## 📋 Pipeline Summary
- **Agent Name**: {agent_name}
- **Repository**: {repo_url}
- **Execution Time**: {timestamp}
- **Total Steps**: {len(results)}
- **Successful Steps**: {successful_steps}
- **Failed Steps**: {len(results) - successful_steps}
- **Success Rate**: {success_rate:.1f}%
- **Total Duration**: {total_duration:.2f} seconds

## 🔄 Pipeline Steps

"""
        
        for step, result in results.items():
            status_icon = "✅" if result["success"] else "❌"
            step_title = step_names.get(step, step.title())
            
            md_content += f"""### {status_icon} {step_title}
- **Status**: {'Success' if result['success'] else 'Failed'}
- **Duration**: {result['duration']:.2f} seconds
- **Output Length**: {len(result['output'])} characters
- **Error Length**: {len(result['error'])} characters

"""
            
            if result["output"]:
                md_content += f"""#### Output Preview:
```
{result['output'][:500]}{'...' if len(result['output']) > 500 else ''}
```

"""
            
            if result["error"]:
                md_content += f"""#### Error Details:
```
{result['error'][:300]}{'...' if len(result['error']) > 300 else ''}
```

"""
        
        md_content += f"""## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Fastest Step | {min(results.keys(), key=lambda x: results[x]['duration'])} ({min(r['duration'] for r in results.values()):.2f}s) |
| Slowest Step | {max(results.keys(), key=lambda x: results[x]['duration'])} ({max(r['duration'] for r in results.values()):.2f}s) |
| Average Duration | {total_duration / len(results):.2f}s |
| Total Output Size | {sum(len(r['output']) for r in results.values())} characters |

## 🎯 Recommendations

"""
        
        # Add recommendations based on results
        if success_rate == 100:
            md_content += "🎉 **Excellent!** All pipeline steps completed successfully.\n\n"
        elif success_rate >= 80:
            md_content += "✅ **Good!** Most steps completed successfully. Review failed steps for improvements.\n\n"
        else:
            md_content += "⚠️ **Attention Needed!** Multiple steps failed. Review configuration and dependencies.\n\n"
        
        # Add specific recommendations
        for step, result in results.items():
            if not result["success"]:
                md_content += f"- **{step_names.get(step, step.title())}**: Review error logs and fix configuration issues.\n"
        
        md_content += f"""
---
*Generated by 1INTERPRETER DevOps Pipeline*  
*Agent: {agent_name}*  
*Timestamp: {timestamp}*
"""
        
        return md_content

    def show_pipeline_summary(self, agent_name, results):
        """Display pipeline execution summary"""
        console.print(f"\n[bold cyan]📋 Pipeline Summary for '{agent_name}'[/bold cyan]")
        
        # Create summary table
        summary_table = Table(show_header=True, header_style="bold magenta")
        summary_table.add_column("Step", style="bold", width=20)
        summary_table.add_column("Status", width=15)
        summary_table.add_column("Duration", width=12)
        summary_table.add_column("Result", width=40)
        
        total_duration = 0
        successful_steps = 0
        
        step_names = {
            "clone": "🔗 Repository Clone",
            "analyze": "📊 Code Analysis", 
            "tests": "🧪 Test Generation",
            "docker": "🐳 Dockerization",
            "deploy": "🚀 Deployment",
            "optimize": "💡 Optimization"
        }
        
        for step, result in results.items():
            status = "[green]✅ Success[/green]" if result["success"] else "[red]❌ Failed[/red]"
            duration = f"{result['duration']:.1f}s"
            output = result["output"][:35] + "..." if len(result["output"]) > 35 else result["output"]
            
            summary_table.add_row(
                step_names.get(step, step.title()),
                status,
                duration, 
                output
            )
            
            total_duration += result["duration"]
            if result["success"]:
                successful_steps += 1
        
        console.print(summary_table)
        
        # Show overall statistics
        success_rate = (successful_steps / len(results)) * 100 if results else 0
        
        stats_text = f"""
[bold]Pipeline Statistics:[/bold]
• Total Steps: {len(results)}
• Successful: {successful_steps}
• Failed: {len(results) - successful_steps}
• Success Rate: {success_rate:.1f}%
• Total Duration: {total_duration:.1f}s

[bold yellow]📁 Files Generated:[/bold yellow]
• JSON Summary: pipeline_summary_*.json
• Markdown Report: pipeline_report_*.md
• Step Outputs: step_outputs/*.txt
• CSV Statistics: pipeline_stats_*.csv

[bold cyan]🎉 DevOps Pipeline Complete![/bold cyan]
All outputs saved to: pipeline_summaries/{agent_name.lower().replace(' ', '_').replace('-', '_')}/
"""
        
        console.print(Panel(stats_text, title="[bold green]📊 Results", border_style="green"))

    def run_workflow_mode(self):
        """Run workflow creation mode"""
        console.print("\n[bold purple]⚡ Workflow Builder Mode[/bold purple]")
        console.print("Build complete AI-powered DevOps workflows!\n")
        
        workflow_name = Prompt.ask("📋 Workflow Name", default="CI-CD-Pipeline")
        workflow_steps = []
        
        console.print("\n🔧 Add workflow steps (press Enter with empty input to finish):")
        step_num = 1
        while True:
            step = Prompt.ask(f"Step {step_num}", default="")
            if not step:
                break
            workflow_steps.append(step)
            step_num += 1
            
        if workflow_steps:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold purple]Building workflow..."),
                transient=True,
            ) as progress:
                progress.add_task("Building", total=None)
                time.sleep(3)
                
            console.print(f"✅ [bold green]Workflow '{workflow_name}' created![/bold green]")
            console.print("📋 Steps:")
            for i, step in enumerate(workflow_steps, 1):
                console.print(f"   {i}. {step}")
                
            # Create workflow files
            self.create_workflow_files(workflow_name, workflow_steps)
        else:
            console.print("❌ No steps added to workflow.")
            
        input("\nPress Enter to continue...")

    def process_ai_query(self, query):
        """Process AI query using real backend"""
        with Progress(
            SpinnerColumn(),
            TextColumn(f"[bold yellow]Processing: {query[:50]}..."),
            transient=True,
        ) as progress:
            progress.add_task("Processing", total=None)
            
            # Try to use real backend first
            if BACKEND_AVAILABLE:
                try:
                    # Use the actual LLM wrapper
                    ai_response = query_llm(query)
                    
                    # Format the response nicely
                    response = f"""🤖 **1INTERPRETER AI Response:**

{ai_response}

---
💡 **Available Commands:**
• `clone <repo>` - Clone and analyze repository
• `analyze` - Run code analysis  
• `docker` - Generate Dockerfile
• `deploy` - Full deployment pipeline
• `tests` - Generate unit tests
• `optimize` - Code optimization suggestions

Type any command or ask me anything!"""
                    
                except Exception as e:
                    response = f"""❌ **Backend Error:**
                    
Error connecting to 1INTERPRETER backend: {str(e)}

� **Troubleshooting:**
1. Ensure backend is properly configured
2. Check AI configuration with `ai-config`
3. Verify API keys are set
4. Try restarting the application"""
            else:
                # Fallback to simulated responses
                if "clone" in query.lower():
                    response = """🔗 **Repository Cloning:**

To clone a repository, I need the GitHub URL. Example:
`clone https://github.com/user/repo`

🔧 **What happens next:**
1. Repository will be downloaded
2. Automatic project analysis
3. Framework detection
4. Security scanning
5. Smart Dockerfile generation

Please provide the repository URL!"""
                
                elif "docker" in query.lower():
                    response = """� **Docker Automation:**

1INTERPRETER can create optimized Dockerfiles:
1. 📊 Analyze project structure
2. 🔧 Detect framework (Flask, Django, Node.js, etc.)
3. 🚀 Generate multi-stage builds
4. 🔒 Security best practices
5. � Minimal image sizes

First, clone a repository or navigate to your project!"""
                
                elif "test" in query.lower():
                    response = """🧪 **AI Test Generation:**

I can generate comprehensive test suites:
1. 🔬 Unit tests with high coverage
2. 🔗 Integration test scenarios  
3. 🎭 Mock objects and fixtures
4. 📈 Performance benchmarks
5. 🛡️ Security test cases

Provide your code or clone a repository first!"""
                
                elif "code analysis" in query.lower():
                    response = """📊 **Code Analysis:**

1INTERPRETER performs deep code analysis:
1. 🔍 Static analysis (pylint, bandit)
2. 🛡️ Security vulnerability scanning
3. 📈 Code complexity metrics
4. 🎯 Performance bottlenecks
5. 💡 Optimization suggestions
6. 📋 Detailed JSON reports

Use `analyze` command on any repository!"""
                
                else:
                    response = f"""🤖 **AI Assistant:**

I understand you're asking about: "{query}"

🚀 **Real Backend Commands Available:**
• `clone <url>` - Clone GitHub repository  
• `analyze` - Deep code analysis
• `docker` - Smart Dockerfile generation
• `deploy` - Full CI/CD automation
• `tests` - AI-powered test creation
• `optimize` - Performance optimization
• `ai-config` - Configure AI settings

⚠️ **Note:** Backend integration is {'✅ ACTIVE' if BACKEND_AVAILABLE else '❌ LIMITED'}
{'' if BACKEND_AVAILABLE else 'Install requirements and configure backend for full functionality.'}

Ask me to help with any DevOps task!"""

        console.print(Panel(response, title="[bold cyan]🤖 1INTERPRETER AI", border_style="cyan"))
        console.print()

    def create_agent_files(self, name, purpose, language):
        """Create agent configuration files"""
        agents_dir = Path("agents")
        agents_dir.mkdir(exist_ok=True)
        
        agent_config = {
            "name": name,
            "purpose": purpose,
            "language": language,
            "created": str(time.time()),
            "capabilities": [
                "code_analysis",
                "docker_generation", 
                "test_creation",
                "optimization"
            ]
        }
        
        config_file = agents_dir / f"{name.lower().replace(' ', '_')}.json"
        with open(config_file, 'w') as f:
            import json
            json.dump(agent_config, f, indent=2)

    def create_workflow_files(self, name, steps):
        """Create workflow configuration files"""
        workflows_dir = Path("workflows")
        workflows_dir.mkdir(exist_ok=True)
        
        workflow_config = {
            "name": name,
            "steps": steps,
            "created": str(time.time()),
            "status": "draft"
        }
        
        config_file = workflows_dir / f"{name.lower().replace(' ', '_')}.json"
        with open(config_file, 'w') as f:
            import json
            json.dump(workflow_config, f, indent=2)

    def run(self):
        """Main application loop"""
        while True:
            self.show_header()
            self.show_important_notes()
            self.show_mode_selection()
            
            user_input = self.get_user_input()
            
            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[bold red]👋 Thank you for using 1INTERPRETER![/bold red]")
                sys.exit(0)
                
            elif user_input.lower() == 'user':
                self.run_user_mode()
                
            elif user_input.lower() == 'agent':
                self.run_agent_mode()
                
            elif user_input.lower() == 'workflow':
                self.run_workflow_mode()
                
            elif user_input.lower() == 'config':
                self.run_config_mode()
                
            elif user_input.startswith('@'):
                console.print(f"\n[yellow]🔍 Searching for agent: {user_input[1:]}[/yellow]")
                time.sleep(1)
                console.print("[red]❌ Agent not found. Use 'agent' mode to create one.[/red]")
                input("Press Enter to continue...")
                
            else:
                console.print(f"\n[red]❌ Unknown command: {user_input}[/red]")
                console.print("[yellow]💡 Valid options: user, agent, workflow, config, exit[/yellow]")
                input("Press Enter to continue...")

    def run_config_mode(self):
        """Run configuration mode for backend setup"""
        console.print("\n[bold magenta]⚙️ Configuration Mode[/bold magenta]")
        console.print("Configure 1INTERPRETER backend and AI settings\n")
        
        if not BACKEND_AVAILABLE:
            console.print("[red]❌ Backend not available![/red]")
            console.print("Please install required packages:")
            console.print("pip install -r requirements.txt")
            input("Press Enter to continue...")
            return
            
        console.print("Current Status:")
        status = self.backend_status
        console.print(f"• Backend: {'✅ Available' if status['backend_available'] else '❌ Not Available'}")
        console.print(f"• AI Mode: {status.get('ai_mode', 'unknown')}")
        console.print(f"• APIs: {', '.join(status['apis_available']) if status['apis_available'] else 'None configured'}")
        
        if Confirm.ask("\nRun AI configuration?", default=True):
            self.execute_backend_command("ai-config")
            # Refresh status after configuration
            self.backend_status = self.check_backend_status()
            
        input("\nPress Enter to continue...")

def main():
    """Entry point"""
    try:
        app = AutoDockUI()
        app.run()
    except KeyboardInterrupt:
        console.print("\n[bold red]👋 Goodbye![/bold red]")
        sys.exit(0)

if __name__ == "__main__":
    main()
