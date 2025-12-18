import subprocess

OSC_USER = "w519nxa"   # <-- her W number
OSC_HOST = f"{OSC_USER}@pitzer.osc.edu"
SSH_KEY = "/home/ubuntu/.ssh/pitzer_key"   # path to her OSC private key


def _run(cmd):
    """Internal helper to execute shell commands."""
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         text=True)
    return p.communicate()


def remote(cmd):
    """Run a command remotely on Pitzer."""
    return _run(f"ssh -o StrictHostKeyChecking=no -i {SSH_KEY} {OSC_HOST} '{cmd}'")


def send(local_path, remote_path):
    """Copy a file TO Pitzer."""
    return _run(f"scp -o StrictHostKeyChecking=no -i {SSH_KEY} {local_path} {OSC_HOST}:{remote_path}")


def retrieve(remote_path, local_path):
    """Copy a file FROM Pitzer."""
    return _run(f"scp -o StrictHostKeyChecking=no -i {SSH_KEY} {OSC_HOST}:{remote_path} {local_path}")


def create_slurm(wt, seed, tries, batches):
    """Build the slurm batch script content."""
    seed = int(seed)
    seeds = " ".join(str(seed + i) for i in range(16))

    return f"""#!/bin/bash
#SBATCH --job-name=TSP_{wt}
#SBATCH --output=proj04_run/out.%j
#SBATCH --error=proj04_run/err.%j
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --account=PWSU0512

cd /users/PWSU0512/{OSC_USER}/proj04_run

cp ~nehrbajo/proj03data/distance0{wt}.pickle .
cp ~nehrbajo/proj03data/original0{wt}.pickle .

python3 ~nehrbajo/proj03data/tspMod.py {wt} initialGuess.pickle {seeds} {tries}
"""
