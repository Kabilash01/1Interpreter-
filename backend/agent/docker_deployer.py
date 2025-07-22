"""
1INTERPRETER Docker Deployer
AI-powered Docker deployment file generation and optimization
"""
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from llm.llm_wrapper import get_llm

class DockerDeployer:
    """AI-powered Docker deployment automation"""
    
    def __init__(self):
        self.llm = get_llm()
        self.deployment_dir = Path("docker_deployments")
        self.deployment_dir.mkdir(exist_ok=True)
    
    def generate_deployment_files(self, project_path: str = ".") -> Dict[str, Any]:
        """Generate comprehensive Docker deployment files using AI"""
        
        start_time = time.time()
        project_path = Path(project_path)
        
        try:
            # Analyze project structure
            project_info = self._analyze_project_structure(project_path)
            
            # Generate AI-powered deployment configuration
            deployment_config = self._generate_ai_deployment_config(project_info)
            
            # Create deployment directory
            timestamp = int(time.time())
            deployment_name = f"deployment_{timestamp}"
            current_deployment_dir = self.deployment_dir / deployment_name
            current_deployment_dir.mkdir(exist_ok=True)
            
            # Generate deployment files
            files_created = []
            
            # 1. Generate intelligent Dockerfile
            dockerfile_content = self._generate_smart_dockerfile(project_info, deployment_config)
            dockerfile_path = current_deployment_dir / "Dockerfile"
            with open(dockerfile_path, 'w', encoding='utf-8') as f:
                f.write(dockerfile_content)
            files_created.append(str(dockerfile_path))
            
            # 2. Generate docker-compose.yml
            compose_content = self._generate_smart_compose(project_info, deployment_config)
            compose_path = current_deployment_dir / "docker-compose.yml"
            with open(compose_path, 'w', encoding='utf-8') as f:
                f.write(compose_content)
            files_created.append(str(compose_path))
            
            # 3. Generate .dockerignore
            dockerignore_content = self._generate_smart_dockerignore(project_info)
            dockerignore_path = current_deployment_dir / ".dockerignore"
            with open(dockerignore_path, 'w', encoding='utf-8') as f:
                f.write(dockerignore_content)
            files_created.append(str(dockerignore_path))
            
            # 4. Generate deployment scripts
            deploy_script = self._generate_deployment_script(project_info, deployment_name)
            deploy_path = current_deployment_dir / "deploy.sh"
            with open(deploy_path, 'w', encoding='utf-8') as f:
                f.write(deploy_script)
            files_created.append(str(deploy_path))
            
            # 5. Generate Kubernetes configuration
            k8s_content = self._generate_kubernetes_config(project_info, deployment_config)
            k8s_path = current_deployment_dir / "k8s-deployment.yaml"
            with open(k8s_path, 'w', encoding='utf-8') as f:
                f.write(k8s_content)
            files_created.append(str(k8s_path))
            
            # 6. Generate deployment documentation
            docs_content = self._generate_deployment_docs(project_info, deployment_config, files_created)
            docs_path = current_deployment_dir / "DEPLOYMENT_README.md"
            with open(docs_path, 'w', encoding='utf-8') as f:
                f.write(docs_content)
            files_created.append(str(docs_path))
            
            execution_time = time.time() - start_time
            
            summary = f"""🐳 AI-Powered Docker Deployment Generated:
📁 Location: {current_deployment_dir}
📄 Files: {len(files_created)} deployment files created
⏱️ Generation Time: {execution_time:.2f}s
🧠 AI Analysis: {deployment_config.get('ai_insights', 'Basic configuration')}"""
            
            return {
                "success": True,
                "summary": summary,
                "files": files_created,
                "deployment_dir": str(current_deployment_dir),
                "project_info": project_info,
                "ai_config": deployment_config,
                "execution_time": execution_time
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "summary": f"❌ Docker deployment generation failed: {str(e)}"
            }
    
    def _analyze_project_structure(self, project_path: Path) -> Dict[str, Any]:
        """Analyze project structure to understand requirements"""
        
        analysis = {
            "path": str(project_path),
            "language": "python",  # Default
            "framework": "unknown",
            "dependencies": [],
            "entry_points": [],
            "database_files": [],
            "config_files": [],
            "static_files": []
        }
        
        # Check for Python files
        python_files = list(project_path.rglob("*.py"))
        if python_files:
            analysis["language"] = "python"
            analysis["entry_points"] = [str(f) for f in python_files[:5]]
        
        # Check for Node.js files
        if (project_path / "package.json").exists():
            analysis["language"] = "node"
            analysis["framework"] = "node.js"
        
        # Check for requirements.txt or similar
        req_files = ["requirements.txt", "package.json", "Pipfile", "pyproject.toml"]
        for req_file in req_files:
            if (project_path / req_file).exists():
                analysis["dependencies"].append(req_file)
        
        # Check for framework indicators
        if any((project_path / f).exists() for f in ["app.py", "main.py", "manage.py"]):
            if (project_path / "manage.py").exists():
                analysis["framework"] = "django"
            else:
                analysis["framework"] = "flask"
        
        # Check for database files
        db_extensions = [".db", ".sqlite", ".sqlite3"]
        for ext in db_extensions:
            analysis["database_files"].extend([str(f) for f in project_path.rglob(f"*{ext}")])
        
        return analysis
    
    def _generate_ai_deployment_config(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered deployment configuration"""
        
        try:
            # Create detailed prompt for AI
            prompt = f"""
Analyze this project and generate optimal Docker deployment configuration:

Project Analysis:
- Language: {project_info['language']}
- Framework: {project_info['framework']}
- Dependencies: {project_info['dependencies']}
- Entry points: {project_info['entry_points'][:3]}

Generate deployment recommendations for:
1. Base Docker image selection
2. Port configuration
3. Environment variables
4. Volume mounts
5. Health check strategy
6. Security considerations
7. Performance optimizations

Provide specific, actionable configuration.
"""
            
            ai_result = self.llm.generate_response(prompt, json.dumps(project_info), "docker_generation")
            
            return {
                "ai_insights": ai_result["content"],
                "recommended_port": 8000 if project_info["language"] == "python" else 3000,
                "base_image": self._select_base_image(project_info),
                "security_features": ["non-root-user", "health-checks", "minimal-surface"],
                "performance_optimizations": ["multi-stage-build", "layer-caching", "small-image"]
            }
            
        except Exception as e:
            return {
                "ai_insights": f"AI analysis failed: {str(e)}. Using default configuration.",
                "recommended_port": 8000,
                "base_image": "python:3.11-slim",
                "security_features": ["basic"],
                "performance_optimizations": ["basic"]
            }
    
    def _select_base_image(self, project_info: Dict[str, Any]) -> str:
        """Select optimal base image based on project analysis"""
        
        if project_info["language"] == "python":
            if project_info["framework"] == "django":
                return "python:3.11-slim"
            elif project_info["framework"] == "flask":
                return "python:3.11-alpine"
            else:
                return "python:3.11-slim"
        elif project_info["language"] == "node":
            return "node:18-alpine"
        else:
            return "ubuntu:22.04"
    
    def _generate_smart_dockerfile(self, project_info: Dict[str, Any], 
                                  config: Dict[str, Any]) -> str:
        """Generate intelligent Dockerfile based on project analysis"""
        
        base_image = config["base_image"]
        port = config["recommended_port"]
        
        dockerfile_template = f"""# 1INTERPRETER Generated Dockerfile
# AI-optimized for {project_info['language']} {project_info['framework']} project
FROM {base_image}

# Set working directory
WORKDIR /app

# Install system dependencies (optimized for {project_info['language']})"""
        
        if project_info["language"] == "python":
            dockerfile_template += """
RUN apt-get update && apt-get install -y \\
    gcc \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \\
    pip install --no-cache-dir -r requirements.txt"""
        elif project_info["language"] == "node":
            dockerfile_template += """
# Copy package files first for better caching  
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force"""
        
        dockerfile_template += f"""

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE {port}

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:{port}/health || exit 1

# Run application"""
        
        if project_info["language"] == "python":
            if "app.py" in str(project_info["entry_points"]):
                dockerfile_template += '\nCMD ["python", "app.py"]'
            elif "main.py" in str(project_info["entry_points"]):
                dockerfile_template += '\nCMD ["python", "main.py"]'
            else:
                dockerfile_template += '\nCMD ["python", "-m", "app"]'
        elif project_info["language"] == "node":
            dockerfile_template += '\nCMD ["npm", "start"]'
        
        return dockerfile_template
    
    def _generate_smart_compose(self, project_info: Dict[str, Any], 
                               config: Dict[str, Any]) -> str:
        """Generate intelligent docker-compose.yml"""
        
        project_name = Path(project_info["path"]).name.lower().replace(" ", "_")
        port = config["recommended_port"]
        
        return f"""# 1INTERPRETER Generated Docker Compose
# AI-optimized for {project_info['language']} project
version: '3.8'

services:
  {project_name}:
    build: .
    ports:
      - "{port}:{port}"
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
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{port}/health"]
      interval: 30s
      timeout: 10s
      retries: 3

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
      POSTGRES_DB: {project_name}
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
    
    def _generate_smart_dockerignore(self, project_info: Dict[str, Any]) -> str:
        """Generate intelligent .dockerignore based on project type"""
        
        base_ignore = """# 1INTERPRETER Generated .dockerignore
.git
.gitignore
README.md
Dockerfile*
docker-compose*
.env
.venv
venv/
env/
.DS_Store
*.log"""
        
        if project_info["language"] == "python":
            base_ignore += """
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
.pytest_cache
.coverage
htmlcov/
.tox/
.cache
.mypy_cache"""
        
        elif project_info["language"] == "node":
            base_ignore += """
node_modules/
.npm
.next/
dist/
build/
coverage/"""
        
        base_ignore += """
docker_deployments/
pipeline_summaries/
agents/
workflows/
tests/
*.test
*.spec"""
        
        return base_ignore
    
    def _generate_deployment_script(self, project_info: Dict[str, Any], 
                                  deployment_name: str) -> str:
        """Generate deployment automation script"""
        
        project_name = Path(project_info["path"]).name.lower()
        
        return f"""#!/bin/bash
# 1INTERPRETER Generated Deployment Script
# AI-optimized deployment for {project_info['language']} project

set -e

echo "🐳 Deploying {project_name}..."

# Build the image
echo "📦 Building Docker image..."
docker build -t {project_name}:latest .

# Stop existing containers
echo "⏹️ Stopping existing containers..."
docker-compose down --remove-orphans

# Pull latest base images
echo "📥 Pulling latest base images..."
docker-compose pull

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Show status
echo "📊 Deployment status:"
docker-compose ps

# Health check
echo "🏥 Running health checks..."
sleep 5
if docker-compose exec -T {project_name.replace('-', '_')} curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "⚠️ Health check failed, checking logs..."
    docker-compose logs {project_name.replace('-', '_')}
fi

# Show logs
echo "📝 Recent logs:"
docker-compose logs --tail=20

echo "✅ Deployment complete!"
echo "🌐 Application available at: http://localhost:8000"
echo "🗄️ PostgreSQL available at: localhost:5432"
echo "🗄️ Redis available at: localhost:6379"
"""
    
    def _generate_kubernetes_config(self, project_info: Dict[str, Any], 
                                   config: Dict[str, Any]) -> str:
        """Generate Kubernetes deployment configuration"""
        
        project_name = Path(project_info["path"]).name.lower().replace("_", "-")
        port = config["recommended_port"]
        
        return f"""# 1INTERPRETER Generated Kubernetes Configuration
# AI-optimized for {project_info['language']} {project_info['framework']} project
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {project_name}-deployment
  labels:
    app: {project_name}
    version: v1
    generated-by: 1interpreter
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: {project_name}
  template:
    metadata:
      labels:
        app: {project_name}
        version: v1
    spec:
      containers:
      - name: {project_name}
        image: {project_name}:latest
        ports:
        - containerPort: {port}
          name: http
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
            port: {port}
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: {port}
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3

---
apiVersion: v1
kind: Service
metadata:
  name: {project_name}-service
  labels:
    app: {project_name}
spec:
  selector:
    app: {project_name}
  ports:
    - protocol: TCP
      port: 80
      targetPort: {port}
      name: http
  type: LoadBalancer

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {project_name}-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - {project_name}.yourdomain.com
    secretName: {project_name}-tls
  rules:
  - host: {project_name}.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {project_name}-service
            port:
              number: 80
"""
    
    def _generate_deployment_docs(self, project_info: Dict[str, Any], 
                                 config: Dict[str, Any], 
                                 files_created: List[str]) -> str:
        """Generate comprehensive deployment documentation"""
        
        project_name = Path(project_info["path"]).name
        
        return f"""# {project_name} - AI-Generated Deployment Guide

**Generated by 1INTERPRETER AI DevOps Pipeline** 🤖🚀

## 🔍 Project Analysis

- **Language**: {project_info['language']}
- **Framework**: {project_info['framework']}
- **Base Image**: {config['base_image']}
- **Port**: {config['recommended_port']}

## 🤖 AI Insights

{config.get('ai_insights', 'AI analysis not available')}

## 📁 Generated Files

{chr(10).join([f"- `{Path(f).name}`" for f in files_created])}

## 🚀 Quick Deploy

### Local Development
```bash
# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services  
docker-compose down
```

### Production Deployment
```bash
# Make executable
chmod +x deploy.sh

# Deploy
./deploy.sh
```

### Kubernetes
```bash
kubectl apply -f k8s-deployment.yaml
kubectl get pods -l app={project_name.lower()}
```

## 🔧 Configuration

### Environment Variables
- `ENV`: Environment (development/production)
- `DEBUG`: Debug mode (true/false)

### Ports
- Application: {config['recommended_port']}
- Database: 5432 (PostgreSQL)
- Cache: 6379 (Redis)

## 🛡️ Security Features

{chr(10).join([f"- {feature}" for feature in config.get('security_features', ['Basic security'])])}

## ⚡ Performance Optimizations  

{chr(10).join([f"- {opt}" for opt in config.get('performance_optimizations', ['Basic optimizations'])])}

## 📊 Monitoring

- Health endpoint: `/health`
- Readiness endpoint: `/ready`
- Metrics: Available via Docker stats

## 🆘 Troubleshooting

### Common Issues
- Check container logs: `docker-compose logs service-name`
- Verify ports: `docker-compose ps`
- Test connectivity: `docker exec -it container-name bash`

### Debug Commands
```bash
# Container status
docker ps -a

# Resource usage
docker stats

# Network inspection
docker network ls
docker network inspect deployment_app-network
```

---

**Generated by 1INTERPRETER** | {time.strftime('%Y-%m-%d %H:%M:%S')}  
**AI-Powered DevOps Automation** 🤖⚡
"""

if __name__ == "__main__":
    deployer = DockerDeployer()
    result = deployer.generate_deployment_files()
    
    if result["success"]:
        print(result["summary"])
    else:
        print(f"❌ Error: {result['error']}")
