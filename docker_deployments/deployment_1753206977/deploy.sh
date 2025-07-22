#!/bin/bash
# 1INTERPRETER Generated Deployment Script
# AI-optimized deployment for python project

set -e

echo "🐳 Deploying ..."

# Build the image
echo "📦 Building Docker image..."
docker build -t :latest .

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
if docker-compose exec -T  curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "⚠️ Health check failed, checking logs..."
    docker-compose logs 
fi

# Show logs
echo "📝 Recent logs:"
docker-compose logs --tail=20

echo "✅ Deployment complete!"
echo "🌐 Application available at: http://localhost:8000"
echo "🗄️ PostgreSQL available at: localhost:5432"
echo "🗄️ Redis available at: localhost:6379"
