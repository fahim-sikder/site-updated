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

Each of the three labs follows a lecture or seminar, as the [schedule](../02-schedule/) shows. In the labs, participants train generative models and evaluate their output for utility, privacy and fairness. Each lab lasts 2 hours.

- Lab 1: Train generative models and find failure modes
- Lab 2: Utility and privacy evaluation of synthetic data
- Lab 3: Fairness evaluation of synthetic data

## How the labs work

The labs come with starter code as Jupyter notebooks, which participants open and run in JupyterLab. The notebooks show each step and its output, such as tables and plots, so participants can see what happens as a model trains and as its synthetic data is evaluated. Participants change settings and then explain what changes in the output. Participants modify working models rather than writing them from scratch.

The examiner publishes all lab material before each session, so participants can prepare at their own pace.

## Set-up {#set-up}

Each participant needs a laptop that can run Docker, or a free cloud server. No GPU is needed, but a GPU, if available, can speed up training. Install [Docker Desktop](https://docs.docker.com/get-started/get-docker/) on Windows or macOS, or Docker Engine on Linux. The examiner provides a Docker container with JupyterLab, the starter notebooks, the Python packages and the data, and explains how to download and start it before Lab 1. Once the container runs, participants open JupyterLab in their web browser.
