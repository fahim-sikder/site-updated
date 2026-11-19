---
title: Individual project
weight: 60
---

In the individual project you develop a generative model, train it on data from your own domain and evaluate the synthetic data for privacy, utility and fairness. The model can be new or taken from the literature. You present the project in week 10 and submit a written reflection report two weeks later. The project covers learning outcomes [LO4 and LO5](../01-about/#learning-outcomes) and draws on LO1 to LO3.

> [!IMPORTANT] Sensitive data
> Follow your own ethical approvals and data agreements. Do not share real sensitive data within the course: not in slides, notebooks, figures or the report. If you cannot bring your real data, use a public dataset with a similar structure, and explain in the report how it differs from your real data.

## What the project must contain

1. **A domain problem.** State the problem in your research field that synthetic data could address, who would use the synthetic data, and for what. The [regulatory and data-access motivation from Lecture 1](../03-lectures/lecture-1/) is a good starting point.
2. **Data.** Describe the dataset: size, variable types, any temporal structure, and the attributes that are sensitive or protected. Hold out a part of the real data that the generator never sees; you need it for evaluation.
3. **A generative model.** Design a new model or take one from the literature, and justify the choice from its training objective and what that objective implies for your data ([Lectures 2](../03-lectures/lecture-2/) and [3](../03-lectures/lecture-3/), LO1).
4. **Evaluation on all three counts.**
   - *Utility and fidelity* with the methods of [Lecture 4](../03-lectures/lecture-4/) and [Lab 2](../04-labs/lab-2/).
   - *Privacy* with the methods of [Lecture 5](../03-lectures/lecture-5/) and [Lab 3](../04-labs/lab-3/): state your threat model, and say whether your model has a formal guarantee such as differential privacy or only empirical evidence.
   - *Fairness* with the methods of [Lecture 6](../03-lectures/lecture-6/) and [Lab 4](../04-labs/lab-4/): name the protected attributes and the fairness criteria you use, and why.
5. **A release decision.** Would you release this synthetic dataset, to whom, and under which conditions? Base the answer on your privacy and fairness results (LO3).
6. **Energy use.** Log the energy use of your training runs with CodeCarbon and report it.

## Steps

{{% steps %}}

### Choose your data and problem

Pick data from your own research field, or a public dataset with a similar structure. Agree on the choice with the course leader early in the course.

### Develop a generative model

Design a new model or take one from the literature. Start from the lab code if it fits your data.

### Train the model

Train the model on the training split of your data, and log the energy use of each training run with CodeCarbon.

### Evaluate the synthetic data

Evaluate the synthetic data for utility, privacy and fairness against the real holdout data.

### Present the project

Present your project in the final session in week 10.

### Write the reflection report

Submit the report two weeks after the final presentations.

{{% /steps %}}

## Presentation {#presentation}

All participants present their projects in the final session in week 10 and receive feedback from the group and the course leader. Cover the problem, the data, the model and why you chose it, the main results on utility, privacy and fairness, and your release decision. Keep to the time the course leader gives for each presentation, and leave time for questions.

## Reflection report {#reflection-report}

The written reflection report is due two weeks after the final presentations. It documents the findings of your project and reflects on how your assumptions and practice around synthetic data have changed during the course.

Structure the report in two parts.

**Part 1: Project report.**

- The problem and why synthetic data is a candidate solution.
- The data, including how you split it and why.
- The model and the reasons for choosing it.
- Results on utility and fidelity, privacy, and fairness, with the metrics, their values and a short interpretation of each.
- The release decision and its conditions.
- Energy use of training, as logged with CodeCarbon.
- Limitations: what your evaluation cannot tell you.

**Part 2: Reflection (LO5).**

- What you assumed about synthetic data at the start of the course, for example that it is anonymous by construction, or that a good fidelity score implies a useful dataset.
- Which lecture, lab, paper or result changed or confirmed each assumption, and how.
- What you will do differently in your own research practice, for example in how you evaluate, document or release synthetic data.

> [!TIP]
> Write down your assumptions about synthetic data in week 1, before the first lecture. Comparing them with your view at the end of the course is the core of Part 2.

## Pass criteria

The project and report pass when they show that you can:

- design or choose a generative model for a problem in your field and justify the choice from its training objective (LO1, LO4);
- evaluate the synthetic data for utility, privacy and fairness with appropriate methods, and interpret the results correctly (LO2, LO4);
- assess the privacy and fairness risks of releasing the synthetic data and reach a reasoned release decision (LO3);
- reflect on how your assumptions and practice around synthetic data have changed, with specific evidence from the course (LO5).

If the report does not yet meet a criterion, the course leader asks for a revision.
