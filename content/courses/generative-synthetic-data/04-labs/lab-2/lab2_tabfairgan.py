"""Lab 2, optional extra: train TabFairGAN with FairX and save its synthetic data.

    python lab2_tabfairgan.py --epochs 15

FairX's TabFairGAN loads the full Adult data from OpenML with its own loader,
trains on a random 90% of it, prints FairX's alpha-precision, beta-recall and
authenticity, and writes the synthetic rows to a CSV file. This script runs
the documented FairX example inside a CodeCarbon tracker and moves the CSV to
--out, so that lab2_fairness.py can read it with --extra.
"""

import argparse
import shutil
import time
from pathlib import Path

from codecarbon import OfflineEmissionsTracker
from fairx.dataset import BaseDataClass
from fairx.models.inprocessing import TabFairGAN


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=15,
                        help="FairX trains the last 10 epochs for fairness, so use more than 10")
    parser.add_argument("--out", type=Path, default=Path("outputs_lab2_tabfairgan"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    data_module = BaseDataClass("Adult-Income", "sex", attach_target=True)
    tabfairgan = TabFairGAN("Female", ">50K")  # the underprivileged group and the desired label

    tracker = OfflineEmissionsTracker(
        country_iso_code="SWE", project_name="lab2-tabfairgan", output_dir=str(args.out), log_level="error"
    )
    tracker.start()
    start = time.perf_counter()
    tabfairgan.fit(data_module, batch_size=256, epochs=args.epochs)
    seconds = time.perf_counter() - start
    tracker.stop()
    print(f"TabFairGAN: {seconds:.0f} s, {tracker.final_emissions_data.energy_consumed * 1000:.2f} Wh")

    # FairX writes '<timestamp>-TabFairGAN-Adult-Income-sex.csv' to the working directory.
    newest = max(Path(".").glob("*-TabFairGAN-Adult-Income-sex.csv"), key=lambda p: p.stat().st_mtime)
    target = args.out / "synthetic_tabfairgan.csv"
    shutil.move(str(newest), target)
    print(f"synthetic data saved to {target}")


if __name__ == "__main__":
    main()
