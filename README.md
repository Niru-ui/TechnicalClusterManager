# TechnicalClusterManager-
Full-stack Django web application to manage and monitor Traveling Salesman Problem (TSP) computations on the Pitzer HPC cluster, with AWS deployment and Slurm integration.

What it does:
1. Submits TSP jobs from a web UI
2. Executes jobs on the Pitzer HPC cluster using Slurm
3. Retrieves and displays best route distance results
4. Runs on an AWS-hosted Django backend

Tech Stack:
1. Django (Python)
2. AWS EC2
3. Slurm (HPC scheduling)
4. SSH / SCP
5. SQLite
6. Git & GitHub

Architecture:
User → Django Web App (AWS) → Pitzer HPC Cluster → Results → Web UI

Setup Instructions:
1. Clone the repository
git clone https://github.com/Niru-ui/TechnicalClusterManager.git
 cd TechnicalClusterManager

2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install django

4. Run Django server
python manage.py runserver 0.0.0.0:8000
