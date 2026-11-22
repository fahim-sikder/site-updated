---
title: Individual project
weight: 60
---

In the individual project you develop a generative model, train it on data from your own domain and evaluate the synthetic data for privacy, utility and fairness (if applicable). You present the project in the final session and submit a written reflection report four weeks later.

> [!IMPORTANT] Sensitive data
> Follow your own ethical approvals and data agreements. Do not share real sensitive data within the course. If you cannot bring your real data, use a public dataset with a similar structure, and explain in the report how it differs from your real data.

## What the project must contain {#what-the-project-must-contain}

1. **A domain problem:** State the problem in your research field that synthetic data could address, who would use the synthetic data, and for what.
2. **Data:** Describe the dataset: size, variable types, any temporal structure, and the attributes that are sensitive or protected. Agree on the choice of data with the examiner early in the course. Hold out a part of the real data that the generator never sees, you need it for evaluation.
3. **A generative model:** Design a new model or take one from the literature, and justify the choice from its training objective and what that objective implies for your data. You can start from the lab code if it fits your data.
4. **Evaluation of synthetic data:** Evaluate from the perspective of utility, privacy and fairness (if applicable).
5. **Energy use:** Log the energy use of your training runs with CodeCarbon and report it.

## Presentation {#presentation}

All participants present their projects in the final session and receive feedback.
## Reflection report {#reflection-report}

The written reflection report is due four weeks after the final presentations. It documents the findings of your project and reflects on how your assumptions and practice around synthetic data have changed during the course.

Structure the report in two parts.

### Part 1: Project report

Report each element listed under [What the project must contain](#what-the-project-must-contain).

### Part 2: Reflection

Cover at least these points:

- What you assumed about synthetic data at the start of the course, for example that it is anonymous by construction, or that a good fidelity score implies a useful dataset.
- What you will do differently in your own research practice, for example in how you evaluate, document or release synthetic data.

> [!TIP]
> Write down your assumptions about synthetic data before the first lecture. Comparing them with your view at the end of the course is the core of Part 2.
