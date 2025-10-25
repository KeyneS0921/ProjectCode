# TableTap - Cloud-Native Restaurant Ordering System

[![Django](https://img.shields.io/badge/Django-5.2.1-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)

A scalable, cloud-based restaurant table ordering system built with Django and deployed using Docker Swarm on Google Cloud Platform.

## Project Overview

TableTap is an INFS3208 Cloud Computing individual project implementing a **Type I - Highly Scalable and Available Web Application**. The system enables:

- **QR Code-Based Ordering**: Customers scan table QR codes to access menus
- **Real-Time Order Management**: Restaurant staff track orders through a live dashboard
- **Cloud-Native Architecture**: Containerized microservices with Docker Swarm orchestration
- **High Availability**: Multiple replicas with load balancing and rolling updates

## Features

### Customer Features
- Scan QR code at table to access menu
- Browse categorized menu items
- Add/remove items from cart
- Submit orders without login
- View order confirmation

### Merchant Features
- Dashboard with real-time order monitoring
- Table management and QR code generation
- Menu management (categories and items)
- Order status tracking (Pending → In Progress → Completed)
- Multi-table support

## Quick Start

### Local Development (Docker Compose)

```bash
# Clone repository
git clone <repository-url>
cd ProjectCode

# Start all services
docker-compose up --build

# Access application
open http://localhost
```

### Local Development (Traditional)

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Default Credentials

### Admin Login
- **Username:** `54657`
- **Password:** `s4857295`

### Restaurant User Login
- **Username:** `Restaurant`
- **Password:** `s4857295`

## Cloud Deployment

### Prerequisites
- Google Cloud Platform account with billing enabled
- `gcloud` CLI installed and configured
- Docker installed locally

### Deploy to GCP with Docker Swarm

```bash
# 1. Create GCP VM instance
gcloud compute instances create tabletap-swarm-manager \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud

# 2. SSH into instance
gcloud compute ssh tabletap-swarm-manager --zone=us-central1-a

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Initialize Docker Swarm
docker swarm init

# 5. Build and deploy
docker build -t tabletap_web:latest .
docker stack deploy -c docker-stack.yml tabletap
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Architecture

```
┌─────────────────────────────────────┐
│     Load Balancer (Nginx x2)       │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌─────▼───────┐
│  Django App │  │ Django App  │ (3 replicas)
└──────┬──────┘  └─────┬───────┘
       │                │
       └───────┬────────┘
               │
        ┌──────▼──────┐
        │ PostgreSQL  │
        └─────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend Framework | Django | 5.2.1 |
| Database | PostgreSQL | 15 |
| WSGI Server | Gunicorn | 21.2.0 |
| Load Balancer | Nginx | Alpine |
| Containerization | Docker | Latest |
| Orchestration | Docker Swarm | Latest |
| Cloud Platform | GCP Compute Engine | - |
| Frontend | Bootstrap | 5.3.3 |

## Project Structure

```
ProjectCode/
├── TableTap/              # Django project settings
├── orders/                # Main Django app
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── Dockerfile             # Container definition
├── docker-compose.yml     # Local development
├── docker-stack.yml       # Production deployment
├── nginx.conf             # Nginx configuration
├── entrypoint.sh          # Container startup script
├── DEPLOYMENT.md          # Deployment guide
├── ARCHITECTURE.md        # Architecture documentation
└── PROPOSAL.md            # Project proposal
```

## Demonstrating Type I Requirements

### ✅ Scalability
```bash
# Scale web application to 5 replicas
docker service scale tabletap_web=5
```

### ✅ Rolling Updates
```bash
# Update service with zero downtime
docker service update --image tabletap_web:v2 tabletap_web
```

### ✅ Rollback
```bash
# Rollback to previous version
docker service rollback tabletap_web
```

### ✅ Load Balancing
- Nginx load balancer with 2 replicas
- Docker Swarm routing mesh
- Round-robin distribution

### ✅ High Availability
- 3 application replicas
- 2 load balancer replicas
- Automatic failure recovery

## How to Use

1. **Admin** logs in to manage tables and view live pending orders
2. **Customers** scan QR codes at their table to open the restaurant menu
3. Customers browse the menu and add items to their cart
4. When ready, customers go to the cart and confirm their order
5. Orders show up instantly in the merchant dashboard
6. Admin can mark orders as completed in the dashboard

## Usage of AI

- **ChatGPT Free Vision**: Used to help debugging
- **Sora AI**: Used to generate the TableTap logo (`logo.png`)

## License

This project is for educational purposes as part of INFS3208 Cloud Computing course.

## Author

**Kunlong Liu** (s4857295)
School of Electrical Engineering and Computer Science
The University of Queensland

## Acknowledgments

- INFS3208 teaching team
- Django documentation
- Docker documentation
- Google Cloud Platform documentation