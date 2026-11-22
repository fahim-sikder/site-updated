---
title: Labs
weight: 40
# This page stays visible; the build block keeps the cascade below from hiding it too.
build:
  render: always
  list: always
# The lab pages below this section, and their starter code, are hidden for now:
# they are not built, listed or published. To publish them again, delete this
# cascade block and restore the full version of this page from git history.
cascade:
  build:
    render: never
    list: never
    publishResources: false
---

Each of the three labs follows a lecture or seminar, as the [schedule](../02-schedule/) shows. In the labs you train generative models and evaluate their output for utility, privacy and fairness. Each lab lasts 2 hours.

| Lab | Learning outcomes | Main tools |
|---|---|---|
| Lab 1: Train generative models and find failure modes | ILO1 | CTGAN, TVAE, TimeGAN, TransFusion |
| Lab 2: Utility and privacy evaluation of synthetic data | ILO2, ILO3 | scikit-learn, synthcity metrics, DPGAN (synthcity), DOMIAS, distance to closest record |
| Lab 3: Fairness evaluation of synthetic data | ILO2, ILO3 | fairlearn, FairX |

## How the labs work

The labs come with starter code: Python scripts that you run from a terminal. You change their arguments, and in some tasks a line of their code, and then explain what changes in the output. You do not write models from scratch.

The labs use the public Adult census data (Becker and Kohavi, 1996) and sine sequences generated in code. No lab uses personal data beyond this public data set.

The examiner publishes all lab material before each session, so you can prepare at your own pace.

## Set-up {#set-up}

You need a laptop that can run Docker, or a free cloud server. No GPU is needed. Install [Docker Desktop](https://docs.docker.com/get-started/get-docker/) on Windows or macOS, or Docker Engine on Linux. The examiner provides a Docker container with the starter code, the Python packages and the data, and explains how to download and start it before Lab 1.
