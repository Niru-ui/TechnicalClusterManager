from django.shortcuts import render
import os, tempfile, pickle

from .pitzer import remote, send, retrieve, create_slurm
from .guess import build_guess

JOB_FILE = "/home/ubuntu/proj04/jobid.txt"
BEST_FILE = "/home/ubuntu/proj04/latest_best_0.pickle"
SEED_FILE = "/home/ubuntu/proj04/seed_used.txt"


def load_best():
    """Read the best solution stored locally."""
    if not os.path.exists(BEST_FILE):
        return "NA"
    try:
        data = pickle.load(open(BEST_FILE, "rb"))
        return data.get("dist", "NA") if isinstance(data, dict) else data
    except:
        return "NA"


def job_running():
    """Check whether a job is active on Pitzer."""
    out, err = remote("squeue -u $USER")
    return "TSP_" in out


def index(request):
    wt = request.GET.get("wt", "00")
    seed = request.GET.get("seed", "0")
    tries = request.GET.get("tries", "1")
    batches = request.GET.get("bjobs", "1")

    best = load_best()
    status = ""

    if request.method != "POST":
        return render(request, "main.html", {
            "wt": wt, "seed": seed, "tries": tries,
            "bjobs": batches, "best": best,
            "status": status, "job_running": job_running()
        })

    # POST begins
    btn = request.POST.get("btn")
    wt = request.POST.get("wt")
    seed = request.POST.get("seed")
    tries = request.POST.get("tries")
    batches = request.POST.get("bjobs")

    # validate numbers
    try:
        int(seed); int(tries); int(batches)
    except:
        return render(request, "main.html", {
            "wt": wt, "seed": seed, "tries": tries,
            "bjobs": batches, "best": best,
            "status": "Inputs must be numeric.",
            "job_running": job_running()
        })

    # -------- UPDATE --------
    if btn == "update":
        out, err = remote("squeue -u $USER")
        status = out or err

        retrieve("proj04_run/best_0.pickle", BEST_FILE)
        best = load_best()

    # -------- START or STOP --------
    elif btn == "toggle":
        if job_running():
            # STOP existing job
            jid = open(JOB_FILE).read().strip() if os.path.exists(JOB_FILE) else ""
            if jid:
                remote(f"scancel {jid}")
                remote("touch proj04_run/STOP")
            open(JOB_FILE, "w").write("")
            status = "Stopped."
        else:
            # START new job
            guess_file = build_guess("")
            remote("mkdir -p proj04_run")
            send(guess_file, "proj04_run/initialGuess.pickle")

            slurm_content = create_slurm(wt, seed, tries, batches)

            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp.write(slurm_content.encode())
            tmp.close()

            send(tmp.name, "proj04_run/slurm.sbatch")
            os.unlink(tmp.name)

            out, err = remote("sbatch proj04_run/slurm.sbatch")
            status = out or err

            if "Submitted batch job" in out:
                jid = out.split()[-1]
                open(JOB_FILE, "w").write(jid)

            open(SEED_FILE, "w").write(seed)

    # -------- RESET --------
    elif btn == "reset":
        jid = open(JOB_FILE).read().strip() if os.path.exists(JOB_FILE) else ""
        if jid:
            remote(f"scancel {jid}")

        remote("rm -rf proj04_run")
        open(JOB_FILE, "w").write("")
        open(SEED_FILE, "w").write("")
        best = "NA"
        status = "Reset complete."

        wt, seed, tries, batches = "00", "0", "1", "1"

    return render(request, "main.html", {
        "wt": wt, "seed": seed, "tries": tries,
        "bjobs": batches, "best": best,
        "status": status, "job_running": job_running()
    })
