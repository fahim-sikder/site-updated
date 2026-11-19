---
title: "Lecture 6: Fairness in synthetic data"
linkTitle: "L6: Fairness"
weight: 36
---

**Week 7** · 2 hours · Learning outcomes [LO2 and LO3](../../01-about/#learning-outcomes)

## Slides

{{< slides "gmsd-lecture-6" >}}

## Overview

This lecture asks when synthetic data is fair and how you can tell. Throughout the course, fairness means algorithmic fairness: the statistical relationship between a sensitive attribute, such as sex or ethnicity, and the outcomes that data and models produce. We start from the formal definitions developed for classifiers (group, individual and counterfactual fairness) and from the impossibility results that show these definitions conflict. We then trace how bias enters a synthetic data pipeline. A generative model can reproduce or amplify it in three ways: through the training objective itself, through the under-representation of small groups, and through the noise that differential privacy adds.

The second half turns to remedies and evidence. You will compare fair generative models: FairGAN, DECAF, TabFairGAN, Bt-GAN and FLDGM. You will then work through a protocol for evaluating the fairness of a synthetic dataset with FairX, and weigh the fairness risks of releasing such a dataset. The lecture builds on the fidelity and utility metrics of [Lecture 4](../lecture-4/) and on the differential privacy of [Lecture 5](../lecture-5/). It prepares you for [Lab 2](../../04-labs/lab-2/).

## Learning goals

After this lecture, you should be able to:

1. Define demographic parity, equalised odds, equal opportunity, calibration within groups, individual fairness and counterfactual fairness, and state which of them you can check on a dataset without training a model (LO2).
2. State the impossibility results of Kleinberg, Mullainathan and Raghavan and of Chouldechova, and explain why the fairness target of a generator is a normative choice made for every downstream user (LO3).
3. Explain how the training objective, under-representation and differential privacy can make synthetic data less fair than the real data it came from (LO1, LO3).
4. Compare how FairGAN, DECAF, TabFairGAN and Bt-GAN intervene in data generation, and name the assumption each one rests on (LO1, LO2).
5. Design a fairness evaluation of a synthetic dataset that covers intersectional subgroups and statistical uncertainty, and use it to argue for or against release (LO2, LO3).

## Before the lecture

Read these two papers before the lecture.

- Ramachandranpillai, R., Sikder, M. F., Bergström, D., & Heintz, F. (2024). Bt-GAN: Generating Fair Synthetic Healthdata via Bias-transforming Generative Adversarial Networks. *Journal of Artificial Intelligence Research*, 79, 1313–1341. [doi:10.1613/jair.1.15317](https://doi.org/10.1613/jair.1.15317) · [Publication page](/publications/bias-transforming-gan/)
  *What to look for:* the two kinds of bias the paper separates (correlation bias and representation bias), the three training stages, and which fairness definition the mutual information penalty enforces.
- Sikder, M. F., Ramachandranpillai, R., de Leng, D., & Heintz, F. (2024). FairX: A comprehensive benchmarking tool for model analysis using fairness, utility, and explainability. *Fairness and Bias in AI 2024 (AEQUITAS 2024), co-located with ECAI 2024*, CEUR Workshop Proceedings, Vol. 3808. [Paper](https://ceur-ws.org/Vol-3808/paper16.pdf) · [arXiv:2406.14281](https://arxiv.org/abs/2406.14281) · [Code](https://github.com/fahim-sikder/FairX) · [Publication page](/publications/fairx/)
  *What to look for:* the evaluation workflow, which bias-mitigation models the tool wraps, which metrics it reports, and the fact that its fairness metrics are computed on a classifier trained on the data you pass in.

> [!NOTE]
> The course leader is a co-author of both papers. Read them as critically as any other paper; two of the discussion questions ask you to find their limits.

## Lecture notes

### Fairness as a property of synthetic data

We write $X$ for the non-sensitive features, $A$ for the sensitive attribute with groups $a$ and $b$, $Y$ for the observed label, $R$ for a score and $\hat{Y}$ for a binary prediction. $D$ is the real dataset and $\hat{D}$ the synthetic one. The attribute is binary unless stated otherwise; several papers we cite write $S$ for it.

Most fairness definitions describe a predictor, not a dataset. A synthetic dataset makes no decisions, so you need two kinds of evidence. Direct evidence comes from the synthetic distribution: the label rate $\hat{P}(Y=1 \mid A=a)$ in each group, or the share of each subgroup. Indirect evidence comes from a classifier that you train on $\hat{D}$ and test on held-out real data.

van Breugel et al. ([2021](https://proceedings.neurips.cc/paper_files/paper/2021/hash/ba9fab001f67381e56e410575874d967-Abstract.html)) make the indirect view precise. Given a fairness definition and an evaluation distribution $P$, a distribution $P'$ is fair if the optimal predictor trained on $P'$ satisfies the definition when evaluated on $P$. The evaluation distribution matters. If you randomise $A$ in the synthetic data, the data passes a fairness check on itself. A model trained on it can still discriminate on real data through features that correlate with $A$.

### Group fairness: independence, separation and sufficiency

Barocas, Hardt and Narayanan ([2023](https://fairmlbook.org/classification.html)) group the statistical criteria into three families, each a conditional independence statement.

**Independence (demographic parity)** requires $\hat{Y} \perp A$. For a binary decision:

$$
P(\hat{Y}=1 \mid A=a) = P(\hat{Y}=1 \mid A=b).
$$

Demographic parity is the only one of the three that ignores $Y$, so you can check its dataset version on $\hat{D}$ alone by comparing $\hat{P}(Y=1 \mid A=a)$ across groups. FairGAN calls this difference the risk difference ([Xu et al., 2018](https://doi.org/10.1109/BigData.2018.8622525)); TabFairGAN calls it the discrimination score ([Rajabi and Garibay, 2022](https://doi.org/10.3390/make4020022)). Fairlearn, which FairX uses, reports the ratio of the smallest to the largest group selection rate ([Weerts et al., 2023](https://jmlr.org/papers/v24/23-0389.html)).

**Separation (equalised odds).** Hardt, Price and Srebro ([2016](https://proceedings.neurips.cc/paper_files/paper/2016/hash/6a9659feb1216f14f7384ba499518b38-Abstract.html)) define equalised odds as $\hat{Y} \perp A \mid Y$. For binary $Y$:

$$
P(\hat{Y}=1 \mid A=a, Y=y) = P(\hat{Y}=1 \mid A=b, Y=y), \qquad y \in \{0, 1\},
$$

that is, equal true positive rates and equal false positive rates. Equal opportunity requires only $y=1$: equal true positive rates. Kearns et al. ([2018](https://proceedings.mlr.press/v80/kearns18a.html)) use "equal opportunity" for equal false positive rates, so check which rate a paper means.

**Sufficiency (calibration)** requires $Y \perp A \mid R$. A score is calibrated by group if

$$
P(Y=1 \mid R=r, A=a) = r \quad \text{for all } r \text{ and } a.
$$

Barocas et al. show that calibration by group and sufficiency are essentially equivalent.

Separation and sufficiency condition on the observed label, so they take the recorded outcomes as ground truth. If $Y$ carries historical or measurement bias, a predictor can satisfy equalised odds and still reproduce that bias. Kusner et al. ([2017](https://proceedings.neurips.cc/paper_files/paper/2017/hash/a486cd07e4ac3d270571622f4f316ec5-Abstract.html)) note that if people in the training data have not had equal opportunity, enforcing equalised odds will not remedy it. Wachter, Mittelstadt and Russell ([2021](https://researchrepository.wvu.edu/wvlr/vol123/iss3/4)) classify fairness metrics by how they handle pre-existing bias, as "bias-preserving" or "bias-transforming". They argue that bias-preserving metrics used for decisions about individuals can require legal justification under EU non-discrimination law, and recommend bias-transforming metrics. Bt-GAN takes its name from this distinction.

### Individual and counterfactual fairness

Dwork et al. ([2012](https://doi.org/10.1145/2090236.2090255)) ask that similar individuals be treated similarly. A classifier is a randomised map $M$ from individuals to distributions over outcomes. Given a task-specific similarity metric $d$, $M$ is individually fair if it satisfies the Lipschitz condition

$$
D\big(M(x), M(x')\big) \le d(x, x') \quad \text{for all } x, x',
$$

where $D$ is a distance between distributions. Whoever defines $d$ decides who counts as similar; that is the hard part. Dwork et al. show that the Lipschitz condition implies statistical parity between two groups if and only if the earthmover distance between them is small. Synthetic records are not people, so the condition applies to models trained on $\hat{D}$ and used on real individuals.

Counterfactual fairness ([Kusner et al., 2017](https://proceedings.neurips.cc/paper_files/paper/2017/hash/a486cd07e4ac3d270571622f4f316ec5-Abstract.html)) needs a causal model with background variables $U$. A predictor is counterfactually fair if, for every context $X=x$, $A=a$, every $y$ and every attainable $a'$,

$$
P\big(\hat{Y}_{A \leftarrow a}(U) = y \mid X=x, A=a\big) = P\big(\hat{Y}_{A \leftarrow a'}(U) = y \mid X=x, A=a\big).
$$

A predictor built only from non-descendants of $A$ satisfies the definition. DECAF also needs a causal graph; note that its abbreviation CF means conditional fairness, not counterfactual fairness.

### Impossibility results

Kleinberg, Mullainathan and Raghavan ([2017](https://doi.org/10.4230/LIPIcs.ITCS.2017.43)) study risk assignments, in which people are placed in bins and each bin carries a score. They state three conditions:

- (A) **Calibration within groups:** in each bin, the fraction of positives in each group equals the bin's score.
- (B) **Balance for the negative class:** the average score of negatives is the same in both groups.
- (C) **Balance for the positive class:** the average score of positives is the same in both groups.

> [!IMPORTANT] Theorem (Kleinberg et al., 2017)
> If a risk assignment satisfies (A), (B) and (C), then the instance allows perfect prediction or the two groups have equal base rates.

An approximate version also holds, and the result applies however the scores are computed. In the debate on the COMPAS recidivism tool, the critique concerned (B) and (C), and the defence showed (A).

Chouldechova ([2017](https://doi.org/10.1089/big.2016.0047)) reaches a related conclusion from an identity. In a group with prevalence $p$, a binary classifier satisfies

$$
\mathrm{FPR} = \frac{p}{1-p} \cdot \frac{1-\mathrm{PPV}}{\mathrm{PPV}} \cdot \left(1 - \mathrm{FNR}\right).
$$

If the positive predictive value (PPV) is equal across groups and the prevalence differs, the false positive and false negative rates cannot both be equal.

Barocas et al. ([2023](https://fairmlbook.org/classification.html)) state the pairwise conflicts:

| Pair | Cannot both hold when |
|---|---|
| Independence and sufficiency | $A$ and $Y$ are not independent |
| Independence and separation | $Y$ is binary, $A$ and $Y$ are not independent, and $R$ and $Y$ are not independent |
| Separation and sufficiency | all events of $(A, R, Y)$ have positive probability, and $A$ and $Y$ are not independent |

Pleiss et al. ([2017](https://proceedings.neurips.cc/paper_files/paper/2017/hash/b8b9c74ac526fffbeb2d39ab038d1cd7-Abstract.html)) show that calibration is compatible with only a single error constraint.

> [!IMPORTANT] What the impossibility results mean for a data producer
> In every result above, the obstacle is that base rates differ: $P(Y=1 \mid A=a) \neq P(Y=1 \mid A=b)$. A generator decides the base rates of $\hat{D}$. If it equalises them, all criteria can hold at once on $\hat{D}$, for example with a constant score. Downstream models, however, act on the real population, where base rates still differ, and the theorems hold for any risk assignment. Equalising base rates therefore does not remove the conflict. It chooses a point in the trade-off on behalf of every downstream user, and that choice belongs in the documentation.

### Where bias enters a synthetic data pipeline

Suresh and Guttag ([2021](https://doi.org/10.1145/3465416.3483305)) name seven sources of harm in the machine learning life cycle. A synthetic data pipeline contains a second model, the generator, so each source can appear twice.

```mermaid
flowchart LR
  W[World] -->|historical| C[Collection]
  C -->|representation, measurement| D[Real data]
  D --> G[Generator]
  G -->|learning| S[Synthetic data]
  S --> M[Downstream model]
  M -->|evaluation, deployment| U[Decisions]
```

| Source | Meaning | In a synthetic data pipeline |
|---|---|---|
| Historical | The world produces harmful outcomes, even with perfect measurement | A faithful generator copies it |
| Representation | The sample under-represents part of the population | Small groups carry little weight in the loss |
| Measurement | Proxies are poor or differ across groups | The generator learns the proxy and its error |
| Aggregation | One model for groups with different mappings | One generator fits the majority |
| Learning | Modelling choices amplify disparities | Objective, clipping and privacy noise |
| Evaluation | Benchmarks do not represent the use population | Aggregate fidelity hides subgroup failures |
| Deployment | Intended and actual use differ | Data used for untested tasks |

### How generative models carry and amplify bias

**Faithful reproduction.** The likelihood, adversarial and denoising objectives of [Lecture 2](../lecture-2/) and [Lecture 3](../lecture-3/) all aim at $P(X, A, Y)$. At the optimum, the generator reproduces every dependency, including $P(Y \mid A)$ and every proxy of $A$. Bt-GAN states this formally: what the paper calls an ideal generation process, one that converges exactly to the data distribution, is bias-preserving ([Ramachandranpillai et al., 2024](https://doi.org/10.1613/jair.1.15317), Theorem 1). High fidelity and fairness therefore conflict whenever the real data is biased. Dropping $A$ does not help, because correlated features still carry it ([Xu et al., 2018](https://doi.org/10.1109/BigData.2018.8622525)).

**Under-representation.** The training loss is an expectation over the data, so a subgroup with share $\pi$ enters it with weight $\pi$. Small groups are fitted worst, and mode collapse (Lecture 2) can drop them. Bt-GAN calls this representation bias. Bhanot et al. ([2021](https://doi.org/10.3390/e23091165)) found that three published synthetic healthcare datasets may not be representative at univariate and multivariate subgroup levels. In the Bt-GAN experiments on MIMIC-III, all models captured the gender proportions, but their intersections with other demographics were biased.

**Amplification.** Wang et al. ([2019](https://openaccess.thecvf.com/content_ICCV_2019/html/Wang_Balanced_Datasets_Are_Not_Enough_Estimating_and_Mitigating_Gender_Bias_ICCV_2019_paper.html)) measure it with leakage. Data leakage is the accuracy of an attacker that predicts the protected attribute from true labels; model leakage is that accuracy from a model's outputs. A model amplifies bias if model leakage exceeds data leakage. Bt-GAN uses both to compare generators. Wyllie, Shumailov and Papernot ([2024](https://doi.org/10.1145/3630106.3659029)) show that when model outputs enter later training sets, performance, fairness and minoritised group representation can degrade over generations, even from unbiased data.

**Differential privacy.** [Lecture 5](../lecture-5/) introduced DP-SGD. Bagdasaryan, Poursaeed and Shmatikov ([2019](https://proceedings.neurips.cc/paper_files/paper/2019/hash/fc0de4e0396fff257ea362983c2dda5a-Abstract.html)) show that it costs more accuracy for under-represented classes and subgroups, so an unfair model becomes more unfair. They trace the effect to gradient clipping and noise: under-represented data produces larger gradients, which clipping shrinks. Ganev, Oprisanu and De Cristofaro ([2022](https://proceedings.mlr.press/v162/ganev22a.html)) study private generators. PrivBayes reduced the size gap between majority and minority subgroups (a "Robin Hood" effect), PATE-GAN increased it (a "Matthew" effect), and DP-WGAN was mixed. In both directions, classifiers trained on the synthetic data had disparate accuracy that hit the under-represented parts harder. Cheng et al. ([2021](https://doi.org/10.1145/3442188.3445879)) found that existing DP GANs for images could not maintain utility, privacy and fairness at the same time.

> [!WARNING]
> A Robin Hood effect is not a fairness repair. It changes subgroup proportions in a way nobody chose, and the classifiers still had disparate accuracy.

### Intersectionality

Crenshaw ([1989](https://chicagounbound.uchicago.edu/uclf/vol1989/iss1/8)) introduced intersectionality in a critique of antidiscrimination doctrine, which treated discrimination against Black women as either race or sex discrimination and so missed discrimination at the intersection. Buolamwini and Gebru ([2018](https://proceedings.mlr.press/v81/buolamwini18a.html)) found that two facial analysis benchmarks were 79.6% (IJB-A) and 86.2% (Adience) lighter-skinned. On a dataset balanced by gender and skin type, three commercial gender classifiers had error rates of up to 34.7% for darker-skinned women, against at most 0.8% for lighter-skinned men.

Kearns et al. ([2018](https://proceedings.mlr.press/v80/kearns18a.html)) show why checking one attribute at a time fails. Let race and gender be independent and uniform, and let a classifier label black men and white women positive. Every gender and every race has a positive rate of 50%, yet each intersection has 0% or 100%. They call this fairness gerrymandering and define subgroup fairness over a class $\mathcal{G}$ of group indicators. For statistical parity, a classifier is $\gamma$-fair if, for every $g \in \mathcal{G}$,

$$
P\big(g(x)=1\big) \cdot \big|P(\hat{Y}=1) - P(\hat{Y}=1 \mid g(x)=1)\big| \le \gamma.
$$

The weight $P(g(x)=1)$ is needed for statistical estimation, but it gives the smallest intersections the weakest protection. Auditing for subgroup fairness is computationally hard in the worst case; Kearns et al. give oracle-efficient algorithms.

In synthetic data, the smallest intersections suffer every mechanism above: least weight in the loss, first to be dropped, most affected by privacy noise. Their metrics also have the largest sampling variance. FairCert ([Sikder, 2026](https://proceedings.mlr.press/v350/sikder26a.html)) gives finite-sample certificates on the false and true positive rate gaps of classifiers. It uses Clopper-Pearson intervals with a Bonferroni correction across $K$ intersectional groups. On one dataset, certification passed for a single attribute but failed for intersections. Sikder et al. ([2025](https://doi.org/10.3233/FAIA251214)) train intersectional fairness into a classifier by knowledge distillation, with losses for false positive rate and demographic parity across intersectional groups.

### Fair generative models

A fair generator can pursue decision fairness (a model trained on $\hat{D}$ is fair on real data) or representation fairness ($\hat{D}$ contains every subgroup in the intended proportion).

| Model | Target | Mechanism | Assumption |
|---|---|---|---|
| FairGAN ([Xu et al., 2018](https://doi.org/10.1109/BigData.2018.8622525)) | Demographic parity | Generator conditioned on $A$; a second discriminator tries to recover the group from generated samples | One binary attribute |
| DECAF ([van Breugel et al., 2021](https://proceedings.neurips.cc/paper_files/paper/2021/hash/ba9fab001f67381e56e410575874d967-Abstract.html)) | Unawareness, demographic parity or conditional fairness | One generator per variable along a causal graph; biased edges removed at inference | Known or estimated causal graph |
| TabFairGAN ([Rajabi and Garibay, 2022](https://doi.org/10.3390/make4020022)) | Demographic parity | WGAN-GP trained for fidelity, then with a discrimination score penalty | One binary attribute |
| Bt-GAN ([Ramachandranpillai et al., 2024](https://doi.org/10.1613/jair.1.15317)) | Statistical parity and subgroup density | Mutual information penalty, weighted sampling, rejection sampling | Subgroups chosen in advance |
| FLDGM ([Ramachandranpillai et al., 2023](https://doi.org/10.3233/FAIA230484)) | Unawareness or demographic parity | Fair latent space from an autoencoder; a GAN or diffusion model generates in it | The decoder keeps latent fairness |
| Choi et al. ([2020](https://proceedings.mlr.press/v119/choi20a.html)) | Representation | Importance weights from a density ratio against unlabelled reference data | A reference dataset |

DECAF separates training from debiasing. Each variable is generated from its causal parents, so after training you can remove an edge, such as $A \to Y$, and generate data for another fairness definition without retraining. Bt-GAN's authors did not benchmark DECAF on MIMIC-III because causal knowledge for that database was not available.

**Bt-GAN** proceeds in three stages.

1. *Pre-train and diagnose.* A semi-supervised Triple GAN handles records with missing labels. Bt-GAN records each subgroup's log disparity, which compares the odds of subgroup membership in synthetic and real data.
2. *Bias transform.* The generator is fine-tuned with $\mathcal{L}_F = \mathcal{L}_{GCD} + \lambda \, I(W; S)$, where $\mathcal{L}_{GCD}$ is the Triple GAN loss, $W$ the generated features and label, and $S$ the sensitive features. MINE, a neural estimator, estimates the mutual information; $I(\hat{Y}; S) = 0$ is equivalent to statistical parity. Training records are sampled in proportion to their log disparity score, so under-represented regions are seen more often.
3. *Rejection sampling.* Discriminator rejection sampling with the stage 1 discriminator corrects the shift that weighted sampling introduces.

The evaluation on MIMIC-III separates utility, parity and AUROC gaps between white and black patients, leakage, and subgroup representation. With $\lambda = 1$, accuracy dropped severely, and Ramachandranpillai et al. chose $\lambda = 0.5$.

Most of these models target demographic parity for one binary attribute, and few handle intersections. All except Choi et al. need the sensitive attribute at training time. Equalising $P(Y \mid A)$ alters a fact about the population, which matters if anyone later studies disparities with the data.

### Evaluating the fairness of a synthetic dataset

A defensible evaluation answers six questions.

1. **Which attributes?** Fix the sensitive attributes and intersections in advance. Bt-GAN recommends choosing them with domain experts: enforcing equality on age in a mortality task can lead to unnecessary medical interventions.
2. **Who is represented?** Compare subgroup shares in $\hat{D}$ and $D$, and compute fidelity within each subgroup, for example α-precision and β-recall ([Alaa et al., 2022](https://proceedings.mlr.press/v162/alaa22a.html)). Bt-GAN calls a subgroup adequately represented when its log disparity lies between $\log 0.9$ and $-\log 0.9$, following Bhanot et al. (2021).
3. **How do labels depend on the attribute?** Compare $\hat{P}(Y=1 \mid A=a)$ with $P(Y=1 \mid A=a)$.
4. **Are downstream models fair on real data?** Train on $\hat{D}$, test on real data, and report demographic parity and error rate gaps against the same model trained on real data. Repeat with several model classes.
5. **Is bias amplified?** Only a gap larger than the real-data baseline counts. Leakage gives a second view.
6. **How certain are the numbers?** Report variation over seeds and splits, with exact intervals for small groups.

**The FairX workflow.** FairX ([Sikder et al., 2024](https://arxiv.org/abs/2406.14281)) loads a benchmark dataset or your own CSV with a named sensitive attribute. It trains Correlation Remover (pre-processing), TabFairGAN, DECAF or FairDisCo ([Liu et al., 2022](https://doi.org/10.1145/3534678.3539302)) (listed as in-processing), or Threshold Optimizer (post-processing, from Fairlearn, based on Hardt et al., 2016). It reports utility, fairness (demographic parity ratio and equalised odds ratio), α-precision, β-recall and authenticity, SHAP explanations and a plot of outcomes across two attributes. The README lists FLDGMs, the knowledge distillation model and an intersectional bias metric as planned, not yet released. Adapted from the repository's evaluation tutorial:

```python
from fairx.dataset import BaseDataClass
from fairx.metrics import FairnessUtils, DataUtilsMetrics

data_module = BaseDataClass('Adult-Income', 'sex', attach_target=False)
_, _, tf_data = data_module.preprocess_data()
splitted_data = data_module.split_data(tf_data)

print(DataUtilsMetrics(splitted_data).evaluate_utility())
print(FairnessUtils(splitted_data).evaluate_fairness())
```

FairX computes its fairness numbers with Fairlearn:

$$
\mathrm{DPR} = \frac{\min_a P(\hat{Y}=1 \mid A=a)}{\max_a P(\hat{Y}=1 \mid A=a)},
$$

and the equalised odds ratio is the smaller of the true positive rate ratio and the false positive rate ratio. A value of 1 means parity. Ratios hide the direction and size of a gap, and they become unstable when rates are small. FairX trains an XGBoost classifier inside the metric, so the numbers describe the data together with that classifier.

### Trade-offs between fairness, utility and privacy

Fairness constraints cost utility, as the ablation of Bt-GAN shows. Fairness and privacy also conflict. Cummings et al. ([2019](https://doi.org/10.1145/3314183.3323847)) show that even with full access to the distribution, differential privacy can rule out exact equality of false positive or false negative rates. They also show that a private PAC learner can be approximately fair with high probability. The results of Bagdasaryan et al. (2019), Ganev et al. (2022) and Cheng et al. (2021) point the same way for deep models and generators. No generator in this course offers joint guarantees on privacy, fairness and utility.

### Fairness release risk

In this course, *fairness release risk* is the risk that releasing a synthetic dataset leads to unfair decisions or to wrong conclusions about groups. It takes five common forms.

1. **Downstream unfairness.** Models trained on $\hat{D}$ are unfair on the real population.
2. **Erasure.** Missing or distorted subgroups lead to wrong conclusions about those groups; Ganev et al. (2022) warn of unreliable or unfair conclusions.
3. **Altered facts.** A bias-transforming release removes real disparities, so an analyst who studies inequity with it finds none.
4. **False assurance.** Fairness was checked on one attribute at a time, with one classifier, or on synthetic test data.
5. **Compounding.** Released data feeds later training and bias grows over generations ([Wyllie et al., 2024](https://doi.org/10.1145/3630106.3659029)).

Documentation is the main control. Datasheets for Datasets ([Gebru et al., 2021](https://doi.org/10.1145/3458723)) organise questions under motivation, composition, collection process, preprocessing, cleaning and labelling, uses, distribution and maintenance. For synthetic data, add the generator, the fairness definition it targets, the attributes and intersections evaluated, subgroup results with uncertainty, known failures, and uses you advise against.

### Limitations and open problems

- **What is a fair dataset?** Label parity, representation parity and distributional fairness differ and can conflict.
- **Preserve or transform?** The choice is normative and legal ([Wachter et al., 2021](https://researchrepository.wvu.edu/wvlr/vol123/iss3/4)); one release may not serve both disparity research and parity.
- **Small groups.** Statistical power for the smallest intersections is an open problem.
- **Missing attributes.** Many datasets do not, or cannot lawfully, record the sensitive attribute.
- **Unknown causal structure.** Causal methods need a graph that is rarely known.
- **Joint guarantees** for privacy, fairness and utility remain open.
- **Beyond tabular data.** Time series, such as longitudinal health records, and multi-valued attributes are less studied.

## Discussion questions

1. A hospital wants to release one synthetic dataset for two uses: researchers who study racial disparities in ICU mortality, and developers who train triage models. Should the generator be bias-preserving or bias-transforming? Can one release serve both uses?

   {{< spoiler text="Show a model answer" >}}
   The two uses need different data. Disparity research needs $P(Y \mid A)$ as it is, so it needs a bias-preserving release. Developers who want parity may prefer a bias-transforming release, but the impossibility results still bind their models on real patients, so the release only chooses a trade-off for them. One option is two releases with different documentation. Another is a bias-preserving release with the fairness intervention left to each developer, who can then pick a criterion that suits the task. Either way, the datasheet must state what was changed.
   {{< /spoiler >}}

2. A generator produces data with equal base rates by construction. Does the theorem of Kleinberg et al. (2017) still constrain a model trained on that data? Distinguish evaluation on synthetic test data from evaluation on real data.

   {{< spoiler text="Show a model answer" >}}
   On synthetic test data with equal base rates, all three conditions can hold, for example with a constant score. On real data, base rates still differ, and the theorem holds for any risk assignment, however it was computed. A model trained on the synthetic data is such an assignment, so unless it predicts perfectly, it violates at least one condition on the real population. This is why the distributional definition of van Breugel et al. (2021) names the evaluation distribution explicitly.
   {{< /spoiler >}}

3. FairX reports a demographic parity ratio above 0.9 for sex and, separately, for race. What can you conclude about the four intersections? What would you compute next, and how large must each intersection be for the answer to mean something?

   {{< spoiler text="Show a hint" >}}
   Nothing follows for the intersections: the gerrymandering example of Kearns et al. (2018) has perfect marginal parity and maximal intersectional disparity. Compute selection rates per intersection, with exact confidence intervals, and correct for the number of groups as FairCert does. If an intersection has very few members, report that the evaluation is inconclusive rather than that the data is fair.
   {{< /spoiler >}}

4. You must release with differential privacy (Lecture 5). How would you detect whether your generator shows a Robin Hood or a Matthew effect, and is a Robin Hood effect acceptable?

   {{< spoiler text="Show a hint" >}}
   Compare subgroup shares in $\hat{D}$ and $D$ over several privacy budgets and seeds, then compare per-group accuracy of downstream classifiers. A Robin Hood effect is still a distortion that nobody chose, and Ganev et al. (2022) found disparate accuracy in both directions.
   {{< /spoiler >}}

5. Bt-GAN enforces statistical parity through $I(W; S) \approx 0$, and FairX measures fairness with one XGBoost classifier. Identify one assumption in each paper that your own research data would violate, and say how you would test for it.

6. Synthetic data is often presented as a way to correct biased data, for example by oversampling a minority group. Using the mechanisms in this lecture, argue when generated minority samples help and when they only repeat what the generator learnt from very few records.

## Further reading

- Barocas, S., Hardt, M., & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. [fairmlbook.org](https://fairmlbook.org/). The chapter "Classification" gives the full treatment of independence, separation and sufficiency and their conflicts.
- Pleiss, G., Raghavan, M., Wu, F., Kleinberg, J., & Weinberger, K. Q. (2017). On Fairness and Calibration. *Advances in Neural Information Processing Systems*, 30. [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2017/hash/b8b9c74ac526fffbeb2d39ab038d1cd7-Abstract.html). Shows how little room calibration leaves for error rate constraints.
- Wachter, S., Mittelstadt, B., & Russell, C. (2021). Bias Preservation in Machine Learning: The Legality of Fairness Metrics Under EU Non-Discrimination Law. *West Virginia Law Review*, 123(3), 735. [WVU Research Repository](https://researchrepository.wvu.edu/wvlr/vol123/iss3/4). The legal argument behind the bias-preserving and bias-transforming distinction.
- Bhanot, K., Qi, M., Erickson, J. S., Guyon, I., & Bennett, K. P. (2021). The Problem of Fairness in Synthetic Healthcare Data. *Entropy*, 23(9), 1165. [doi:10.3390/e23091165](https://doi.org/10.3390/e23091165). Subgroup disparity metrics for synthetic health data.
- Choi, K., Grover, A., Singh, T., Shu, R., & Ermon, S. (2020). Fair Generative Modeling via Weak Supervision. *Proceedings of the 37th International Conference on Machine Learning*, PMLR 119, 1887–1898. [PMLR](https://proceedings.mlr.press/v119/choi20a.html). Representation fairness without attribute labels.
- Ramachandranpillai, R., Sikder, M. F., & Heintz, F. (2023). Fair Latent Deep Generative Models (FLDGMs) for Syntax-Agnostic and Fair Synthetic Data Generation. *ECAI 2023*, Frontiers in Artificial Intelligence and Applications 372, 1938–1945. [doi:10.3233/FAIA230484](https://doi.org/10.3233/FAIA230484) · [Publication page](/publications/fair-latent-generative-models/). Separates fairness optimisation from generation.
- Wyllie, S., Shumailov, I., & Papernot, N. (2024). Fairness Feedback Loops: Training on Synthetic Data Amplifies Bias. *FAccT 2024*, 2113–2147. [doi:10.1145/3630106.3659029](https://doi.org/10.1145/3630106.3659029). What happens when synthetic data feeds later training.
- Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T. (2019). Model Cards for Model Reporting. *FAT\* 2019*, 220–229. [doi:10.1145/3287560.3287596](https://doi.org/10.1145/3287560.3287596). Documentation for the generator itself, including results for intersectional groups.

## References

- Alaa, A., van Breugel, B., Saveliev, E. S., & van der Schaar, M. (2022). How Faithful is your Synthetic Data? Sample-level Metrics for Evaluating and Auditing Generative Models. *Proceedings of the 39th International Conference on Machine Learning*, PMLR 162, 290–306. [PMLR](https://proceedings.mlr.press/v162/alaa22a.html)
- Bagdasaryan, E., Poursaeed, O., & Shmatikov, V. (2019). Differential Privacy Has Disparate Impact on Model Accuracy. *Advances in Neural Information Processing Systems*, 32, 15479–15488. [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2019/hash/fc0de4e0396fff257ea362983c2dda5a-Abstract.html)
- Barocas, S., Hardt, M., & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. [fairmlbook.org](https://fairmlbook.org/)
- Bhanot, K., Qi, M., Erickson, J. S., Guyon, I., & Bennett, K. P. (2021). The Problem of Fairness in Synthetic Healthcare Data. *Entropy*, 23(9), 1165. [doi:10.3390/e23091165](https://doi.org/10.3390/e23091165)
- Buolamwini, J., & Gebru, T. (2018). Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *Proceedings of the 1st Conference on Fairness, Accountability and Transparency*, PMLR 81, 77–91. [PMLR](https://proceedings.mlr.press/v81/buolamwini18a.html)
- Cheng, V., Suriyakumar, V. M., Dullerud, N., Joshi, S., & Ghassemi, M. (2021). Can You Fake It Until You Make It? Impacts of Differentially Private Synthetic Data on Downstream Classification Fairness. *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency*, 149–160. [doi:10.1145/3442188.3445879](https://doi.org/10.1145/3442188.3445879)
- Choi, K., Grover, A., Singh, T., Shu, R., & Ermon, S. (2020). Fair Generative Modeling via Weak Supervision. *Proceedings of the 37th International Conference on Machine Learning*, PMLR 119, 1887–1898. [PMLR](https://proceedings.mlr.press/v119/choi20a.html)
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. [doi:10.1089/big.2016.0047](https://doi.org/10.1089/big.2016.0047)
- Crenshaw, K. (1989). Demarginalizing the Intersection of Race and Sex: A Black Feminist Critique of Antidiscrimination Doctrine, Feminist Theory and Antiracist Politics. *University of Chicago Legal Forum*, 1989(1), Article 8. [Chicago Unbound](https://chicagounbound.uchicago.edu/uclf/vol1989/iss1/8)
- Cummings, R., Gupta, V., Kimpara, D., & Morgenstern, J. (2019). On the Compatibility of Privacy and Fairness. *Adjunct Publication of the 27th Conference on User Modeling, Adaptation and Personalization*, 309–315. [doi:10.1145/3314183.3323847](https://doi.org/10.1145/3314183.3323847)
- Dwork, C., Hardt, M., Pitassi, T., Reingold, O., & Zemel, R. (2012). Fairness through awareness. *Proceedings of the 3rd Innovations in Theoretical Computer Science Conference*, 214–226. [doi:10.1145/2090236.2090255](https://doi.org/10.1145/2090236.2090255)
- Ganev, G., Oprisanu, B., & De Cristofaro, E. (2022). Robin Hood and Matthew Effects: Differential Privacy Has Disparate Impact on Synthetic Data. *Proceedings of the 39th International Conference on Machine Learning*, PMLR 162, 6944–6959. [PMLR](https://proceedings.mlr.press/v162/ganev22a.html)
- Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for Datasets. *Communications of the ACM*, 64(12), 86–92. [doi:10.1145/3458723](https://doi.org/10.1145/3458723)
- Hardt, M., Price, E., & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems*, 29, 3315–3323. [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2016/hash/6a9659feb1216f14f7384ba499518b38-Abstract.html)
- Kearns, M., Neel, S., Roth, A., & Wu, Z. S. (2018). Preventing Fairness Gerrymandering: Auditing and Learning for Subgroup Fairness. *Proceedings of the 35th International Conference on Machine Learning*, PMLR 80, 2564–2572. [PMLR](https://proceedings.mlr.press/v80/kearns18a.html)
- Kleinberg, J., Mullainathan, S., & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *8th Innovations in Theoretical Computer Science Conference (ITCS 2017)*, LIPIcs 67, 43:1–43:23. [doi:10.4230/LIPIcs.ITCS.2017.43](https://doi.org/10.4230/LIPIcs.ITCS.2017.43)
- Kusner, M., Loftus, J., Russell, C., & Silva, R. (2017). Counterfactual Fairness. *Advances in Neural Information Processing Systems*, 30, 4066–4076. [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2017/hash/a486cd07e4ac3d270571622f4f316ec5-Abstract.html)
- Liu, J., Li, Z., Yao, Y., Xu, F., Ma, X., Xu, M., & Tong, H. (2022). Fair Representation Learning: An Alternative to Mutual Information. *Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, 1088–1097. [doi:10.1145/3534678.3539302](https://doi.org/10.1145/3534678.3539302)
- Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T. (2019). Model Cards for Model Reporting. *Proceedings of the Conference on Fairness, Accountability, and Transparency (FAT\* 2019)*, 220–229. [doi:10.1145/3287560.3287596](https://doi.org/10.1145/3287560.3287596)
- Pleiss, G., Raghavan, M., Wu, F., Kleinberg, J., & Weinberger, K. Q. (2017). On Fairness and Calibration. *Advances in Neural Information Processing Systems*, 30. [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2017/hash/b8b9c74ac526fffbeb2d39ab038d1cd7-Abstract.html)
- Rajabi, A., & Garibay, O. O. (2022). TabFairGAN: Fair Tabular Data Generation with Generative Adversarial Networks. *Machine Learning and Knowledge Extraction*, 4(2), 488–501. [doi:10.3390/make4020022](https://doi.org/10.3390/make4020022)
- Ramachandranpillai, R., Sikder, M. F., Bergström, D., & Heintz, F. (2024). Bt-GAN: Generating Fair Synthetic Healthdata via Bias-transforming Generative Adversarial Networks. *Journal of Artificial Intelligence Research*, 79, 1313–1341. [doi:10.1613/jair.1.15317](https://doi.org/10.1613/jair.1.15317)
- Ramachandranpillai, R., Sikder, M. F., & Heintz, F. (2023). Fair Latent Deep Generative Models (FLDGMs) for Syntax-Agnostic and Fair Synthetic Data Generation. *ECAI 2023*, Frontiers in Artificial Intelligence and Applications 372, 1938–1945. [doi:10.3233/FAIA230484](https://doi.org/10.3233/FAIA230484)
- Sikder, M. F. (2026). FairCert: Certifiable Error Rate Fairness for ML and LLM Decision Systems. *Proceedings of the European Conference on Algorithmic Fairness*, PMLR 350, 8–23. [PMLR](https://proceedings.mlr.press/v350/sikder26a.html)
- Sikder, M. F., Ramachandranpillai, R., de Leng, D., & Heintz, F. (2024). FairX: A comprehensive benchmarking tool for model analysis using fairness, utility, and explainability. *Fairness and Bias in AI 2024 (AEQUITAS 2024), co-located with ECAI 2024*, CEUR Workshop Proceedings, Vol. 3808. [Paper](https://ceur-ws.org/Vol-3808/paper16.pdf) · [arXiv:2406.14281](https://arxiv.org/abs/2406.14281)
- Sikder, M. F., Ramachandranpillai, R., de Leng, D., & Heintz, F. (2025). Promoting Intersectional Fairness Through Knowledge Distillation. *ECAI 2025*, Frontiers in Artificial Intelligence and Applications 413, 3427–3434. [doi:10.3233/FAIA251214](https://doi.org/10.3233/FAIA251214)
- Suresh, H., & Guttag, J. (2021). A Framework for Understanding Sources of Harm throughout the Machine Learning Life Cycle. *Equity and Access in Algorithms, Mechanisms, and Optimization (EAAMO '21)*. [doi:10.1145/3465416.3483305](https://doi.org/10.1145/3465416.3483305)
- van Breugel, B., Kyono, T., Berrevoets, J., & van der Schaar, M. (2021). DECAF: Generating Fair Synthetic Data Using Causally-Aware Generative Networks. *Advances in Neural Information Processing Systems*, 34, 22221–22233. [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2021/hash/ba9fab001f67381e56e410575874d967-Abstract.html)
- Wachter, S., Mittelstadt, B., & Russell, C. (2021). Bias Preservation in Machine Learning: The Legality of Fairness Metrics Under EU Non-Discrimination Law. *West Virginia Law Review*, 123(3), 735. [WVU Research Repository](https://researchrepository.wvu.edu/wvlr/vol123/iss3/4)
- Wang, T., Zhao, J., Yatskar, M., Chang, K.-W., & Ordonez, V. (2019). Balanced Datasets Are Not Enough: Estimating and Mitigating Gender Bias in Deep Image Representations. *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, 5310–5319. [CVF Open Access](https://openaccess.thecvf.com/content_ICCV_2019/html/Wang_Balanced_Datasets_Are_Not_Enough_Estimating_and_Mitigating_Gender_Bias_ICCV_2019_paper.html)
- Weerts, H., Dudík, M., Edgar, R., Jalali, A., Lutz, R., & Madaio, M. (2023). Fairlearn: Assessing and Improving Fairness of AI Systems. *Journal of Machine Learning Research*, 24(257), 1–8. [JMLR](https://jmlr.org/papers/v24/23-0389.html)
- Wyllie, S., Shumailov, I., & Papernot, N. (2024). Fairness Feedback Loops: Training on Synthetic Data Amplifies Bias. *Proceedings of the 2024 ACM Conference on Fairness, Accountability, and Transparency*, 2113–2147. [doi:10.1145/3630106.3659029](https://doi.org/10.1145/3630106.3659029)
- Xu, D., Yuan, S., Zhang, L., & Wu, X. (2018). FairGAN: Fairness-aware Generative Adversarial Networks. *2018 IEEE International Conference on Big Data*, 570–575. [doi:10.1109/BigData.2018.8622525](https://doi.org/10.1109/BigData.2018.8622525)

[Lab 2: Utility and fairness evaluation](../../04-labs/lab-2/) follows this lecture in the same week. There you evaluate synthetic data with fairlearn and FairX and log the energy use of training with CodeCarbon.
