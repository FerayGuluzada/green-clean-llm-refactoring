import pyRAPL
import subprocess
import time
import sys
import csv
from pathlib import Path
from datetime import datetime

# -----------------------
# CONFIG
# -----------------------
EXECUTIONS_PER_RUN = 30
WARMUP_RUNS = 5
COOLDOWN_SECONDS = 60
TIMEOUT_SECONDS = 10

# -----------------------
# INPUT
# Usage:
# python3 measure.py folder_or_file number_of_runs
# -----------------------
if len(sys.argv) < 3:
    print("Usage: python3 greenmetrics.py <file_or_folder> <runs>")
    sys.exit(1)

input_path = Path(sys.argv[1])
runs = int(sys.argv[2])

# -----------------------
# INIT pyRAPL
# -----------------------
pyRAPL.setup()

files = sorted(input_path.glob("*.py")) if input_path.is_dir() else [input_path]

output_file = "energy_metrics.csv"
avg_file = "avg_energy_metrics.csv"

print(f"\nFound {len(files)} script(s) in {input_path}\n")

# -----------------------
# SAFE SUBPROCESS RUNNER
# -----------------------
failed_executions = 0

def safe_run(command, file_name):
    global failed_executions

    try:
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=TIMEOUT_SECONDS,
            check=True
        )
        return True

    except subprocess.TimeoutExpired:
        print(f"⚠️ TIMEOUT: {file_name}")
        failed_executions += 1
        return False

    except subprocess.CalledProcessError:
        print(f"⚠️ ERROR: {file_name}")
        failed_executions += 1
        return False


# -----------------------
# MAIN CSV OUTPUT
# -----------------------
with open(output_file, "w", newline="") as raw_csv, \
     open(avg_file, "w", newline="") as avg_csv:

    raw_writer = csv.writer(raw_csv)
    avg_writer = csv.writer(avg_csv)

    # Raw per-run data
    raw_writer.writerow([
        "timestamp",
        "script",
        "run",
        "energy_uj",
        "runtime_seconds"
    ])

    # Avg per-script data
    avg_writer.writerow([
        "script",
        "avg_energy_uj",
        "avg_runtime_s",
        "runs_used"
    ])

    # -----------------------
    # LOOP FILES
    # -----------------------
    for file_idx, file_path in enumerate(files, 1):

        print("\n==============================")
        print(f"[{file_idx}/{len(files)}] Running: {file_path.name}")
        print("==============================\n")

        command = ["python3", "-u", str(file_path)]

        # ✅ reset per script
        energy_results = []
        runtime_results = []

        # -----------------------
        # WARM-UP
        # -----------------------
        print("Warm-up phase...")
        for _ in range(WARMUP_RUNS):
            safe_run(command, file_path.name)

        # -----------------------
        # MEASURED RUNS
        # -----------------------
        for run_num in range(1, runs + 1):

            print(f"Run {run_num}/{runs}")

            meter = pyRAPL.Measurement(f"{file_path.stem}_run_{run_num}")

            success = True

            start_time = time.perf_counter()
            meter.begin()

            for _ in range(EXECUTIONS_PER_RUN):
                ok = safe_run(command, file_path.name)
                if not ok:
                    success = False
                    break

            meter.end()
            end_time = time.perf_counter()

            # Discard failed runs
            if not success:
                print("  Discarded run due to timeout/error")
                time.sleep(COOLDOWN_SECONDS)
                continue

            runtime = end_time - start_time
            energy = sum(meter.result.pkg)

            timestamp = datetime.now().isoformat()

            # store raw
            raw_writer.writerow([
                timestamp,
                file_path.name,
                run_num,
                energy,
                runtime
            ])

            # store for averaging
            energy_results.append(energy)
            runtime_results.append(runtime)

            print(f"  Energy: {energy:.2f} µJ | Runtime: {runtime:.4f}s")

            time.sleep(COOLDOWN_SECONDS)

        # -----------------------
        # AVERAGE PER SCRIPT
        # -----------------------
        if energy_results and runtime_results:
            avg_writer.writerow([
                file_path.name,
                sum(energy_results) / len(energy_results),
                sum(runtime_results) / len(runtime_results),
                len(energy_results)
            ])


print(f"\nSaved raw results to '{output_file}'")
print(f"Saved averages to '{avg_file}'")
print(f"Total failed executions: {failed_executions}")
