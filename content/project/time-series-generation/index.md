---
title: "Time Series Generation"
date: 2026-02-17T12:26:04+01:00

# Summary for listing cards
summary: "Advanced diffusion-based models for generating high-quality, long-sequence time series data."

# Tags for filtering
tags:
  - Time Series Generation
  - Diffusion Models
  - Transformers
  - Synthetic Data Generation
  - Deep Learning
  - Generative Models

# Featured image
image:
  filename: featured.jpg
  caption: "TransFusion architecture for long-sequence time series generation"
  focal_point: Smart

# Links displayed as buttons
links:
  - name: Code
    url: https://github.com/fahim-sikder/TransFusion
    icon: brands/github
  - name: Paper
    url: https://www.sciencedirect.com/science/article/pii/S2666827025000350
    icon: document

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

The Time Series Generation project develops state-of-the-art deep generative models for synthesizing high-quality, long-sequence time series data. Our recent contribution, **TransFusion**, combines the strengths of diffusion models and transformer architectures to overcome limitations in existing time series generation methods, enabling the creation of realistic synthetic temporal data at higher sequence lengths.

## The Challenge

Traditional generative models for time series face several limitations:

### 1. **Sequence Length Limitations**

- **RNN/LSTM-based GANs**: Struggle with sequences beyond 100 time steps due to vanishing/exploding gradients
- **CNN-based models**: Limited receptive fields make capturing long-range dependencies difficult
- **Standard GANs**: Training instability worsens with longer sequences

### 2. **Temporal Coherence**

- Maintaining realistic temporal correlations across long sequences
- Preserving both short-term fluctuations and long-term trends
- Capturing seasonal patterns and periodic behaviors

### 3. **Training Instability**

- Mode collapse in GANs becomes more severe with complex temporal patterns
- Difficulty balancing discriminator and generator learning
- Convergence issues with long-sequence modeling

### 4. **Scalability**

- Computational cost grows prohibitively with sequence length
- Memory constraints limit batch sizes and model capacity
- Slow generation speed hinders practical applications
