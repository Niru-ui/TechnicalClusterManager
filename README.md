# TechnicalClusterManager-
Full-stack Django web application to manage and monitor Traveling Salesman Problem (TSP) computations on the Pitzer HPC cluster, with AWS deployment and Slurm integration.

What it does:
Submits TSP jobs from a web UI
Executes jobs on the Pitzer HPC cluster using Slurm
Retrieves and displays best route distance results
Runs on an AWS-hosted Django backend

Tech Stack:
Django (Python)
AWS EC2
Slurm (HPC scheduling)
SSH / SCP
SQLite
Git & GitHub

Architecture:
User → Django Web App (AWS) → Pitzer HPC Cluster → Results → Web UI

Setup Instructions:
Clone the repository
git clone https://github.com/Niru-ui/TechnicalClusterManager.git
cd TechnicalClusterManager
Create virtual environment
python3 -m venv venv
source venv/bin/activate
Install dependencies
pip install django
Run Django server
python manage.py runserver 0.0.0.0:8000
