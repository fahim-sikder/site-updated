---
title: 1. Why synthetic data?
linkTitle: 1. Why synthetic data?
weight: 10
---

Real data is often hard to share. Patient records, financial transactions and location traces carry personal information, so access is restricted by law and by ethics boards.

Synthetic data offers one way around this restriction. A generative model learns the distribution of a real dataset and then samples new records from that distribution. No synthetic record corresponds to a real person, yet the dataset as a whole keeps the statistical structure of the original.

## Common use cases

- **Data sharing.** A hospital releases a synthetic version of its records so that external researchers can develop methods without access to the real data.
- **Augmentation.** We add synthetic samples of a rare class to reduce class imbalance before training a classifier.
- **Fairness.** We generate data in which a protected attribute is less correlated with the outcome, so that downstream models inherit less bias.
- **Testing.** Engineers test software pipelines on synthetic data before the real data is available.

## Limits

Synthetic data is not private by default. A model that overfits can memorise and reproduce real records. We return to this risk in [Lesson 3](../03-evaluation/).

> [!TIP]
> Keep a held-out set of real data that the generator never sees. You will need it to evaluate the generator.
