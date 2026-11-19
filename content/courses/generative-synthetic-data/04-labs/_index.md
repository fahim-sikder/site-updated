---
title: Labs
weight: 40
---

The four labs run in weeks 4 to 7, each after the lecture or seminar of that week. In the labs you train generative models and evaluate their output for utility, privacy and fairness. Each lab lasts 2 hours.

| Week | Lab | Learning outcomes | Main tools |
|:----:|---|---|---|
| 4 | [Lab 1: Train generative models and compare their output](lab-1/) | LO1 | CTGAN, TVAE, TimeGAN, TransFusion |
| 5 | [Lab 2: Utility evaluation](lab-2/) | LO2 | scikit-learn, synthcity metrics, FairX |
| 6 | [Lab 3: Privacy evaluation](lab-3/) | LO2, LO3 | DPGAN (synthcity), DOMIAS, distance to closest record |
| 7 | [Lab 4: Fairness evaluation](lab-4/) | LO2, LO3 | fairlearn, FairX, TabFairGAN |

## How the labs work

Every lab page has the same parts: the goal and learning outcomes, what to do before the lab, the set-up, numbered tasks, questions for your lab notes, a note on energy use, what completing the lab means, and further reading.

The labs come with starter code: one or two Python scripts that you download from the lab page and run from a terminal. You change their arguments, and in some tasks a line of their code, and then explain what changes in the output. You do not write models from scratch.

Lab 1 writes the data splits and the synthetic data that Labs 2, 3 and 4 read, so keep its output folder. We suggest one folder per lab, next to each other:

```text
labs/
  lab-1/   lab1_tabular.py, lab1_timeseries.py, TransFusion/, outputs/, outputs_ts/
  lab-2/   lab2_utility.py
  lab-3/   lab3_privacy.py
  lab-4/   lab4_fairness.py, lab4_tabfairgan.py
```

We ran every command on the lab pages on a desktop PC with an AMD Ryzen 5 5500 CPU (6 cores) and 32 GB RAM, under Windows 11, with CPU-only PyTorch. The run times on the lab pages come from that machine. On it, no single training run took more than 4 minutes, and no lab script more than 7 minutes. Your laptop may take longer.

The course leader publishes all lab material before each session, so you can prepare at your own pace.

## Set-up {#set-up}

You need a laptop that can run Docker, or a free cloud server. No GPU is needed.

{{% steps %}}

### Option A: the course container

The course leader provides a Docker container with the starter code, the Python packages and the data. Install [Docker Desktop](https://docs.docker.com/get-started/get-docker/) on Windows or macOS, or Docker Engine on Linux, and follow the course leader's instructions to download and start the container. Contact the course leader before Lab 1 if the set-up fails.

### Option B: the same environment without Docker

You can create the same Python environment yourself. Download the requirements file [requirements.txt](lab-1/requirements.txt) into an empty folder, open a terminal there and run the four commands below. We tested these steps with [uv](https://docs.astral.sh/uv/) 0.12.18 and Python 3.11.16 on Windows 11 in November 2026; they took 80 seconds with the packages already in uv's cache. We did not test them on macOS or Linux.

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv torch==2.2.2 torchvision==0.17.2 --index-url https://download.pytorch.org/whl/cpu
uv pip install --python .venv -r requirements.txt
uv pip install --python .venv --no-deps "fairx @ git+https://github.com/fahim-sikder/FairX.git@417c3d9f7d29776429950a0f45af8093100de175"
```

Then activate the environment, as uv suggests when it creates it: `.venv\Scripts\activate` on Windows, or `source .venv/bin/activate` on macOS and Linux. Check the installation with:

```bash
python -c "import ctgan, synthcity, fairx, fairlearn, codecarbon; print('ok')"
```

The first command installs the CPU-only build of PyTorch. FairX pins Linux GPU packages in its own requirements, so the last command installs FairX without them; `requirements.txt` already installs the packages that FairX imports. The complete list of package versions in our tested environment is in [requirements-lock.txt](lab-1/requirements-lock.txt).

{{% /steps %}}

> [!NOTE] Messages you can ignore
> When synthcity loads, it prints messages marked `CRITICAL` about the optional plugins `goggle` and `great`, and KeOps prints warnings about a missing C++ compiler. The labs use none of these parts, and the scripts ran correctly with these messages on our test machine.

**Data.** The labs use the Adult census data (Becker and Kohavi, 1996), which scikit-learn downloads from [OpenML](https://www.openml.org/d/1590) on first use, and sine sequences generated in code. The [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/2/adult) publishes Adult under the CC BY 4.0 licence. No lab uses personal data beyond this public data set.

## Tools

| Tool | What it does in the labs | Labs | Version tested | Licence |
|---|---|:---:|---|---|
| [CTGAN](https://github.com/sdv-dev/CTGAN) (`ctgan`) | CTGAN and TVAE for tabular data | 1 | 0.13.0 | Business Source License 1.1 |
| [synthcity](https://github.com/vanderschaarlab/synthcity) | TimeGAN, DPGAN, alpha-precision, beta-recall, authenticity and DOMIAS | 1, 2, 3 | 0.2.12 | Apache 2.0 |
| [TransFusion](https://github.com/fahim-sikder/TransFusion) | Diffusion model with a transformer for time series | 1 | commit `7be6389` | Apache 2.0 |
| [FairX](https://github.com/fahim-sikder/FairX) | Utility, fidelity and fairness metrics; TabFairGAN | 2, 4 | commit `417c3d9` | MIT |
| [fairlearn](https://fairlearn.org) | Demographic parity, equalised odds, metrics per group | 4 | 0.15.0 | MIT |
| [scikit-learn](https://scikit-learn.org) | Classifiers, encoders, PCA and t-SNE | All | 1.6.1 | BSD 3-Clause |
| [CodeCarbon](https://github.com/mlco2/codecarbon) | Logging the energy use of each run | All | 3.3.2 | MIT |

The sample-level metrics of Alaa et al. (2022), that is alpha-precision, beta-recall and authenticity, come from two implementations: synthcity's `alpha_precision` metric and FairX's `SyntheticEvaluation`, which FairX adapted from synthcity. Lab 2 compares them.

## Energy use {#energy-use}

> [!TIP] Log your energy use
> Log the energy use of every training run with CodeCarbon, in the labs and in your project.

Every lab script wraps its training or evaluation in a CodeCarbon tracker and appends a row to `emissions.csv` in its output folder:

```python
import os

from codecarbon import OfflineEmissionsTracker

os.makedirs("outputs", exist_ok=True)  # the tracker needs an existing output folder
tracker = OfflineEmissionsTracker(country_iso_code="SWE", project_name="lab1-CTGAN", output_dir="outputs")
tracker.start()
# ... training ...
tracker.stop()
print(tracker.final_emissions_data.energy_consumed)  # kWh
```

> [!WARNING] Create the output folder first
> When the output folder did not exist, the tracker failed while starting, logged only a warning, and `final_emissions_data` did not exist after `stop()`. The lab scripts create their output folders before they start a tracker.

The offline tracker takes the country from its arguments, so it does not look up your location online. It converts energy to emissions with the average carbon intensity of the country you give: for Sweden, the data shipped with CodeCarbon 3.3.2 give 40.7 g CO<sub>2</sub>eq per kWh (2023 figures). How CodeCarbon gets the energy depends on the hardware and the operating system. It reads hardware energy counters where it can, and otherwise estimates CPU power from the processor's rated power and its load. It estimates RAM power from the number of memory modules. The [CodeCarbon methodology page](https://docs.codecarbon.io/latest/explanation/methodology/) explains the details. On our test machine, CodeCarbon read the CPU energy from the Windows Energy Meter Interface, estimated the RAM power at 20 W, and also measured the graphics card, which the labs do not use. By default the tracker measures the whole machine, not only your Python process. Treat the numbers as estimates and report how you obtained them.
