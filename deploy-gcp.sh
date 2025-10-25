#!/bin/bash

# GCP Deployment Script for TableTap with Docker Swarm
# This script automates the deployment of TableTap to Google Cloud Platform

set -e

# Configuration
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
ZONE="us-central1-a"
INSTANCE_NAME="tabletap-swarm-manager"
MACHINE_TYPE="e2-medium"
IMAGE_FAMILY="ubuntu-2004-lts"
IMAGE_PROJECT="ubuntu-os-cloud"

echo "========================================="
echo "TableTap GCP Deployment Script"
echo "========================================="

# Step 1: Create VM instance
echo "Step 1: Creating VM instance..."
gcloud compute instances create $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --image-family=$IMAGE_FAMILY \
    --image-project=$IMAGE_PROJECT \
    --boot-disk-size=20GB \
    --tags=http-server,https-server \
    --metadata=startup-script='#!/bin/bash
    # Install Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    usermod -aG docker $USER

    # Enable Docker service
    systemctl enable docker
    systemctl start docker
    '

# Step 2: Create firewall rules
echo "Step 2: Creating firewall rules..."
gcloud compute firewall-rules create allow-http \
    --project=$PROJECT_ID \
    --allow=tcp:80 \
    --target-tags=http-server \
    --description="Allow HTTP traffic" || true

gcloud compute firewall-rules create allow-https \
    --project=$PROJECT_ID \
    --allow=tcp:443 \
    --target-tags=https-server \
    --description="Allow HTTPS traffic" || true

# Step 3: Wait for instance to be ready
echo "Step 3: Waiting for instance to be ready..."
sleep 30

# Step 4: Get instance IP
INSTANCE_IP=$(gcloud compute instances describe $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "Instance IP: $INSTANCE_IP"

echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo "VM Instance: $INSTANCE_NAME"
echo "External IP: $INSTANCE_IP"
echo ""
echo "Next steps:"
echo "1. SSH into the instance: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo "2. Clone your repository or upload your code"
echo "3. Initialize Docker Swarm: docker swarm init"
echo "4. Build the image: docker build -t tabletap_web:latest ."
echo "5. Deploy the stack: docker stack deploy -c docker-stack.yml tabletap"
echo "========================================="
