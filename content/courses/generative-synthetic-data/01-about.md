---
title: About the course
weight: 10
---

## Why this course

Synthetic data can ease data scarcity when real data is restricted, but it can still leak sensitive information, amplify bias in the real data or lose the utility of the real data in downstream tasks. The main goal of the course is to prepare participants to use the main families of generative models to generate synthetic data, and to evaluate it for privacy, fairness and utility.

## Intended learning outcomes {#learning-outcomes}

After the course, participants should be able to:

1. **ILO1:** Analyse how the training objectives of the main families of generative models relate to their failure modes.
2. **ILO2:** Evaluate synthetic data for utility, privacy and fairness.
3. **ILO3:** Assess whether a synthetic dataset can be released based on its measured privacy and fairness risks.
4. **ILO4:** Design and evaluate a generative model for a domain problem in their own research field.
5. **ILO5:** Reflect on how their own assumptions and practice around synthetic data have changed during the course.

## Who should take this course

The course is intended for PhD students in computer science who work with data that is challenging to access due to regulations or restrictions, or who want to understand how generative models work.

PhD students from other fields who work with sensitive data, for example in medicine or the social sciences, are also welcome.

> [!NOTE]
> Throughout the course, *fairness* refers to algorithmic fairness.

## Prerequisites

- Some background in machine learning or deep learning.
- Basic programming experience in Python, enough to run and modify the lab code.
- A personal laptop that can run Docker (instructions are on the [Labs](../04-labs/#set-up) page).

## How the course works

The course combines four kinds of activity.

- **[Lectures](../03-lectures/)** cover the main families of generative models and how to evaluate them for utility, privacy and fairness.
- **[Labs](../04-labs/)** let participants train generative models and evaluate their output.
- **[Paper seminars](../05-paper-seminars/)**: each participant chooses one paper on one of the two seminar topics and leads its discussion, with a short summary and questions for the group.
- **[Individual project](../06-project/)**: each participant trains a generative model on data from their own domain, evaluates the synthetic data and writes a reflection report. Participants who cannot bring their real data, because of ethical approvals or data agreements, use a public dataset with a similar structure.

## Topics

- Why synthetic data is needed: data access, scarcity and regulation
- Main generative models: variational autoencoders, generative adversarial networks, diffusion models and transformer-based models
- Generation and evaluation of synthetic data for fidelity and utility
- Privacy: differential privacy and privacy attacks
- Fairness: how synthetic data can carry or amplify bias
- Synthetic data release risk: measuring the privacy and fairness risks of releasing a synthetic dataset

The labs and the project log the energy use of training with [CodeCarbon](https://github.com/mlco2/codecarbon).
