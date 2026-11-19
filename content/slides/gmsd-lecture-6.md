---
title: "Fairness in synthetic data"
kicker: "Lecture 6 · Week 7"
subtitle: "Generative Models for Synthetic Data: Privacy, Fairness and Utility"
presenter: "Md Fahim Sikder"
event: "PhD course · IDA, Linköping University"
course_url: /courses/generative-synthetic-data/03-lectures/lecture-6/
course_short: "Lecture page"
---

## Outline

1. Fairness definitions: group, individual, counterfactual
2. Impossibility results
3. Where bias enters a synthetic data pipeline
4. How generative models carry and amplify bias
5. Intersectionality
6. Fair generative models
7. Evaluating fairness, trade-offs and release risk

Note:
Fairness in this course always means algorithmic fairness: the statistical relationship between a sensitive attribute and the outcomes that data and models produce. The lecture serves LO2 (evaluate synthetic data for fairness) and LO3 (assess the fairness risk of releasing it). We build on Lecture 4 for fidelity and utility, and on Lecture 5 for differential privacy. Lab 4 later this week puts the evaluation part into practice with FairX.

---

## When is synthetic data fair?

- Most fairness definitions describe a predictor $\hat{Y}$, not a dataset
- Direct evidence: group label rates and subgroup shares in $\hat{D}$
- Indirect evidence: train on $\hat{D}$, test on held-out real data
- Distributional fairness: the optimal predictor trained on $\hat{D}$ is fair **on the real distribution** (van Breugel et al., 2021)

Note:
A synthetic dataset makes no decisions, so we need a bridge from definitions for predictors to properties of data. DECAF's definition makes the bridge explicit: given a fairness definition and an evaluation distribution, a distribution is fair if the optimal predictor trained on it satisfies the definition when evaluated on the evaluation distribution. The evaluation distribution matters. If you randomise the sensitive attribute, the data passes a fairness check on itself. A model trained on it can still discriminate on real data through features that correlate with the attribute.

---

## Notation

| Symbol | Meaning |
|---|---|
| $X$ | non-sensitive features |
| $A$ | sensitive attribute, groups $a, b$ |
| $Y$ | observed label |
| $R$, $\hat{Y}$ | score and binary prediction |
| $D$, $\hat{D}$ | real and synthetic data |

Note:
Many papers in this area write S for the sensitive attribute; Bt-GAN, FairGAN and TabFairGAN do. I use A, as Barocas, Hardt and Narayanan do in Fairness and Machine Learning. The attribute is binary unless I say otherwise.

---

## Independence: demographic parity

$$
P(\hat{Y}=1 \mid A=a) = P(\hat{Y}=1 \mid A=b)
$$

- Formally $\hat{Y} \perp A$; the only criterion that ignores $Y$
- Dataset version: compare $P(Y=1 \mid A=a)$ across groups
- Reported as a difference or as a ratio $\min_a / \max_a$ of selection rates

Note:
Barocas, Hardt and Narayanan group statistical criteria into independence, separation and sufficiency. Demographic parity is independence. Because it does not involve the label, it is the one criterion you can check on the synthetic data alone. FairGAN calls the dataset difference the risk difference; TabFairGAN calls it the discrimination score. Fairlearn, and therefore FairX, reports the demographic parity ratio: the smallest group selection rate divided by the largest.

---

## Separation: equalised odds and equal opportunity

$$
P(\hat{Y}=1 \mid A=a, Y=y) = P(\hat{Y}=1 \mid A=b, Y=y)
$$

- Equalised odds: holds for $y \in \{0,1\}$, that is equal TPR and FPR (Hardt et al., 2016)
- Equal opportunity: holds for $y=1$ only, that is equal TPR
- Terminology varies: Kearns et al. (2018) use "equal opportunity" for equal FPR

Note:
Equalised odds is the conditional independence of the prediction and the attribute given the label. It allows the prediction to depend on the attribute only through the label. Equal opportunity is the relaxation to the positive class. Always check which error rate a paper means.

---

## Sufficiency: calibration

$$
P(Y=1 \mid R=r, A=a) = r \quad \text{for all } r, a
$$

- Sufficiency: $Y \perp A \mid R$
- Calibration by group and sufficiency are essentially equivalent (Barocas et al., 2023)
- Separation and sufficiency condition on the observed $Y$: a biased label stays the reference

Note:
Calibration by group says that a score of 0.7 means a 70 percent positive rate in every group. The last bullet carries the key point for synthetic data. Separation and sufficiency take the recorded outcomes as ground truth. Kusner and colleagues make the point that enforcing equalised odds does not remedy a history in which people did not have equal opportunity. Wachter, Mittelstadt and Russell classify fairness metrics as bias-preserving or bias-transforming on the basis of how they handle pre-existing bias. Bt-GAN takes its name from that distinction.

---

## Individual fairness (Dwork et al., 2012)

$$
D\big(M(x), M(x')\big) \le d(x, x') \quad \text{for all } x, x'
$$

- $M$ maps an individual to a distribution over outcomes
- $d$ is a task-specific similarity metric that someone must supply
- Synthetic records are not people: the condition applies to models trained on $\hat{D}$

Note:
Similar individuals should be treated similarly. D is a distance between distributions; Dwork et al. use statistical distance. Whoever chooses d decides who counts as similar, and that is the hard part. Dwork et al. also show that the Lipschitz condition implies statistical parity between two groups if and only if the earthmover distance between the groups is small.

---

## Counterfactual fairness (Kusner et al., 2017)

$$
P\big(\hat{Y}_{A \leftarrow a}(U)=y \mid x, a\big) = P\big(\hat{Y}_{A \leftarrow a'}(U)=y \mid x, a\big)
$$

- Needs a causal model with background variables $U$
- The prediction must not change in the world where $A$ had been $a'$
- A predictor built only from non-descendants of $A$ satisfies it

Note:
Counterfactual fairness is an individual-level definition. Lemma 1 in Kusner et al. gives the third bullet. The causal model is the price; DECAF pays the same price for generation. Note that DECAF's abbreviation CF means conditional fairness, not counterfactual fairness.

---

## Impossibility 1: Kleinberg, Mullainathan and Raghavan (2017)

- (A) Calibration within groups
- (B) Balance for the negative class: equal mean score of negatives
- (C) Balance for the positive class: equal mean score of positives
- **Theorem:** (A), (B) and (C) together force perfect prediction or equal base rates
- An approximate version holds for approximate conditions

Note:
The setting is a risk assignment: people are placed in bins, each bin has a score. The theorem holds for any rule that computes the assignment, algorithmic or not. Kleinberg et al. connect it to the COMPAS debate: the critique focused on violations of B and C, the defence on A. Equal base rates means the share of the positive class is the same in both groups.

---

## Impossibility 2: Chouldechova (2017)

$$
\mathrm{FPR} = \frac{p}{1-p} \cdot \frac{1-\mathrm{PPV}}{\mathrm{PPV}} \cdot \left(1-\mathrm{FNR}\right)
$$

- $p$ is the prevalence (base rate) in a group
- Equal PPV and different $p$: FPR and FNR cannot both be equal
- Predictive parity and error rate balance conflict

Note:
This identity holds within each group. If two groups share the same positive predictive value but differ in prevalence, the right-hand side differs unless the false negative rates compensate, so the error rates cannot both be balanced. Chouldechova then shows how unequal error rates lead to disparate impact in a hypothetical sentencing setting.

---

## Pairwise conflicts (Barocas et al., 2023) {.dense}

| Pair | Cannot both hold when |
|---|---|
| Independence and sufficiency | $A$ and $Y$ are dependent |
| Independence and separation | $Y$ binary, $A$ and $Y$ dependent, $R$ and $Y$ dependent |
| Separation and sufficiency | all events have positive probability, $A$ and $Y$ dependent |

- The hinge in every result: base rates that differ across groups

Note:
These are Propositions 2 to 4 in the classification chapter of Fairness and Machine Learning. The common condition is dependence between the attribute and the label, which is the same as unequal base rates for a binary label. That condition is exactly what a generator controls when it produces synthetic labels.

---

## What impossibility means for a data producer

- A generator sets the base rates $\hat{P}(Y=1 \mid A)$ of $\hat{D}$
- Equal base rates in $\hat{D}$: all criteria can hold on $\hat{D}$
- Downstream models act on the real population, where base rates differ
- The theorems hold for any risk assignment, so the conflict returns there
- Equalising base rates **chooses** a point on the trade-off for every user

Note:
This is the main conceptual point for LO3. Fixing base rates in the synthetic data does not dissolve the impossibility; it moves the decision upstream to the data producer, who makes it for all downstream users at once. That is a normative choice and should be documented as one.

---

## Where bias enters (Suresh and Guttag, 2021)

```mermaid
flowchart LR
  W[World] -->|historical| C[Collection]
  C -->|representation, measurement| D[Real data]
  D --> G[Generator]
  G -->|learning| S[Synthetic data]
  S --> M[Downstream model]
  M -->|evaluation, deployment| U[Decisions]
```

- Seven sources: historical, representation, measurement, aggregation, learning, evaluation, deployment
- The generator is a second model, so the list applies twice

Note:
Historical bias exists even with perfect measurement and sampling. Representation bias: part of the population is under-represented. Measurement bias: proxies that are poor or measured differently across groups. Aggregation bias: one model for groups with different mappings. Learning bias: modelling choices amplify disparities. Evaluation bias: benchmarks that do not represent the use population. Deployment bias: use that differs from the intended use. In a synthetic data pipeline, the generator's objective adds learning bias, and evaluating it with aggregate metrics adds evaluation bias.

---

## Mechanism 1: faithful reproduction

- Likelihood, adversarial and denoising objectives all target $P(X, A, Y)$
- At the optimum the generator copies $P(Y \mid A)$ and every proxy of $A$
- Bt-GAN, Theorem 1: an ideal generation process is bias-preserving
- High fidelity (Lecture 4) and fairness conflict when $D$ is biased
- Dropping $A$ does not help: correlated features still carry it

Note:
This follows from the objectives of Lectures 2 and 3. Bt-GAN states it formally: a generation process that converges exactly to the data distribution preserves the correlations across groups. FairGAN's authors make the related point that removing the protected attribute leaves disparate impact through correlated unprotected attributes.

---

## Mechanism 2: under-representation

- A subgroup with share $\pi$ enters the expected loss with weight $\pi$
- Small groups are fitted worst; mode collapse can drop them (Lecture 2)
- Bt-GAN: representation bias; aims at a density-preserving process
- Bhanot et al. (2021): published synthetic health datasets not representative at subgroup level
- Bt-GAN on MIMIC-III: gender shares preserved, intersections distorted

Note:
The expected loss is a mixture over subgroups weighted by their shares, so a 2 percent subgroup gets 2 percent of the weight. Bhanot and colleagues analysed three published synthetic research datasets with two covariate-level disparity metrics and found that the synthetic data may not be representative at univariate and multivariate subgroup levels. In the Bt-GAN paper, all models captured gender proportions, but their intersections with other demographics showed biases.

---

## Measuring amplification

- Data leakage: accuracy of an attacker that predicts $A$ from true labels
- Model leakage: the same attacker on a model's predictions
- Amplification: model leakage exceeds data leakage (Wang et al., 2019)
- Bt-GAN uses leakage to compare generators on MIMIC-III
- Feedback loops: training on model outputs over generations can reduce fairness and minority representation (Wyllie et al., 2024)

Note:
Leakage turns bias amplification into a measurable quantity: how well can you recover the sensitive attribute from labels alone, compared with from predictions. Wyllie, Shumailov and Papernot study model-induced distribution shift over many generations, which matters when synthetic data feeds future training sets.

---

## Mechanism 3: differential privacy {.dense}

- DP-SGD (Lecture 5) costs more accuracy for under-represented groups (Bagdasaryan et al., 2019)
- Cause: gradient clipping and noise hit small groups hardest
- DP generators change subgroup sizes (Ganev et al., 2022):
  - PrivBayes shrank the gap between majority and minority: "Robin Hood"
  - PATE-GAN widened it: "Matthew"; DP-WGAN mixed
- Either way, classifiers trained on the data had disparate accuracy
- DP GAN images: utility, privacy and fairness not kept together (Cheng et al., 2021)

Note:
Bagdasaryan, Poursaeed and Shmatikov show that if the non-private model is already unfair, the private one is more unfair. Their explanation: data from under-represented groups produces larger gradients, which clipping shrinks, and added noise has the largest relative effect on those inputs. A Robin Hood effect is not a repair: it changes proportions in a way nobody chose, and Ganev and colleagues still found disparate accuracy, with minority subparts affected more.

---

## Intersectionality

- Crenshaw (1989): discrimination against Black women was invisible when law looked at race or sex alone
- Gender Shades (Buolamwini and Gebru, 2018): three commercial gender classifiers
- Darker-skinned women: error rates up to 34.7%
- Lighter-skinned men: at most 0.8%
- Benchmarks were 79.6% (IJB-A) and 86.2% (Adience) lighter-skinned

Note:
Crenshaw introduced the term in legal scholarship. Gender Shades is the standard machine learning example: both audit numbers come from the paper's abstract. The datasets used to benchmark the systems were themselves dominated by lighter-skinned subjects, a representation bias that hid the intersectional failure.

---

## Fairness gerrymandering (Kearns et al., 2018)

- Race and gender independent and uniform; predict positive for black men and white women
- Each attribute alone: 50% positive rate in every group
- Every intersection: 0% or 100%
- Subgroup fairness over a class $\mathcal{G}$ of groups:

$$
P\big(g(x)=1\big)\cdot\big|P(\hat{Y}=1) - P(\hat{Y}=1 \mid g(x)=1)\big| \le \gamma
$$

Note:
This is Example 1.1 in Kearns, Neel, Roth and Wu. The weight, the probability that a person belongs to group g, lets the definition ignore very small groups, which is necessary for statistical estimation but gives the smallest intersections weak protection. They show that auditing is computationally hard in the worst case and give oracle-efficient algorithms based on a game between a learner and an auditor.

---

## Small groups need uncertainty

- Intersections are the smallest groups: least weight, first dropped, most DP noise
- Their metrics have the largest sampling variance
- FairCert (Sikder, 2026): Clopper-Pearson intervals with Bonferroni correction over $K$ intersectional groups
- One dataset passed certification for a single attribute but failed for intersections
- Intersectional constraints in training: knowledge distillation (Sikder et al., 2025)

Note:
A point estimate of an FPR gap on a small group can be sampling noise. FairCert produces finite-sample certificates on FPR and TPR gaps for black-box classifiers. In Sikder et al. 2025, a teacher trained for accuracy passes knowledge to a student with intersectional FPR and demographic parity losses and an adversarial term that removes protected information from the representation. This is a classifier, not a generator, but it shows that intersectional constraints can be trained.

---

## Fair generative models {.dense}

| Model | Target | Mechanism | Needs |
|---|---|---|---|
| FairGAN | DP | second discriminator predicts $A$ | binary $A$ |
| DECAF | FTU, DP, CF | causal generator, edges cut at inference | known DAG |
| TabFairGAN | DP | WGAN-GP, phase II DP penalty | binary $A$ |
| Bt-GAN | DP, subgroup density | MI penalty, weighted sampling | chosen subgroups |
| FLDGM | FTU, DP | fair latent space, then GAN or diffusion | autoencoder |
| Choi et al. | representation | importance weights from a reference set | balanced reference data |

Note:
Two goals hide in this table. Decision fairness asks that a model trained on the synthetic data is fair on real data. Representation fairness asks that every subgroup appears in the intended proportion. Bt-GAN targets both. DP here is demographic parity, FTU is fairness through unawareness, and CF in DECAF is conditional fairness. FairGAN conditions the generator on the attribute; one discriminator separates real from fake, the other tries to tell the protected from the unprotected group in generated samples. TabFairGAN trains for fidelity first, then adds a discrimination score penalty to the generator loss, with one critic. FLDGM learns a fair low-dimensional latent space with an autoencoder and a distance correlation penalty, then generates latent vectors with a GAN or a diffusion model and decodes them. Choi and colleagues estimate a density ratio against a small unlabelled reference dataset, so they need no attribute labels on the training data.

---

## DECAF (van Breugel et al., 2021)

- Embeds a structural causal model in the generator's input layers
- One generator per variable, in topological order of the DAG
- Inference-time debiasing: remove edges, for example $A \to Y$
- Different fairness definitions from one trained model
- Assumption: the DAG is known or estimated by causal discovery

Note:
Because each variable is generated from its causal parents, you can intervene on the graph after training and generate data for a different fairness definition without retraining. The cost is the assumption. Bt-GAN's authors did not benchmark DECAF on MIMIC-III because causal knowledge for that database was not available.

---

## Bt-GAN (Ramachandranpillai et al., 2024)

1. **Pre-train and diagnose:** Triple GAN for partly unlabelled records; record subgroup log disparities (LDS)
2. **Bias transform:** fine-tune with a mutual information penalty; sample records by their LDSS score
3. **Rejection sampling:** the stage 1 discriminator corrects the shift from weighted sampling

Note:
Healthcare records often lack labels, so stage 1 uses a semi-supervised Triple GAN with a classifier, a generator and a discriminator. The log disparity of a subgroup compares the odds of membership in synthetic and real data. In stage 2, records from poorly represented regions are drawn more often. Stage 3 removes the bias that this weighted sampling itself injects, using discriminator rejection sampling.

---

## Bt-GAN objective

$$
\mathcal{L}_F = \mathcal{L}_{GCD} + \lambda\, I(W; S)
$$

- $W$: generated record and label; $S$: sensitive features
- $I(W;S)$ estimated with MINE (a neural estimator)
- $I(\hat{Y};S)=0$ is equivalent to statistical parity
- Ablation: $\lambda = 1$ cut accuracy severely; the authors use $\lambda = 0.5$

Note:
L GCD is the Triple GAN loss. The penalty pushes the generated space towards independence from the sensitive features. Unlike adversarial debiasing, the estimator does not compete with the generator, so it can be trained to convergence every epoch. The evaluation on MIMIC-III reports parity and AUROC gaps between white and black patients, data and model leakage, and subgroup representation. Here S is the paper's own symbol for the sensitive attribute.

---

## An evaluation protocol {.dense}

1. Fix sensitive attributes and intersections in advance, with domain experts
2. Representation: subgroup shares and per-subgroup fidelity
3. Label dependence: $\hat{P}(Y=1 \mid A)$ against $P(Y=1 \mid A)$
4. Downstream: train on $\hat{D}$, test on real; DP, TPR and FPR gaps against a train-on-real baseline
5. Amplification: leakage against the real-data baseline
6. Uncertainty: several seeds and classifiers; exact intervals for small groups

Note:
Bt-GAN recommends choosing protected attributes with domain experts, because enforcing equality on some attributes, such as age in a mortality task, can lead to unnecessary medical interventions. Representation can use the fidelity metrics of Lecture 4 within each subgroup. The baseline matters: a gap in the synthetic pipeline is only amplification if it exceeds the gap of the same model trained on real data.

---

## FairX workflow (Sikder et al., 2024)

- Load data with a sensitive attribute, or a custom CSV
- Models: Correlation Remover, TabFairGAN, DECAF, FairDisCo, Threshold Optimizer
- Utility: accuracy, AUROC, F1, precision, recall
- Fairness: demographic parity ratio, equalised odds ratio
- Synthetic data: α-precision, β-recall, authenticity (Alaa et al., 2022)
- Explanations with SHAP; plots of outcomes across two attributes

Note:
Correlation Remover is pre-processing, TabFairGAN, DECAF and FairDisCo are listed as in-processing, and the Threshold Optimizer is post-processing. Correlation Remover and Threshold Optimizer wrap their Fairlearn implementations, and DECAF runs through the synthcity library. The README lists FLDGMs, the knowledge distillation model and an intersectional bias metric as planned, not yet implemented. Lab 4 uses FairX on this workflow.

---

## Reading FairX's fairness numbers

$$
\mathrm{DPR} = \frac{\min_a P(\hat{Y}=1 \mid A=a)}{\max_a P(\hat{Y}=1 \mid A=a)}
$$

- EOR: the smaller of the TPR ratio and the FPR ratio
- 1 means parity; ratios hide direction and absolute size
- Computed on an XGBoost classifier trained on the data you pass in

Note:
These are Fairlearn's definitions; FairX calls fairlearn's demographic parity ratio and equalised odds ratio with the default worst-case aggregation. Because a classifier is trained inside the metric, the number describes the data together with that classifier. Repeat with other model classes before you call a dataset fair.

---

## Trade-offs

- Fairness and utility: stronger penalties cost accuracy (Bt-GAN ablation)
- Fairness and privacy: DP can rule out exact equality of error rates (Cummings et al., 2019)
- An approximately fair, private PAC learner exists in their setting
- Privacy, fairness and utility together: no generator in this course guarantees all three

Note:
Cummings, Gupta, Kimpara and Morgenstern show that even with full distributional access there are cases where differential privacy precludes exact equality of false positive or false negative rates. They then show a private learner that is approximately fair with high probability. The empirical results of Bagdasaryan, Ganev and Cheng point the same way for deep models and generators.

---

## Fairness release risk (LO3)

- Downstream models that are unfair on the real population
- Missing or distorted subgroups lead to wrong conclusions about them
- A bias-transforming release removes real disparities from the data
- False assurance: one attribute, one classifier, synthetic test data
- Document it: Datasheets for Datasets (Gebru et al., 2021)

Note:
I use fairness release risk for the risk that releasing a synthetic dataset leads to unfair decisions or to wrong conclusions about groups. The third point is subtle: if the generator equalises base rates, an analyst who studies health disparities with the synthetic data will find none. Datasheets organise documentation into motivation, composition, collection process, preprocessing, uses, distribution and maintenance. For synthetic data, add the generator, the fairness definition it targets, the sensitive attributes, subgroup tables and known failure cases.

---

## Open problems

- No agreed definition of a fair dataset
- Bias-preserving or bias-transforming: a normative and legal choice
- Statistics for very small intersectional groups
- Sensitive attributes that are missing or cannot be collected
- Causal methods need a graph that is rarely known
- Joint guarantees for privacy, fairness and utility

Note:
Each of these is a possible project direction. The second point is not technical: Wachter and colleagues argue that bias-preserving metrics used for decisions about individuals can require legal justification under EU non-discrimination law.

---

## Summary

- Fairness definitions conflict whenever base rates differ
- A generator sets base rates, so it makes that choice for every user
- Generators reproduce bias by design and amplify it through under-representation and DP
- Fair generators differ in target, mechanism and assumptions
- Evaluate on real data, by subgroup and intersection, with uncertainty
- Document the choices before you release

---

## Discussion

- A hospital releases one synthetic dataset to study racial disparities **and** to train triage models. Should the generator be bias-preserving or bias-transforming?
- A synthetic dataset has equal base rates by construction. Does the impossibility result still bind a model trained on it?
- FairX reports DPR above 0.9 for sex and for race separately. What can you conclude about their intersections?

Note:
Give the groups ten minutes per question. For the first, push towards the conclusion that one release cannot serve both purposes without documentation, and possibly not at all. For the second, the answer depends on where the model is evaluated. For the third, recall the gerrymandering example and the sample sizes of the intersections.

---

## References (1/2) {.refs}

- Alaa, A., van Breugel, B., Saveliev, E. S., & van der Schaar, M. (2022). How Faithful is your Synthetic Data? ICML 2022, PMLR 162, 290–306.
- Bagdasaryan, E., Poursaeed, O., & Shmatikov, V. (2019). Differential Privacy Has Disparate Impact on Model Accuracy. NeurIPS 32, 15479–15488.
- Barocas, S., Hardt, M., & Narayanan, A. (2023). Fairness and Machine Learning: Limitations and Opportunities. MIT Press. fairmlbook.org
- Bhanot, K., Qi, M., Erickson, J. S., Guyon, I., & Bennett, K. P. (2021). The Problem of Fairness in Synthetic Healthcare Data. Entropy, 23(9), 1165.
- Buolamwini, J., & Gebru, T. (2018). Gender Shades. FAT\* 2018, PMLR 81, 77–91.
- Cheng, V., Suriyakumar, V. M., Dullerud, N., Joshi, S., & Ghassemi, M. (2021). Can You Fake It Until You Make It? FAccT 2021, 149–160.
- Choi, K., Grover, A., Singh, T., Shu, R., & Ermon, S. (2020). Fair Generative Modeling via Weak Supervision. ICML 2020, PMLR 119, 1887–1898.
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact. Big Data, 5(2), 153–163.
- Crenshaw, K. (1989). Demarginalizing the Intersection of Race and Sex. University of Chicago Legal Forum, 1989(1), Article 8.
- Cummings, R., Gupta, V., Kimpara, D., & Morgenstern, J. (2019). On the Compatibility of Privacy and Fairness. UMAP 2019 Adjunct, 309–315.
- Dwork, C., Hardt, M., Pitassi, T., Reingold, O., & Zemel, R. (2012). Fairness through awareness. ITCS 2012, 214–226.
- Ganev, G., Oprisanu, B., & De Cristofaro, E. (2022). Robin Hood and Matthew Effects. ICML 2022, PMLR 162, 6944–6959.
- Gebru, T., et al. (2021). Datasheets for Datasets. Communications of the ACM, 64(12), 86–92.
- Hardt, M., Price, E., & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. NeurIPS 29, 3315–3323.
- Kearns, M., Neel, S., Roth, A., & Wu, Z. S. (2018). Preventing Fairness Gerrymandering. ICML 2018, PMLR 80, 2564–2572.

---

## References (2/2) {.refs}

- Kleinberg, J., Mullainathan, S., & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. ITCS 2017, LIPIcs 67, 43:1–43:23.
- Kusner, M., Loftus, J., Russell, C., & Silva, R. (2017). Counterfactual Fairness. NeurIPS 30, 4066–4076.
- Rajabi, A., & Garibay, O. O. (2022). TabFairGAN. Machine Learning and Knowledge Extraction, 4(2), 488–501.
- Ramachandranpillai, R., Sikder, M. F., Bergström, D., & Heintz, F. (2024). Bt-GAN. Journal of Artificial Intelligence Research, 79, 1313–1341.
- Ramachandranpillai, R., Sikder, M. F., & Heintz, F. (2023). Fair Latent Deep Generative Models (FLDGMs) for Syntax-Agnostic and Fair Synthetic Data Generation. ECAI 2023, 1938–1945.
- Sikder, M. F. (2026). FairCert: Certifiable Error Rate Fairness for ML and LLM Decision Systems. European Conference on Algorithmic Fairness, PMLR 350, 8–23.
- Sikder, M. F., Ramachandranpillai, R., de Leng, D., & Heintz, F. (2024). FairX. AEQUITAS 2024 at ECAI 2024, CEUR-WS Vol. 3808. arXiv:2406.14281
- Sikder, M. F., Ramachandranpillai, R., de Leng, D., & Heintz, F. (2025). Promoting Intersectional Fairness Through Knowledge Distillation. ECAI 2025, 3427–3434.
- Suresh, H., & Guttag, J. (2021). A Framework for Understanding Sources of Harm throughout the Machine Learning Life Cycle. EAAMO 2021.
- van Breugel, B., Kyono, T., Berrevoets, J., & van der Schaar, M. (2021). DECAF. NeurIPS 34, 22221–22233.
- Wachter, S., Mittelstadt, B., & Russell, C. (2021). Bias Preservation in Machine Learning. West Virginia Law Review, 123(3), 735.
- Wang, T., Zhao, J., Yatskar, M., Chang, K.-W., & Ordonez, V. (2019). Balanced Datasets Are Not Enough. ICCV 2019, 5310–5319.
- Wyllie, S., Shumailov, I., & Papernot, N. (2024). Fairness Feedback Loops: Training on Synthetic Data Amplifies Bias. FAccT 2024, 2113–2147.
- Xu, D., Yuan, S., Zhang, L., & Wu, X. (2018). FairGAN: Fairness-aware Generative Adversarial Networks. IEEE Big Data 2018, 570–575.
