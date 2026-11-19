---
title: 3. Evaluating synthetic data
linkTitle: 3. Evaluating synthetic data
weight: 30
---

We judge synthetic data on three axes. A good generator balances all three; a gain on one axis often costs something on another.

| Axis | Question | Example measure |
|------|----------|-----------------|
| Fidelity | Does the synthetic data look like the real data? | Distance between marginal distributions |
| Utility | Is the synthetic data useful for a downstream task? | Train on synthetic, test on real (TSTR) |
| Privacy | Does the synthetic data leak real records? | Distance to closest real record |

## Train on synthetic, test on real

The TSTR protocol trains a model on synthetic data and tests it on held-out real data. We compare its score with a model trained on real data. A small gap means the synthetic data preserves the patterns that matter for the task.

## Privacy checks

For each synthetic record, we find the distance to the closest record in the real training set. If many synthetic records sit closer to real ones than real records sit to each other, the generator has probably memorised its training data.

> [!WARNING]
> A high fidelity score combined with near-zero distances to real records is a sign of memorisation, not of a good generator.
