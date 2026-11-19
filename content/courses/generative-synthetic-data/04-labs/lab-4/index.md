---
title: "Lab 4: Fairness evaluation"
linkTitle: "Lab 4: Fairness"
weight: 44
---

**Week 7** · 2 hours · Learning outcomes [LO2 and LO3](../../01-about/#learning-outcomes)

## Goal

You test whether synthetic data carries or amplifies the bias in the real data. First you compare group sizes and base rates for the protected attributes sex and race in real and synthetic Adult data. Then you train classifiers on each data set, measure their fairness on real holdout data and repeat the analysis for intersections of sex and race. You also train one fair generative model from FairX. The lab ends with a short assessment of the fairness risks of releasing a synthetic data set.

## Learning outcomes

The lab supports [LO2 and LO3](../../01-about/#learning-outcomes). After the lab you should be able to:

- measure demographic parity and equalised odds of a classifier trained on synthetic data, on real data, with fairlearn and FairX;
- run an intersectional analysis and judge whether its groups are large enough to support a conclusion;
- assess and document the fairness risks of releasing a synthetic data set.

Throughout the course, fairness means algorithmic fairness: whether a model's decisions, or the data it learns from, treat groups defined by protected attributes differently.

## Before the lab

- Attend or review [Lecture 6](../../03-lectures/lecture-6/), which runs earlier the same week.
- Complete [Lab 1](../lab-1/). This lab reads the Lab 1 files in `outputs/`. If you completed [Lab 3](../lab-3/), you can add its private synthetic data to the comparison.

## Set-up

Use the course environment from the [Labs](../#set-up) page. Download the two scripts for this lab into a folder `lab-4` next to your Lab 1 folder:

- [lab4_fairness.py](lab4_fairness.py) compares base rates, downstream fairness and intersectional groups.
- [lab4_tabfairgan.py](lab4_tabfairgan.py) trains TabFairGAN with FairX.

Run the commands below from the `lab-4` folder.

## Tasks

{{% steps %}}

### Compare group sizes and base rates

```bash
python lab4_fairness.py --data-dir ../lab-1/outputs
```

The first table shows, for each group of `sex` and `race`, its share of the rows and the share of its rows with income `>50K`, in the real training data and in each synthetic data set. In our run, TVAE generated rows for one race group only (White). CTGAN doubled or tripled the share of the three smallest race groups and changed their income rates: for the group Amer-Indian-Eskimo, the share with income `>50K` rose from 0.049 in the real data to 0.422. On our test machine the whole script took 20 s.

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

FairX reports the same two criteria as ratios (smallest group rate divided by largest, 1 is equal), for an XGBoost classifier and the protected attribute `sex`:

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

### Remove the protected attributes

Run the analysis again with classifiers that do not see `sex` and `race`:

```bash
python lab4_fairness.py --data-dir ../lab-1/outputs --drop-protected --out outputs_lab4_unaware
```

Compare DPD and EOD with the first run. In our run, the DPD for sex of the classifier trained on real data went from 0.203 to 0.199, and that of the classifier trained on CTGAN data from 0.364 to 0.245.

### Add the private data from Lab 3

If you completed [Lab 3](../lab-3/), add its DPGAN data at ε = 1 to the comparison:

```bash
python lab4_fairness.py --data-dir ../lab-1/outputs --extra ../lab-3/outputs_lab3/synthetic_dpgan_eps1.csv --out outputs_lab4_dp
```

Read the accuracy next to DPD and EOD.

### Train a fair generative model with FairX

TabFairGAN (Rajabi and Garibay, 2022) is a Wasserstein GAN with a second training phase. In FairX, the last 10 epochs add a term to the generator loss that rewards equal rates of the desired label (`>50K`) for the two groups of one binary protected attribute (`sex`) in the generated rows. FairX trains it on the full Adult data, which it loads from OpenML:

```bash
python lab4_tabfairgan.py --epochs 15
```

The script runs the FairX example from its README inside a CodeCarbon tracker:

```python
data_module = BaseDataClass("Adult-Income", "sex", attach_target=True)
tabfairgan = TabFairGAN("Female", ">50K")  # the underprivileged group and the desired label
tabfairgan.fit(data_module, batch_size=256, epochs=args.epochs)
```

On our test machine the TabFairGAN training took 134 s, and the whole script 151 s. FairX printed its own alpha-precision, beta-recall and authenticity for the generated data (0.836, 0.480 and 0.549) and saved 32,561 synthetic rows. In our run, the TabFairGAN data reversed the gap between the sexes: 47.9% of the women and 14.4% of the men had income `>50K`, against 12.6% and 30.5% in the real training data. Then add the TabFairGAN data to the comparison:

```bash
python lab4_fairness.py --data-dir ../lab-1/outputs --extra outputs_lab4/synthetic_tabfairgan.csv --out outputs_lab4_tfg
```

> [!WARNING] Overlap with the holdout set
> FairX trains TabFairGAN on a random 90% of all 48,842 Adult rows, so most rows of our holdout set were in its training data. Its TSTR numbers on our holdout set are therefore optimistic, and you should compare its fairness numbers, not its accuracy, with the other models.

### Write a fairness release assessment

Choose one synthetic data set from this lab or from Lab 3, and imagine a research group plans to publish it so that others can train income classifiers. Write half a page that covers: which groups the data under-represent or misrepresent; how a classifier trained on it changes DPD and EOD compared with real data; which intersectional groups are too small to evaluate; and what you would require, or publish alongside the data, before release.

{{% /steps %}}

## Questions for your lab notes

1. Compare `P(>50K | group)` in the real and synthetic data with the DPD of the classifiers trained on them. Does a gap in the data always turn into a gap in the classifier, and can a classifier show a larger gap than the data it learned from?
2. In our run, TVAE generated no rows for four of the five race groups. What do the fairness metrics for race report for TVAE, and why is that number not evidence that TVAE data are fair? What should an evaluation report when a group is missing from the synthetic data?
3. fairlearn and FairX measure the same criteria, as differences and as ratios, with different classifiers. Can the two rank the data sets differently? Which form would you report, and why?
4. Use the column `n` of the intersectional table. Which groups would you leave out of a conclusion, and on what grounds? Kearns et al. (2018) and Buolamwini and Gebru (2018) argue for subgroup evaluation; how do they deal with small groups?
5. Removing `sex` and `race` from the input did not remove the disparities in our run. Which other columns can carry the same information in Adult? What does this say about fairness through unawareness as a release strategy for synthetic data?
6. TabFairGAN targets demographic parity in the generated data, for one binary protected attribute and one desired label. Which criterion did it improve, for which attribute, and what happened to the other attribute and to the intersections? What does this suggest about choosing the fairness target before you generate data?
7. Link this lab to Lab 3. In our run, the classifier trained on the DPGAN data predicted `>50K` for every person in the holdout set: its DPD and EOD were 0 and its accuracy was 0.253. Why is this classifier not fair in any useful sense? Ganev et al. (2022) report that differential privacy can have a disparate impact on synthetic data. What would you need to test that claim on Adult?

## Energy use

`lab4_fairness.py` tracks its whole evaluation and `lab4_tabfairgan.py` tracks the TabFairGAN training, both with `OfflineEmissionsTracker(country_iso_code="SWE")`. Our evaluation used 0.21 Wh in 14 s and TabFairGAN used 2.42 Wh in 134 s.

**Question.** TabFairGAN trains on about nine times as many rows as the models in Lab 1. Compare its energy per training row with that of CTGAN in Lab 1. If a fairness intervention costs extra training, how would you report that cost next to the fairness gain?

## Completing the lab

Completing all four labs is part of the [examination](../../07-examination/). As evidence for this lab, the course leader may ask for short lab notes: your answers to the questions above, your fairness release assessment, and the energy figures from `emissions.csv`. Follow the course leader's instructions for the format and the deadline.

## Further reading

- Hardt, M., Price, E., & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29 (NIPS 2016)*. [Proceedings page](https://papers.nips.cc/paper_files/paper/2016/hash/6a9659feb1216f14f7384ba499518b38-Abstract.html)
- Buolamwini, J., & Gebru, T. (2018). Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *Proceedings of the 1st Conference on Fairness, Accountability and Transparency*, PMLR 81, 77–91. [Proceedings page](https://proceedings.mlr.press/v81/buolamwini18a.html)
- Kearns, M., Neel, S., Roth, A., & Wu, Z. S. (2018). Preventing Fairness Gerrymandering: Auditing and Learning for Subgroup Fairness. *Proceedings of the 35th International Conference on Machine Learning*, PMLR 80, 2564–2572. [Proceedings page](https://proceedings.mlr.press/v80/kearns18a.html)
- Rajabi, A., & Garibay, O. O. (2022). TabFairGAN: Fair Tabular Data Generation with Generative Adversarial Networks. *Machine Learning and Knowledge Extraction*, 4(2), 488–501. [doi:10.3390/make4020022](https://doi.org/10.3390/make4020022)
- Ganev, G., Oprisanu, B., & De Cristofaro, E. (2022). Robin Hood and Matthew Effects: Differential Privacy Has Disparate Impact on Synthetic Data. *Proceedings of the 39th International Conference on Machine Learning*, PMLR 162, 6944–6959. [Proceedings page](https://proceedings.mlr.press/v162/ganev22a.html)
- Weerts, H., Dudík, M., Edgar, R., Jalali, A., Lutz, R., & Madaio, M. (2023). Fairlearn: Assessing and Improving Fairness of AI Systems. *Journal of Machine Learning Research*, 24(257), 1–8. [JMLR page](https://jmlr.org/papers/v24/23-0389.html)
- Sikder, M. F., Ramachandranpillai, R., de Leng, D., & Heintz, F. (2024). FairX: A comprehensive benchmarking tool for model analysis using fairness, utility, and explainability. *Proceedings of the 2nd Workshop on Fairness and Bias in AI (AEQUITAS 2024), co-located with ECAI 2024*, CEUR Workshop Proceedings, Vol. 3808. [PDF](https://ceur-ws.org/Vol-3808/paper16.pdf)
