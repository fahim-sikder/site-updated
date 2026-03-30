---
title: "Fair Decision Making"
date: 2026-02-17T12:34:34+01:00
# Summary for listing cards
summary: "Research on fair synthetic data generation and fair representation learning for bias-free decision making."

# Tags for filtering
tags:
  - Data Fairness
  - Synthetic Data Generation
  - Generative Models
  - ML for Healthcare
  - Algorithmic Fairness
  - Deep Learning

# Featured image
image:
  filename: featured.jpg
  caption: 
  focal_point: Smart

# Links displayed as buttons
# links:
#   - name: Demo
#     url: https://demo.example.com
#     icon: globe
#   - name: Code
#     url: https://github.com/user/project
#     icon: brands/github
#   - name: Paper
#     url: /publication/my-paper/
#     icon: document

# External link (clicking project card opens this URL)
external_link: ""

# Shorthand link fields
url_code: ""
url_pdf: ""
url_slides: ""
url_video: ""

# Pin to top of listings
featured: true

# Draft
draft: false
---

## Overview

The Fair Decision Making project addresses an important challenge in modern machine learning: generating high-quality synthetic data while ensuring fairness across different demographic groups. As machine learning models increasingly influence high-stakes decisions in healthcare, finance, and criminal justice, ensuring these systems make bias-free predictions has become paramount.

This research program develops novel deep generative model architectures and training methodologies that produce synthetic data exhibiting both high utility (quality, diversity, fidelity) and fairness properties as well as representation learning techniques that aids for fair decision making process. Our work primarily focuses on healthcare applications, where biased models can have serious real-world consequences for patient care and treatment decisions.

## Motivation

Training machine learning models on real-world data often leads to biased outcomes due to:

1. **Spurious correlations** between sensitive attributes (e.g., race, gender) and target variables
2. **Underrepresentation** of minority subgroups in training data
3. **Historical biases** embedded in data collection processes

Synthetic data generation offers a promising solution by allowing us to create de-identified, representative datasets that maintain utility while mitigating these fairness concerns. However, existing synthetic data generators often fail to adequately address fairness, leading to bias amplification in downstream tasks.

## Research Approach

Our research tackles fairness in synthetic data generation through multiple approaches:

### 1. Bias-Transforming Generative Models

We develop generative adversarial networks (GANs) with specific fairness constraints that learn to transform biased data distributions into fair ones. This includes:

- Information-constrained data generation processes based on well-defined notions of algorithmic fairness
- Score-based weighted sampling to preserve minority subgroup densities
- Techniques to break spurious correlations while maintaining data utility

### 2. Fair Latent Representations

We propose learning syntax-agnostic, model-agnostic fair latent representations that separate fairness optimization from data generation:

- Enables more stable training by decoupling fairness constraints from generator optimization
- Reduces computational demands by generating data in low-dimensional spaces
- Provides flexibility to use different generative model architectures (GANs, Diffusion Models, VAEs)

### 3. Intersectional Fairness

We address the challenge of intersectional bias, where multiple sensitive attributes interact to create compounded discrimination:

- Novel fairness metrics that capture intersectional disparities
- Generation techniques that ensure fairness across intersecting demographic groups
- Applications to temporal and sequential data domains

## Key Contributions

Our work has resulted in:

- **Novel architectures**: Bt-GAN, FLDGM, and Fair distillation frameworks that achieve state-of-the-art performance in fair synthetic data generation and fair representation learning
- **Empirical validation**: Extensive experiments on real-world healthcare datasets (MIMIC-III, IV) demonstrating improved fairness without sacrificing utility
- **Open-source tools**: Publicly available implementations enabling reproducible research and practical applications

## Impact and Applications

This research enables:

- **Fair healthcare AI**: Training clinical decision support systems that provide equitable care across patient demographics
- **Bias mitigation**: Identifying and correcting biases in existing datasets and models

## Technical Approach

Our methods employ:

- **Deep generative models**: GANs, Diffusion Models, Variational Autoencoders
- **Fairness metrics**: Demographic parity, equalized odds, individual fairness measures
- **Optimization techniques**: Adversarial training, score-based sampling, information constraints
- **Evaluation frameworks**: Comprehensive assessment of utility (quality, diversity, fidelity) and fairness trade-offs
