---
title: 2.2 Diffusion models
linkTitle: 2.2 Diffusion models
weight: 22
---

A diffusion model learns to reverse a process that gradually adds noise to data.

## Forward process

We start from a real sample $x_0$ and add Gaussian noise over $T$ steps. With a noise schedule $\beta_1, \dots, \beta_T$, each step is

$$
q(x_t \mid x_{t-1}) = \mathcal{N}\big(x_t;\, \sqrt{1 - \beta_t}\, x_{t-1},\, \beta_t I\big).
$$

After enough steps, $x_T$ is close to pure noise.

## Reverse process

A neural network learns to predict the noise added at each step. To generate a new sample, we start from random noise and apply the learnt denoising step $T$ times.

## Why use diffusion for time series?

Diffusion models avoid the adversarial game of GANs, so training is more stable. They can also condition on observed values, which suits time-series tasks such as imputation and forecasting. The cost is slower sampling, since generation needs many denoising steps.
