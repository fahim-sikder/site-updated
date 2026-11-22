---
title: "Lab 2: Utility and fairness evaluation of synthetic data"
linkTitle: "Lab 2: Utility and fairness"
weight: 42
---

**2 hours** · Learning outcomes [ILO2 and ILO3](../../01-about/#learning-outcomes)

## Goal

You evaluate the synthetic Adult data from Lab 1 in two parts. In the first part you measure utility and fidelity: the AUROC, accuracy and F1 score of classifiers trained on synthetic data and tested on real data (and the reverse), and the sample-level metrics of Alaa et al. (2022). Two reference data sets that the script builds, a copy of the training data and a table of independently sampled columns, show where the metrics agree and where they disagree. In the second part you test whether the synthetic data carry or amplify the bias in the real data: you compare group sizes and base rates for the protected attributes sex and race, measure the fairness of classifiers trained on each data set, and repeat the analysis for intersections of sex and race. You end by noting the fairness risks of releasing the data, which you use in the release assessment of [Lab 3](../lab-3/).

## Learning outcomes

The lab supports [ILO2](../../01-about/#learning-outcomes), evaluate synthetic data for utility, privacy and fairness, and prepares [ILO3](../../01-about/#learning-outcomes), assess whether a synthetic data set can be released. This lab covers utility and fairness; [Lab 3](../lab-3/) covers privacy. After the lab you should be able to:

- run TSTR and TRTS evaluations with a real holdout set and read them correctly;
- compute alpha-precision, beta-recall and authenticity, and explain what each one measures;
- explain why two metrics can rank the same synthetic data sets differently;
- measure demographic parity and equalised odds of a classifier trained on synthetic data, on real data;
- run an intersectional analysis and judge whether its groups are large enough to support a conclusion.

Throughout the course, fairness means algorithmic fairness: whether a model's decisions, or the data it learns from, treat groups defined by protected attributes differently.

## Before the lab

- Attend or review [Lecture 4](../../03-lectures/lecture-4/) on fidelity and utility and [Lecture 6](../../03-lectures/lecture-6/) on fairness.
- Read Sections 1 to 3 of Alaa et al. (2022), listed under [Further reading](#further-reading).
- Complete [Lab 1](../lab-1/). This lab reads `adult_train.csv`, `adult_holdout.csv`, `synthetic_ctgan.csv` and `synthetic_tvae.csv` from the Lab 1 folder `outputs/`.

## Set-up

Use the course environment from the [Labs](../#set-up) page. Download the scripts for this lab into a folder `lab-2` next to your Lab 1 folder:

- [lab2_utility.py](lab2_utility.py) evaluates utility and fidelity (part 1).
- [lab2_fairness.py](lab2_fairness.py) compares base rates, downstream fairness and intersectional groups (part 2).
- [lab2_tabfairgan.py](lab2_tabfairgan.py) trains TabFairGAN with FairX. You need it only for the [optional extras](#optional-extras).

```text
labs/
  lab-1/
    outputs/          from Lab 1
  lab-2/
    lab2_utility.py
    lab2_fairness.py
    lab2_tabfairgan.py
```

Run the commands below from the `lab-2` folder. If your Lab 1 output is somewhere else, pass its path with `--data-dir`.

## Tasks

{{% steps %}}

### Part 1: run the utility evaluation

```bash
python lab2_utility.py --data-dir ../lab-1/outputs
```

The script evaluates six data sets against the real training rows. "real" (in the TSTR table) and "real holdout" (in the fidelity table) are real data and serve as references. "CTGAN" and "TVAE" come from Lab 1. "copy" is the training data itself, a generator that memorises perfectly. "marginals" samples every column independently from the training data, so each column has the right distribution but the columns carry no relation to each other. On our test machine the evaluation took about 1 minute (70 s) and wrote `tstr_trts.csv` and `fidelity.csv` to `outputs_lab2/`.

### Read the TSTR and TRTS table

For every data set, the script trains a logistic regression and a random forest to predict income `>50K`:

```python
syn_model = classifiers(seed)[clf_name].fit(X_syn, y_syn)
row = {"data": name, "classifier": clf_name}
row.update({f"TSTR {k}": v for k, v in scores(syn_model, X_hold, y_hold).items()})
row.update({f"TRTS {k}": v for k, v in scores(real_model, X_syn, y_syn).items()})
```

Here the script trains `syn_model` on synthetic data and tests it on the real holdout set (TSTR). It trains `real_model` on the real training data and tests it on the synthetic data (TRTS).

All data sets share one encoder (one-hot categories and standardised numbers) fitted on the real training data, and the real holdout set never takes part in training. Our run printed:

```text
     data          classifier  TSTR AUROC  TSTR accuracy  TSTR F1  TRTS AUROC  TRTS accuracy  TRTS F1
     real logistic regression       0.898          0.843    0.658       0.901          0.842    0.655
    CTGAN logistic regression       0.803          0.756    0.531       0.626          0.664    0.187
     TVAE logistic regression       0.825          0.778    0.597       0.935          0.868    0.711
     copy logistic regression       0.898          0.843    0.658       0.901          0.842    0.655
marginals logistic regression       0.599          0.747    0.002       0.515          0.710    0.140
     real       random forest       0.903          0.847    0.658       0.931          0.863    0.689
    CTGAN       random forest       0.807          0.769    0.502       0.640          0.679    0.144
     TVAE       random forest       0.853          0.799    0.604       0.934          0.869    0.713
     copy       random forest       0.903          0.847    0.658       0.931          0.863    0.689
marginals       random forest       0.585          0.747    0.000       0.516          0.726    0.102
```

Compare the TSTR AUROC of each data set with the "real" row, which is the train-on-real, test-on-real baseline. Then compare TSTR with TRTS for the same data set.

### Read the sample-level metrics

The script computes alpha-precision, beta-recall and authenticity (Alaa et al., 2022) with synthcity's `alpha_precision` metric, which embeds the data with a one-class network before it computes the scores:

```python
from synthcity.metrics import Metrics

result = Metrics.evaluate(
    X_gt=train, X_syn=df, metrics={"stats": ["alpha_precision"]},
    random_state=seed, use_cache=False,
)
```

synthcity reports the integrated scores as `delta_precision_alpha_OC` and `delta_coverage_beta_OC`. The script prints the full table, which also holds FairX's version of the same metrics (see the [optional extras](#optional-extras)), and saves it as `outputs_lab2/fidelity.csv`. Our run gave (rounded, with shorter row names):

| Metric | CTGAN | TVAE | copy | marginals | real holdout |
|---|---:|---:|---:|---:|---:|
| synthcity alpha-precision | 0.143 | 0.368 | 1.000 | 0.837 | 0.983 |
| synthcity beta-recall | 0.040 | 0.055 | 1.000 | 0.356 | 0.529 |
| synthcity authenticity | 0.731 | 0.764 | 0.000 | 0.559 | 0.508 |

Rank CTGAN, TVAE, copy and marginals by each metric in turn, including the TSTR AUROC. Note every pair of metrics that disagree on the order, and the data set that causes the disagreement.

### Part 2: compare group sizes and base rates

```bash
python lab2_fairness.py --data-dir ../lab-1/outputs
```

The first table shows, for each group of `sex` and `race`, its share of the rows and the share of its rows with income `>50K`, in the real training data and in each synthetic data set. In our run, TVAE generated rows for one race group only (White). CTGAN doubled or tripled the share of the three smallest race groups and changed their income rates: for the group Amer-Indian-Eskimo, the share with income `>50K` rose from 0.049 in the real data to 0.422. On our test machine the whole script took 20 s and wrote its tables to `outputs_lab2_fairness/`.

### Measure downstream fairness

The script then trains a logistic regression on each data set and evaluates it on the real holdout set, with fairlearn:

```python
model = LogisticRegression(max_iter=2000).fit(X, y)
proba = model.predict_proba(X_hold)[:, 1]
pred = (proba >= 0.5).astype(int)
```

```python
for attr in PROTECTED:
    s = holdout[attr]
    row[f"DPD {attr}"] = demographic_parity_difference(y_hold, pred, sensitive_features=s)
    row[f"EOD {attr}"] = equalized_odds_difference(y_hold, pred, sensitive_features=s)
```

The demographic parity difference (DPD) is the largest gap in selection rate between groups. For the equalised odds difference (EOD), fairlearn takes the largest gap in true positive rate and the largest gap in false positive rate, and reports the larger of the two. Both are 0 for a classifier that meets the criterion exactly. Our run printed:

```text
            accuracy  AUROC  DPD sex  EOD sex  DPD race  EOD race
trained on                                                      
real           0.843  0.898    0.203    0.177     0.286     0.689
CTGAN          0.756  0.803    0.364    0.502     0.362     0.714
TVAE           0.778  0.825    0.294    0.300     0.297     0.622
```

### Look at intersections of sex and race

The last table gives, for every combination of sex and race in the holdout set, the number of rows `n`, the selection rate and the true positive rate (TPR) of each classifier:

```python
mf = MetricFrame(
    metrics={"n": count, "selection rate": selection_rate, "TPR": true_positive_rate},
    y_true=y_hold, y_pred=pred, sensitive_features=holdout[["sex", "race"]],
)
```

Our run printed:

```text
real: largest gap in selection rate over sex x race groups = 0.396
CTGAN: largest gap in selection rate over sex x race groups = 0.538
TVAE: largest gap in selection rate over sex x race groups = 0.527
                             real                         CTGAN                          TVAE                      
                                n selection rate    TPR       n selection rate    TPR       n selection rate    TPR
sex    race                                                                                                        
Female Amer-Indian-Eskimo    19.0          0.053  0.500    19.0          0.053  0.500    19.0          0.053  0.500
       Asian-Pac-Islander    42.0          0.119  0.800    42.0          0.048  0.200    42.0          0.143  0.800
       Black                214.0          0.065  0.588   214.0          0.014  0.059   214.0          0.089  0.412
       Other                 16.0          0.000  0.000    16.0          0.000  0.000    16.0          0.000  0.000
       White               1328.0          0.070  0.424  1328.0          0.023  0.121  1328.0          0.102  0.382
Male   Amer-Indian-Eskimo    26.0          0.000  0.000    26.0          0.462  0.800    26.0          0.462  0.600
       Asian-Pac-Islander    91.0          0.396  0.675    91.0          0.538  0.750    91.0          0.527  0.825
       Black                235.0          0.128  0.500   235.0          0.157  0.310   235.0          0.196  0.524
       Other                 30.0          0.067  0.000    30.0          0.033  0.000    30.0          0.167  0.250
       White               2999.0          0.285  0.634  2999.0          0.402  0.632  2999.0          0.406  0.699
```

Look at the column `n` before you read the rates. Some groups have fewer than 20 people in the holdout set.

### Note the fairness risks

Choose CTGAN or TVAE, and imagine a research group plans to publish its data so that others can train income classifiers. Write a few lines that cover: which groups the data under-represent or misrepresent; how a classifier trained on it changes DPD and EOD compared with real data; and which intersectional groups are too small to evaluate. Keep these notes: in [Lab 3](../lab-3/) you combine them with the privacy results into one release assessment.

{{% /steps %}}

## Questions for your lab notes

1. Which metrics rank "copy" as the best data set, and which metric flags it? What does this mean for model selection when you tune a generator on utility metrics alone?
2. In our run, "marginals" had a higher alpha-precision and beta-recall than CTGAN and TVAE, but the lowest TSTR AUROC. Explain how both results can be true, using the definitions in Alaa et al. (2022) and the embedding the implementation uses.
3. TRTS can be higher for a synthetic data set than for the real data. Find a case in your table and explain what it says about that synthetic data. Why do we treat TSTR, not TRTS, as the main utility measure?
4. Compare `P(>50K | group)` in the real and synthetic data with the DPD of the classifiers trained on them. Does a gap in the data always turn into a gap in the classifier, and can a classifier show a larger gap than the data it learned from?
5. In our run, TVAE generated no rows for four of the five race groups. What do the fairness metrics for race report for TVAE, and why is that number not evidence that TVAE data are fair? What should an evaluation report when a group is missing from the synthetic data?
6. Use the column `n` of the intersectional table. Which groups would you leave out of a conclusion, and on what grounds? Kearns et al. (2018) and Buolamwini and Gebru (2018) argue for subgroup evaluation; how do they deal with small groups?
7. You may use only one number to choose between two generators for a downstream classification task in your own research. Which number would you pick, which held-out data would you compute it on, and what would you report next to it? Would you also report a fairness number, and which one?

## Optional extras {#optional-extras}

These tasks go deeper into the tools and the methods. Do them if you finish early, or if they matter for your project.

### Compare FairX with synthcity and fairlearn

`lab2_utility.py` also computes the sample-level metrics with FairX's `SyntheticEvaluation`, which FairX adapted from synthcity, and a third TSTR evaluation with FairX's `DataUtilsMetrics`, which trains an XGBoost classifier on the synthetic data and tests it on the real holdout set:

```python
from fairx.dataset import CustomDataClass
from fairx.metrics import DataUtilsMetrics, SyntheticEvaluation

real_module = CustomDataClass(str(train_csv), "sex", [TARGET])
syn_module = CustomDataClass(str(syn_csv), "sex", [TARGET])
fidelity = SyntheticEvaluation(real_module, syn_module, use_cache=False).calculate_alpha_precision()

split = (X_syn, X_hold, y_syn, y_hold, df["sex"].to_numpy(), holdout["sex"].to_numpy())
out.update({f"FairX XGB {k}": v for k, v in DataUtilsMetrics(split).evaluate_utility().items()})
```

Our run gave these FairX rows in `fidelity.csv`. The real holdout set has no FairX XGB values, because it cannot be the training set and the test set at once.

| Metric | CTGAN | TVAE | copy | marginals | real holdout |
|---|---:|---:|---:|---:|---:|
| FairX alpha-precision | 0.094 | 0.045 | 1.000 | 0.386 | 0.420 |
| FairX beta-recall | 0.037 | 0.003 | 1.000 | 0.040 | 0.130 |
| FairX authenticity | 0.860 | 0.998 | 0.000 | 0.792 | 0.845 |
| FairX XGB accuracy | 0.762 | 0.785 | 0.847 | 0.743 |  |
| FairX XGB F1 | 0.434 | 0.586 | 0.675 | 0.117 |  |
| FairX XGB AUROC | 0.629 | 0.725 | 0.774 | 0.520 |  |

`lab2_fairness.py` also reports FairX's fairness criteria, as ratios (smallest group rate divided by largest, 1 is equal), for an XGBoost classifier and the protected attribute `sex`:

```python
from fairx.metrics import FairnessUtils

split = (X, X_hold, y, y_hold, df["sex"].to_numpy(), holdout["sex"].to_numpy())
rows.append({"trained on": name, **FairnessUtils(split).evaluate_fairness()})
```

```text
            Demographic Parity Ratio  Equalized Odd Ratio
trained on                                               
real                           0.304                0.253
CTGAN                          0.094                0.075
TVAE                           0.187                0.137
```

1. synthcity and FairX implement the same three sample-level metrics, partly from the same code, yet give different numbers for the same data. Find at least two differences in what they do before they compute the scores, for example in encoding, in the columns they include or in the rows they keep. What should a paper report so that a reader can reproduce a value of alpha-precision?
2. Open `fairx/metrics/datautil/main_utils.py` in your environment and find how FairX computes its `Auroc`. What does an AUROC computed from hard labels equal for a binary classifier, and why is it usually lower than the AUROC from predicted probabilities?
3. fairlearn and FairX measure the same fairness criteria, as differences and as ratios, with different classifiers. Can the two rank the data sets differently? Which form would you report, and why?

### Remove the protected attributes

Run the fairness analysis again with classifiers that do not see `sex` and `race`:

```bash
python lab2_fairness.py --data-dir ../lab-1/outputs --drop-protected --out outputs_lab2_unaware
```

Compare DPD and EOD with the first run. In our run, the DPD for sex of the classifier trained on real data went from 0.203 to 0.199, and that of the classifier trained on CTGAN data from 0.364 to 0.245.

**Question.** Removing `sex` and `race` from the input did not remove the disparities in our run. Which other columns can carry the same information in Adult? What does this say about fairness through unawareness as a release strategy for synthetic data?

### Train a fair generative model with FairX

TabFairGAN (Rajabi and Garibay, 2022) is a Wasserstein GAN with a second training phase. In FairX, the last 10 epochs add a term to the generator loss that rewards equal rates of the desired label (`>50K`) for the two groups of one binary protected attribute (`sex`) in the generated rows. FairX trains it on the full Adult data, which it loads from OpenML:

```bash
python lab2_tabfairgan.py --epochs 15
```

The script runs the FairX example from its README inside a CodeCarbon tracker:

```python
data_module = BaseDataClass("Adult-Income", "sex", attach_target=True)
tabfairgan = TabFairGAN("Female", ">50K")  # the underprivileged group and the desired label
tabfairgan.fit(data_module, batch_size=256, epochs=args.epochs)
```

On our test machine the TabFairGAN training took 134 s, and the whole script 151 s. FairX printed its own alpha-precision, beta-recall and authenticity for the generated data (0.836, 0.480 and 0.549) and saved 32,561 synthetic rows. In our run, the TabFairGAN data reversed the gap between the sexes: 47.9% of the women and 14.4% of the men had income `>50K`, against 12.6% and 30.5% in the real training data. Then add the TabFairGAN data to the comparison:

```bash
python lab2_fairness.py --data-dir ../lab-1/outputs --extra outputs_lab2_tabfairgan/synthetic_tabfairgan.csv --out outputs_lab2_tfg
```

> [!WARNING] Overlap with the holdout set
> FairX trains TabFairGAN on a random 90% of all 48,842 Adult rows, so most rows of our holdout set were in its training data. Its TSTR numbers on our holdout set are therefore optimistic, and you should compare its fairness numbers, not its accuracy, with the other models.

**Question.** TabFairGAN targets demographic parity in the generated data, for one binary protected attribute and one desired label. Which criterion did it improve, for which attribute, and what happened to the other attribute and to the intersections? What does this suggest about choosing the fairness target before you generate data?

## Energy use

Each script tracks its work with `OfflineEmissionsTracker(country_iso_code="SWE")` and writes `emissions.csv` to its output folder. Our utility evaluation used 1.21 Wh in 64 s and our fairness evaluation 0.21 Wh in 14 s, measured inside the scripts. TabFairGAN, in the optional extras, used 2.42 Wh in 134 s.

**Question.** Compare the energy of the two evaluations with the energy of training CTGAN and TVAE in Lab 1 (`lab-1/outputs/emissions.csv`). Which steps of the evaluation use most of the time? Would it change the balance if you evaluated every checkpoint of a training run, as early stopping on a fidelity metric does?

## Completing the lab

Completing all three labs is part of the [examination](../../07-examination/). As evidence for this lab, the examiner may ask for short lab notes: your answers to the questions above, with the tables they refer to, your notes on the fairness risks, and the energy figures from `emissions.csv`. Follow the examiner's instructions for the format and the deadline.

## Further reading

- Alaa, A., van Breugel, B., Saveliev, E. S., & van der Schaar, M. (2022). How Faithful is your Synthetic Data? Sample-level Metrics for Evaluating and Auditing Generative Models. *Proceedings of the 39th International Conference on Machine Learning*, PMLR 162, 290–306. [Proceedings page](https://proceedings.mlr.press/v162/alaa22a.html)
- Sikder, M. F., Ramachandranpillai, R., de Leng, D., & Heintz, F. (2024). FairX: A comprehensive benchmarking tool for model analysis using fairness, utility, and explainability. *Proceedings of the 2nd Workshop on Fairness and Bias in AI (AEQUITAS 2024), co-located with ECAI 2024*, CEUR Workshop Proceedings, Vol. 3808. [PDF](https://ceur-ws.org/Vol-3808/paper16.pdf)
- Qian, Z., Davis, R., & van der Schaar, M. (2023). Synthcity: a benchmark framework for diverse use cases of tabular synthetic data. *Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track*. [Proceedings page](https://papers.nips.cc/paper_files/paper/2023/hash/09723c9f291f6056fd1885081859c186-Abstract-Datasets_and_Benchmarks.html)
- Xu, L., Skoularidou, M., Cuesta-Infante, A., & Veeramachaneni, K. (2019). Modeling Tabular data using Conditional GAN. *Advances in Neural Information Processing Systems 32 (NeurIPS 2019)*. [arXiv:1907.00503](https://arxiv.org/abs/1907.00503)
- Hardt, M., Price, E., & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29 (NIPS 2016)*. [Proceedings page](https://papers.nips.cc/paper_files/paper/2016/hash/6a9659feb1216f14f7384ba499518b38-Abstract.html)
- Buolamwini, J., & Gebru, T. (2018). Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *Proceedings of the 1st Conference on Fairness, Accountability and Transparency*, PMLR 81, 77–91. [Proceedings page](https://proceedings.mlr.press/v81/buolamwini18a.html)
- Kearns, M., Neel, S., Roth, A., & Wu, Z. S. (2018). Preventing Fairness Gerrymandering: Auditing and Learning for Subgroup Fairness. *Proceedings of the 35th International Conference on Machine Learning*, PMLR 80, 2564–2572. [Proceedings page](https://proceedings.mlr.press/v80/kearns18a.html)
- Rajabi, A., & Garibay, O. O. (2022). TabFairGAN: Fair Tabular Data Generation with Generative Adversarial Networks. *Machine Learning and Knowledge Extraction*, 4(2), 488–501. [doi:10.3390/make4020022](https://doi.org/10.3390/make4020022)
- Weerts, H., Dudík, M., Edgar, R., Jalali, A., Lutz, R., & Madaio, M. (2023). Fairlearn: Assessing and Improving Fairness of AI Systems. *Journal of Machine Learning Research*, 24(257), 1–8. [JMLR page](https://jmlr.org/papers/v24/23-0389.html)
