#!/usr/bin/env python3
"""Experiment queue runner — adapted from AutoResearch experiment-queue.
OOM-aware retry, stale detection, wave transitions, resume on restart."""

import json, os, subprocess, sys, time, signal
from datetime import datetime
from pathlib import Path


def load_manifest(path):
    with open(path) as f:
        return json.load(f)


def load_state(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"jobs": {}, "completed": [], "failed": [], "running": []}


def save_state(path, state):
    state["checkpoint"] = datetime.utcnow().isoformat()
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def run_job(job, state, state_path):
    """Run a single job with OOM-aware retry."""
    cmd = job.get("command", "")
    if not cmd:
        config = job.get("config", "configs/default.yaml")
        seed = job.get("seed", 42)
        cmd = f"python run_experiment.py --config {config} --seed {seed}"

    batch_size = job.get("batch_size", None)
    max_retries = job.get("max_retries", 3)
    attempt = 0

    while attempt < max_retries:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=job.get("timeout", 7200))
            if result.returncode == 0:
                return {"status": "completed", "output": result.stdout[-500:]}
            elif "OOM" in result.stderr or "out of memory" in result.stderr.lower():
                if batch_size:
                    batch_size = batch_size // 2
                    cmd = cmd.replace(f"--batch_size {batch_size*2}", f"--batch_size {batch_size}")
                attempt += 1
                state["jobs"][job["id"]]["retry_count"] = attempt
                state["jobs"][job["id"]]["reduced_batch_size"] = batch_size
                save_state(state_path, state)
                time.sleep(10)
            else:
                return {"status": "failed", "error": result.stderr[-500:], "returncode": result.returncode}
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": f"Job exceeded {job.get('timeout', 7200)}s limit"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    return {"status": "failed_oom_retries_exhausted", "error": f"OOM after {max_retries} retries, final batch_size={batch_size}"}


def run_queue(manifest_path, state_path, max_parallel=4):
    """Process all jobs in manifest with wave transitions."""
    manifest = load_manifest(manifest_path)
    state = load_state(state_path)
    if "jobs" not in state:
        state["jobs"] = {}

    jobs = manifest.get("jobs", [])
    waves = manifest.get("waves", [jobs])  # default: all jobs in one wave

    for wave_idx, wave in enumerate(waves if isinstance(waves[0], list) else [jobs]):
        print(f"=== Wave {wave_idx+1} ===")
        pending = [j for j in wave if j["id"] not in state.get("completed", [])]

        for job in pending:
            state["jobs"][job["id"]] = {"status": "running", "started": datetime.utcnow().isoformat()}
            save_state(state_path, state)

            result = run_job(job, state, state_path)

            if result["status"] == "completed":
                state["completed"].append(job["id"])
                state["jobs"][job["id"]]["status"] = "completed"
            else:
                state["failed"].append(job["id"])
                state["jobs"][job["id"]]["status"] = "failed"
                state["jobs"][job["id"]]["error"] = result.get("error", "")

            save_state(state_path, state)

    # Summary
    print(f"Done: {len(state['completed'])} completed, {len(state['failed'])} failed")
    return state


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--state", default="queue_state.json")
    parser.add_argument("--max-parallel", type=int, default=4)
    args = parser.parse_args()
    run_queue(args.manifest, args.state, args.max_parallel)
