import subprocess
import re
import math
import csv
from pathlib import Path
from datetime import datetime

# =========================
# CONFIG
# =========================

INPUT_FOLDER = "results_all"
OUTPUT_FILE = "refactored_clean_metrics.csv"

SMELL_CODES = {
    "R0911", "R0912", "R0913", "R0914", "R0915",
    "R1702", "R1723", "R1720", "R1705", "R1710",
    "R1703",
    "C0103", "C0114", "C0115", "C0116"
}

# =========================
# FAILURE TRACKING
# =========================

RADON_FAILED = []
LIZARD_FAILED = []
PYLINT_FAILED = []

# =========================
# METRICS FUNCTIONS
# =========================

def get_loc(file):
    try:
        out = subprocess.check_output(
            ["radon", "raw", file],
            stderr=subprocess.STDOUT
        ).decode()

        m = re.search(r"SLOC:\s+(\d+)", out)
        return int(m.group(1)) if m else 0

    except Exception:
        print(f"⚠️ radon raw failed on {file}")
        RADON_FAILED.append(file)
        return 0


def get_halstead(file):
    try:
        out = subprocess.check_output(
            ["radon", "hal", file],
            stderr=subprocess.STDOUT
        ).decode()

        m = re.search(r"volume:\s+([\d\.]+)", out, re.IGNORECASE)
        return float(m.group(1)) if m else 0.0

    except Exception:
        print(f"⚠️ radon hal failed on {file}")
        if file not in RADON_FAILED:
            RADON_FAILED.append(file)
        return 0.0


def get_complexity(file):
    try:
        out = subprocess.check_output(
            ["lizard", file],
            stderr=subprocess.STDOUT
        ).decode()

        cc_values = []

        for line in out.splitlines():
            parts = line.strip().split()

            if len(parts) >= 6 and parts[0].isdigit():
                try:
                    cc_values.append(int(parts[1]))
                except Exception:
                    continue

        if not cc_values:
            return 0, 0, 0

        total = sum(cc_values)
        avg = total / len(cc_values)
        mx = max(cc_values)

        return total, avg, mx

    except Exception:
        print(f"⚠️ lizard failed on {file}")
        LIZARD_FAILED.append(file)
        return 0, 0, 0


def get_smells(file):
    try:
        out = subprocess.check_output(
            [
                "pylint",
                file,
                "--disable=all",
                "--enable=" + ",".join(SMELL_CODES)
            ],
            stderr=subprocess.STDOUT
        ).decode()

    except subprocess.CalledProcessError as e:
        out = e.output.decode()
        PYLINT_FAILED.append(file)

    except Exception:
        print(f"⚠️ pylint failed on {file}")
        PYLINT_FAILED.append(file)
        return 0

    warnings = re.findall(r":(\d+):(\d+):\s([CRWEF]\d+):", out)
    filtered = [w for w in warnings if w[2] in SMELL_CODES]

    return len(filtered)


def compute_mi(loc, hv, cc_total):
    if hv > 0 and loc > 0:
        raw = 171 - 5.2 * math.log(hv) - 0.23 * cc_total - 16.2 * math.log(loc)
        return max(0, raw * 100 / 171)
    return 0


# =========================
# MAIN BATCH RUN
# =========================

def run_all():
    files = list(Path(INPUT_FOLDER).glob("*.py"))
    rows = []

    run_timestamp = datetime.now().isoformat()

    print(f"Processing {len(files)} files...\n")

    for file in files:
        file = str(file)
        filename = Path(file).name

        print(f"Analyzing {file}")

        loc = get_loc(file)
        hv = get_halstead(file)
        cc_total, cc_avg, cc_max = get_complexity(file)
        mi = compute_mi(loc, hv, cc_total)
        smells = get_smells(file)

        rows.append([
            run_timestamp,
            filename,
            loc,
            cc_total,
            round(cc_avg, 2),
            cc_max,
            round(hv, 2),
            round(mi, 2),
            smells
        ])

    # =========================
    # WRITE CSV
    # =========================

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "timestamp",
            "script",
            "LOC",
            "CC_total",
            "CC_avg",
            "CC_max",
            "halstead_volume",
            "maintainability_index",
            "code_smells"
        ])

        writer.writerows(rows)

    # =========================
    # FAILURE SUMMARY
    # =========================

    print("\n=========================")
    print("PROBLEMATIC FILES")
    print("=========================")

    print(f"\nRadon failed ({len(set(RADON_FAILED))}):")
    for x in sorted(set(RADON_FAILED)):
        print(" -", x)

    print(f"\nLizard failed ({len(set(LIZARD_FAILED))}):")
    for x in sorted(set(LIZARD_FAILED)):
        print(" -", x)

    print(f"\nPylint issues/failures ({len(set(PYLINT_FAILED))}):")
    for x in sorted(set(PYLINT_FAILED)):
        print(" -", x)

    print(f"\nSaved to {OUTPUT_FILE}")


# =========================

if __name__ == "__main__":
    run_all()