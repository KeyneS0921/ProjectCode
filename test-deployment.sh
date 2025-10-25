#!/bin/bash

# TableTap Deployment Test Script
# This script tests the Docker Swarm deployment

set -e

echo "========================================="
echo "TableTap Deployment Test Script"
echo "========================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
echo -e "${YELLOW}Checking prerequisites...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is installed${NC}"

# Check if Docker Swarm is initialized
if ! docker info | grep -q "Swarm: active"; then
    echo -e "${YELLOW}⚠ Docker Swarm not initialized. Initializing now...${NC}"
    docker swarm init
    echo -e "${GREEN}✓ Docker Swarm initialized${NC}"
else
    echo -e "${GREEN}✓ Docker Swarm is active${NC}"
fi

# Build the Docker image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t tabletap_web:latest .
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Docker image built successfully${NC}"
else
    echo -e "${RED}❌ Failed to build Docker image${NC}"
    exit 1
fi

# Deploy the stack
echo -e "${YELLOW}Deploying stack...${NC}"
docker stack deploy -c docker-stack.yml tabletap
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Stack deployed successfully${NC}"
else
    echo -e "${RED}❌ Failed to deploy stack${NC}"
    exit 1
fi

# Wait for services to start
echo -e "${YELLOW}Waiting for services to start (30 seconds)...${NC}"
sleep 30

# Check service status
echo -e "${YELLOW}Checking service status...${NC}"
docker service ls

# Test scaling
echo -e "${YELLOW}Testing scaling feature...${NC}"
docker service scale tabletap_web=5
sleep 10
docker service ps tabletap_web
echo -e "${GREEN}✓ Scaling test completed${NC}"

# Scale back
docker service scale tabletap_web=3

# Get service endpoints
echo ""
echo "========================================="
echo -e "${GREEN}Deployment Test Complete!${NC}"
echo "========================================="
echo ""
echo "Services running:"
docker service ls
echo ""
echo "Access your application at:"
echo "  http://localhost"
echo ""
echo "To view logs:"
echo "  docker service logs tabletap_web"
echo "  docker service logs tabletap_nginx"
echo ""
echo "To remove the stack:"
echo "  docker stack rm tabletap"
echo ""
echo "========================================="
