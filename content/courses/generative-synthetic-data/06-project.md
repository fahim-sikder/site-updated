---
title: Individual project
weight: 60
---

In the individual project, each participant develops a generative model, trains it on data from their own domain and evaluates the synthetic data for privacy, utility and fairness (if applicable). Participants present their projects in the final session and submit a written reflection report four weeks later.

> [!IMPORTANT] Sensitive data
> Participants follow their own ethical approvals and data agreements and do not share real sensitive data within the course. Participants who cannot bring their real data use a public dataset with a similar structure, and explain in the report how it differs from the real data.

## What the project must contain {#what-the-project-must-contain}

1. **A domain problem:** State the problem in the participant's research field that synthetic data could address, who would use the synthetic data, and for what.
2. **Data:** Describe the dataset: size, variable types, any temporal structure, and the attributes that are sensitive or protected. Agree on the choice of data with the examiner early in the course. Hold out a part of the real data that the generator never sees; it is needed for evaluation.
3. **A generative model:** Design a new model or take one from the literature, and justify the choice from its training objective and what that objective implies for the data. The lab code can serve as a starting point if it fits the data.
4. **Evaluation of synthetic data:** Evaluate from the perspective of utility, privacy and fairness (if applicable).
5. **Energy use:** Log the energy use of the training runs with [CodeCarbon](https://github.com/mlco2/codecarbon) and report it.

## Presentation {#presentation}

All participants present their projects in the final session and receive feedback.
## Reflection report {#reflection-report}

The written reflection report is due four weeks after the final presentations. It documents the findings of the project and reflects on how the participant's assumptions and practice around synthetic data have changed during the course.

Structure the report in two parts.

### Part 1: Project report

Report each element listed under [What the project must contain](#what-the-project-must-contain).

### Part 2: Reflection

Cover at least these points:

- What the participant assumed about synthetic data at the start of the course, for example that it is anonymous by construction, or that a good fidelity score implies a useful dataset.
- What the participant will do differently in their own research practice, for example in how they evaluate, document or release synthetic data.

> [!TIP]
> Participants should write down their assumptions about synthetic data before the first lecture. This makes Part 2 easier to write.
