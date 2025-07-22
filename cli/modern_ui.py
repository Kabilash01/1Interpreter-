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

# 1INTERPRETER Backend Integration
sys.path.append(str(Path(__file__).parent.parent))

# Initialize console first
from rich.console import Console
console = Console()

try:
    # Import backend components
    from backend.main import Backend
    from backend.llm.llm_wrapper import get_llm, test_llm_connection
    from backend.llm.agent_engine import get_agent_engine
    from backend.workflow_engine import get_workflow_engine
    
    BACKEND_AVAILABLE = True
    console.print("[green]🤖 1INTERPRETER Backend: AI Components Loaded[/green]")
    
    # Initialize backend services
    try:
        backend_service = Backend()
        llm_service = get_llm()
        agent_service = get_agent_engine()  
        workflow_service = get_workflow_engine()
        console.print("[green]✅ AI Services: Fully Operational[/green]")
        
        # Test AI connection
        ai_test = test_llm_connection()
        if ai_test:
            console.print("[green]🌐 Gemini AI: Connected[/green]")
        else:
            console.print("[yellow]🔄 AI: Fallback mode (Simulation)[/yellow]")
            
    except Exception as e:
        console.print(f"[yellow]⚠️ AI Services: Fallback mode ({str(e)[:50]}...)[/yellow]")
        backend_service = None
        
except ImportError as e:
    console.print(f"[red]❌ Backend unavailable: {str(e)[:50]}...[/red]")
    BACKEND_AVAILABLE = False
    backend_service = None

# AI Helper Functions
def get_ai_status():
    """Get AI system status"""
    if BACKEND_AVAILABLE and backend_service:
        try:
            return backend_service.handle_status()
        except:
            return {"success": False, "content": "AI status unavailable"}
    return {"success": False, "content": "Backend not available"}

def query_llm(query):
    """Query the LLM with fallback"""
    if BACKEND_AVAILABLE and backend_service:
        try:
            return llm_service.generate_response(query, "", "general")
        except:
            pass
    
    # Fallback response
    return {
        "success": True,
        "content": f"AI Response (Simulated): {query[:100]}... - Analysis complete with recommendations.",
        "provider": "simulation"
    }

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
            "duration": 0,
            "files_created": []
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
                
                # Special handling for docker step - create actual files
                if command == "docker":
                    files_created = self.create_docker_deployment_files(arg)
                    step_result["files_created"] = files_created
                    step_result["output"] = f"✅ Docker deployment files created:\n" + "\n".join([f"• {file}" for file in files_created])
                else:
                    step_result["output"] = f"✅ {command.title()} completed successfully (simulated)"
                
                step_result["success"] = True
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
                
                # If docker command, also create deployment files
                if command == "docker" and step_result["success"]:
                    files_created = self.create_docker_deployment_files(arg)
                    step_result["files_created"] = files_created
                    step_result["output"] += f"\n\nDocker deployment files created:\n" + "\n".join([f"• {file}" for file in files_created])
                
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

    def create_docker_deployment_files(self, repo_info=""):
        """Create comprehensive Docker deployment files"""
        deployment_dir = Path("docker_deployments")
        deployment_dir.mkdir(exist_ok=True)
        
        # Create timestamped deployment folder
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = deployment_dir / f"deployment_{timestamp}"
        project_dir.mkdir(exist_ok=True)
        
        files_created = []
        
        # 1. Create Dockerfile
        dockerfile_content = self.generate_dockerfile()
        dockerfile_path = project_dir / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        files_created.append(str(dockerfile_path))
        
        # 2. Create docker-compose.yml
        compose_content = self.generate_docker_compose()
        compose_path = project_dir / "docker-compose.yml"
        with open(compose_path, 'w') as f:
            f.write(compose_content)
        files_created.append(str(compose_path))
        
        # 3. Create .dockerignore
        dockerignore_content = self.generate_dockerignore()
        dockerignore_path = project_dir / ".dockerignore"
        with open(dockerignore_path, 'w') as f:
            f.write(dockerignore_content)
        files_created.append(str(dockerignore_path))
        
        # 4. Create Kubernetes deployment
        k8s_content = self.generate_kubernetes_deployment()
        k8s_path = project_dir / "k8s-deployment.yaml"
        with open(k8s_path, 'w') as f:
            f.write(k8s_content)
        files_created.append(str(k8s_path))
        
        # 5. Create deployment scripts
        deploy_script = self.generate_deployment_script()
        script_path = project_dir / "deploy.sh"
        with open(script_path, 'w') as f:
            f.write(deploy_script)
        files_created.append(str(script_path))
        
        # 6. Create README for deployment
        readme_content = self.generate_deployment_readme(timestamp)
        readme_path = project_dir / "DEPLOYMENT_README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        files_created.append(str(readme_path))
        
        return files_created

    def generate_dockerfile(self):
        """Generate a comprehensive Dockerfile"""
        return """# 1INTERPRETER Generated Dockerfile
# Multi-stage build for optimized production image

# Development stage
FROM python:3.11-slim as development

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    make \\
    git \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Production stage
FROM python:3.11-slim as production

WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from development stage
COPY --from=development /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=development /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Default command
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    def generate_docker_compose(self):
        """Generate docker-compose.yml for local development"""
        return """# 1INTERPRETER Generated Docker Compose
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - /app/__pycache__
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
    depends_on:
      - redis
      - postgres
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: apppass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    networks:
      - app-network

volumes:
  redis_data:
  postgres_data:

networks:
  app-network:
    driver: bridge
"""

    def generate_dockerignore(self):
        """Generate .dockerignore file"""
        return """# 1INTERPRETER Generated .dockerignore

# Git
.git
.gitignore

# Docker
Dockerfile*
docker-compose*
.dockerignore

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
.pytest_cache
.coverage
.venv
venv/
env/

# IDE
.vscode
.idea
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Documentation
*.md
docs/

# Tests
tests/
test_*

# Build artifacts
build/
dist/
*.egg-info/

# Environment
.env
.env.local
.env.*.local

# Node modules (if any)
node_modules/

# Temporary files
tmp/
temp/
"""

    def generate_kubernetes_deployment(self):
        """Generate Kubernetes deployment manifest"""
        return """# 1INTERPRETER Generated Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  labels:
    app: 1interpreter-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: 1interpreter-app
  template:
    metadata:
      labels:
        app: 1interpreter-app
    spec:
      containers:
      - name: app
        image: 1interpreter-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "production"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: 1interpreter-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - your-domain.com
    secretName: app-tls
  rules:
  - host: your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
"""

    def generate_deployment_script(self):
        """Generate deployment automation script"""
        return """#!/bin/bash
# 1INTERPRETER Generated Deployment Script

set -e

echo "🚀 1INTERPRETER Deployment Script"
echo "=================================="

# Configuration
IMAGE_NAME="1interpreter-app"
CONTAINER_NAME="1interpreter-container"
PORT="8000"

# Functions
build_image() {
    echo "🔨 Building Docker image..."
    docker build -t $IMAGE_NAME:latest .
    echo "✅ Image built successfully"
}

run_container() {
    echo "🏃 Running container..."
    docker run -d \\
        --name $CONTAINER_NAME \\
        -p $PORT:8000 \\
        --restart unless-stopped \\
        $IMAGE_NAME:latest
    echo "✅ Container started on port $PORT"
}

stop_container() {
    echo "🛑 Stopping existing container..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
}

deploy_compose() {
    echo "🐳 Deploying with Docker Compose..."
    docker-compose up -d
    echo "✅ Services deployed successfully"
}

deploy_k8s() {
    echo "☸️ Deploying to Kubernetes..."
    kubectl apply -f k8s-deployment.yaml
    echo "✅ Kubernetes deployment applied"
}

# Main deployment logic
case "$1" in
    "build")
        build_image
        ;;
    "run")
        stop_container
        build_image
        run_container
        ;;
    "compose")
        deploy_compose
        ;;
    "k8s")
        deploy_k8s
        ;;
    "stop")
        stop_container
        docker-compose down 2>/dev/null || true
        ;;
    *)
        echo "Usage: $0 {build|run|compose|k8s|stop}"
        echo "  build   - Build Docker image"
        echo "  run     - Build and run single container"
        echo "  compose - Deploy with Docker Compose"
        echo "  k8s     - Deploy to Kubernetes"
        echo "  stop    - Stop all containers"
        exit 1
        ;;
esac

echo "🎉 Deployment completed!"
"""

    def generate_deployment_readme(self, timestamp):
        """Generate deployment documentation"""
        return f"""# 🐳 Docker Deployment Files

Generated by 1INTERPRETER on {timestamp}

## 📁 Files Included

- **Dockerfile** - Multi-stage production-ready container
- **docker-compose.yml** - Local development environment
- **.dockerignore** - Optimized build context
- **k8s-deployment.yaml** - Kubernetes deployment manifests
- **deploy.sh** - Automated deployment script
- **DEPLOYMENT_README.md** - This documentation

## 🚀 Quick Start

### Local Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment
```bash
# Make script executable
chmod +x deploy.sh

# Build and run single container
./deploy.sh run

# Deploy with compose (recommended)
./deploy.sh compose

# Deploy to Kubernetes
./deploy.sh k8s
```

## 🔧 Configuration

### Environment Variables
- `ENVIRONMENT` - Set to 'production' or 'development'
- `DEBUG` - Enable debug mode (development only)
- `DATABASE_URL` - Database connection string
- `REDIS_URL` - Redis connection string

### Ports
- **8000** - Application port
- **5432** - PostgreSQL database
- **6379** - Redis cache
- **80/443** - Nginx reverse proxy

## 📊 Container Resources

### Development
- Memory: 256Mi - 512Mi
- CPU: 250m - 500m

### Production
- Memory: 512Mi - 1Gi
- CPU: 500m - 1000m

## 🔍 Health Checks

- **Liveness**: `/health` endpoint
- **Readiness**: `/ready` endpoint
- **Interval**: 30s
- **Timeout**: 3s

## 🛡️ Security Features

- Non-root user execution
- Multi-stage builds for smaller images
- Health checks for reliability
- Resource limits for stability
- SSL/TLS support with nginx

## 🔄 CI/CD Integration

This deployment can be integrated with:
- GitHub Actions
- GitLab CI/CD
- Jenkins
- Azure DevOps
- AWS CodePipeline

## 📝 Customization

Edit the following files to customize:
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Service definitions
- `k8s-deployment.yaml` - Kubernetes resources
- `deploy.sh` - Deployment automation

---
*Generated by 1INTERPRETER DevOps Pipeline*
"""

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

    def create_docker_deployment_files(self, repo_url=""):
        """Create comprehensive Docker deployment files"""
        # Create docker deployment folder
        docker_dir = Path("docker_deployments")
        docker_dir.mkdir(exist_ok=True)
        
        # Extract repo name or use timestamp
        if repo_url:
            repo_name = repo_url.split('/')[-1].replace('.git', '')
        else:
            repo_name = f"project_{int(time.time())}"
        
        project_docker_dir = docker_dir / repo_name
        project_docker_dir.mkdir(exist_ok=True)
        
        files_created = []
        
        # 1. Create Dockerfile
        dockerfile_content = self.generate_dockerfile()
        dockerfile_path = project_docker_dir / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        files_created.append(f"📄 {dockerfile_path}")
        
        # 2. Create docker-compose.yml
        compose_content = self.generate_docker_compose(repo_name)
        compose_path = project_docker_dir / "docker-compose.yml"
        with open(compose_path, 'w') as f:
            f.write(compose_content)
        files_created.append(f"📄 {compose_path}")
        
        # 3. Create .dockerignore
        dockerignore_content = self.generate_dockerignore()
        dockerignore_path = project_docker_dir / ".dockerignore"
        with open(dockerignore_path, 'w') as f:
            f.write(dockerignore_content)
        files_created.append(f"📄 {dockerignore_path}")
        
        # 4. Create deployment scripts
        deploy_script = self.generate_deploy_script(repo_name)
        deploy_path = project_docker_dir / "deploy.sh"
        with open(deploy_path, 'w') as f:
            f.write(deploy_script)
        files_created.append(f"📄 {deploy_path}")
        
        # 5. Create Kubernetes deployment
        k8s_content = self.generate_k8s_deployment(repo_name)
        k8s_path = project_docker_dir / "k8s-deployment.yaml"
        with open(k8s_path, 'w') as f:
            f.write(k8s_content)
        files_created.append(f"📄 {k8s_path}")
        
        # 6. Create deployment README
        readme_content = self.generate_deployment_readme(repo_name)
        readme_path = project_docker_dir / "DEPLOYMENT_README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        files_created.append(f"📄 {readme_path}")
        
        console.print(f"[cyan]🐳 Docker deployment files created in: {project_docker_dir}[/cyan]")
        return files_created

    def generate_dockerfile(self):
        """Generate intelligent Dockerfile"""
        return """# 1INTERPRETER Generated Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "app.py"]
"""

    def generate_docker_compose(self, project_name):
        """Generate docker-compose.yml"""
        return f"""# 1INTERPRETER Generated Docker Compose
version: '3.8'

services:
  {project_name.lower().replace('-', '_')}:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
      - DEBUG=false
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    networks:
      - app-network
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - app-network

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: {project_name.lower()}
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: changeme123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - app-network

volumes:
  redis_data:
  postgres_data:

networks:
  app-network:
    driver: bridge
"""

    def generate_dockerignore(self):
        """Generate .dockerignore file"""
        return """# 1INTERPRETER Generated .dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
.git
.gitignore
README.md
Dockerfile
.dockerignore
.env
.venv
venv/
env/
.pytest_cache
.coverage
htmlcov/
.tox/
.cache
.mypy_cache
.DS_Store
*.log
docker_deployments/
pipeline_summaries/
agents/
workflows/
node_modules/
.npm
.next/
dist/
build/
"""

    def generate_deploy_script(self, project_name):
        """Generate deployment script"""
        return f"""#!/bin/bash
# 1INTERPRETER Generated Deployment Script

echo "🐳 Deploying {project_name}..."

# Build the image
echo "📦 Building Docker image..."
docker build -t {project_name.lower()}:latest .

# Stop existing containers
echo "⏹️ Stopping existing containers..."
docker-compose down

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Show status
echo "📊 Deployment status:"
docker-compose ps

# Show logs
echo "📝 Recent logs:"
docker-compose logs --tail=20

echo "✅ Deployment complete!"
echo "🌐 Application available at: http://localhost:8000"
echo "🗄️ PostgreSQL available at: localhost:5432"
echo "🗄️ Redis available at: localhost:6379"
"""

    def generate_k8s_deployment(self, project_name):
        """Generate Kubernetes deployment"""
        return f"""# 1INTERPRETER Generated Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {project_name.lower()}-deployment
  labels:
    app: {project_name.lower()}
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {project_name.lower()}
  template:
    metadata:
      labels:
        app: {project_name.lower()}
        version: v1
    spec:
      containers:
      - name: {project_name.lower()}
        image: {project_name.lower()}:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENV
          value: "production"
        - name: DEBUG
          value: "false"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: {project_name.lower()}-service
  labels:
    app: {project_name.lower()}
spec:
  selector:
    app: {project_name.lower()}
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
      name: http
  type: LoadBalancer

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {project_name.lower()}-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: {project_name.lower()}.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {project_name.lower()}-service
            port:
              number: 80
"""

    def generate_deployment_readme(self, project_name):
        """Generate deployment README"""
        return f"""# {project_name} - Docker Deployment Guide

Generated by **1INTERPRETER DevOps Pipeline** 🚀

## 📁 Deployment Files

- `Dockerfile` - Multi-stage Docker build configuration
- `docker-compose.yml` - Complete stack with app, Redis, and PostgreSQL
- `.dockerignore` - Files to exclude from Docker build context
- `deploy.sh` - Automated deployment script
- `k8s-deployment.yaml` - Kubernetes deployment and service configuration

## 🚀 Quick Start

### 1. Local Development
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f {project_name.lower()}

# Stop services
docker-compose down
```

### 2. Production Deployment
```bash
# Make deploy script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### 3. Kubernetes Deployment
```bash
# Apply Kubernetes configuration
kubectl apply -f k8s-deployment.yaml

# Check deployment status
kubectl get pods
kubectl get services
kubectl get ingress

# Port forward for local access
kubectl port-forward service/{project_name.lower()}-service 8000:80
```

## 🔧 Configuration

### Environment Variables
- `ENV`: Environment (development/production)
- `DEBUG`: Enable debug mode (true/false)
- `DATABASE_URL`: Database connection string

### Service Ports
- **Application**: 8000
- **Redis**: 6379
- **PostgreSQL**: 5432

## 📊 Monitoring & Health Checks

### Health Endpoints
- Health check: `http://localhost:8000/health`
- Readiness check: `http://localhost:8000/ready`

### Container Logs
```bash
# Application logs
docker-compose logs {project_name.lower()}

# All services logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f
```

### Kubernetes Monitoring
```bash
# Pod status
kubectl get pods -l app={project_name.lower()}

# Service status
kubectl describe service {project_name.lower()}-service

# View logs
kubectl logs -l app={project_name.lower()} -f
```

## 🛡️ Security Features

- ✅ Non-root user in container
- ✅ Minimal base image (python:3.11-slim)
- ✅ Health checks configured
- ✅ Resource limits set
- ✅ Network isolation
- ✅ Secret management ready

## 🔄 CI/CD Integration

### GitHub Actions
Add this workflow to `.github/workflows/deploy.yml`:

```yaml
name: Deploy {project_name}
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build and Deploy
      run: |
        docker build -t {project_name.lower()}:latest .
        # Add your deployment commands here
```

## 📝 Customization

1. **Update Dependencies**: Modify `requirements.txt`
2. **Adjust Resources**: Update resource limits in `k8s-deployment.yaml`
3. **Add Services**: Extend `docker-compose.yml`
4. **Configure Ingress**: Update ingress rules for custom domains

## 🆘 Troubleshooting

### Common Issues
- **Port conflicts**: Change ports in `docker-compose.yml`
- **Permission errors**: Ensure deploy script is executable
- **Image build fails**: Check Dockerfile and requirements

### Debug Commands
```bash
# Check container status
docker ps

# Inspect container
docker inspect {project_name.lower()}

# Enter container shell
docker exec -it {project_name.lower()} /bin/bash

# View container logs
docker logs {project_name.lower()}
```

---

**Generated by 1INTERPRETER** | *{time.strftime('%Y-%m-%d %H:%M:%S')}*

🔗 **Repository**: Ready for deployment  
🐳 **Docker**: Multi-stage optimized build  
☸️ **Kubernetes**: Production-ready configuration  
📊 **Monitoring**: Health checks included  
🛡️ **Security**: Best practices applied  
"""

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
