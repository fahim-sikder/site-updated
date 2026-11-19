---
title: "Lab 2: Utility evaluation"
linkTitle: "Lab 2: Utility"
weight: 42
---

**Week 5** · 2 hours · Learning outcome [LO2](../../01-about/#learning-outcomes)

## Goal

You evaluate the synthetic Adult data from Lab 1 for utility and fidelity. You use three families of metrics: the AUROC, accuracy and F1 score of classifiers trained on synthetic data and tested on real data (and the reverse), the sample-level metrics of Alaa et al. (2022), and the utility and fidelity metrics of FairX. Two reference data sets that the script builds, a copy of the training data and a table of independently sampled columns, show where the metrics agree and where they disagree.

## Learning outcomes

The lab supports [LO2](../../01-about/#learning-outcomes): evaluate synthetic data from an existing generative model for utility, privacy and fairness. This lab covers utility; Labs 3 and 4 cover privacy and fairness. After the lab you should be able to:

- run TSTR and TRTS evaluations with a real holdout set and read them correctly;
- compute alpha-precision, beta-recall and authenticity, and explain what each one measures;
- explain why two metrics, or two implementations of the same metric, can rank the same synthetic data sets differently.

## Before the lab

- Attend or review [Lecture 4](../../03-lectures/lecture-4/), which runs earlier the same week.
- Read Sections 1 to 3 of Alaa et al. (2022), listed under [Further reading](#further-reading).
- Complete [Lab 1](../lab-1/). This lab reads `adult_train.csv`, `adult_holdout.csv`, `synthetic_ctgan.csv` and `synthetic_tvae.csv` from the Lab 1 folder `outputs/`.

## Set-up

Use the course environment from the [Labs](../#set-up) page. Download [lab2_utility.py](lab2_utility.py) into a folder next to your Lab 1 folder, for example:

```text
labs/
  lab-1/
    outputs/          from Lab 1
  lab-2/
    lab2_utility.py
```

Run the commands below from the `lab-2` folder. If your Lab 1 output is somewhere else, pass its path with `--data-dir`.

## Tasks

{{% steps %}}

### Run the evaluation

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

The script computes alpha-precision, beta-recall and authenticity (Alaa et al., 2022) twice: with synthcity's `alpha_precision` metric and with FairX's `SyntheticEvaluation`. Both embed the data with a one-class network before they compute the scores:

```python
from synthcity.metrics import Metrics

result = Metrics.evaluate(
    X_gt=train, X_syn=df, metrics={"stats": ["alpha_precision"]},
    random_state=seed, use_cache=False,
)
```

```python
from fairx.dataset import CustomDataClass
from fairx.metrics import DataUtilsMetrics, SyntheticEvaluation

real_module = CustomDataClass(str(train_csv), "sex", [TARGET])
syn_module = CustomDataClass(str(syn_csv), "sex", [TARGET])
fidelity = SyntheticEvaluation(real_module, syn_module, use_cache=False).calculate_alpha_precision()
```

synthcity reports the integrated scores as `delta_precision_alpha_OC` and `delta_coverage_beta_OC`. The script prints the full table and saves it as `outputs_lab2/fidelity.csv`. Our run gave (rounded, with shorter row names):

| Metric | CTGAN | TVAE | copy | marginals | real holdout |
|---|---:|---:|---:|---:|---:|
| synthcity alpha-precision | 0.143 | 0.368 | 1.000 | 0.837 | 0.983 |
| synthcity beta-recall | 0.040 | 0.055 | 1.000 | 0.356 | 0.529 |
| synthcity authenticity | 0.731 | 0.764 | 0.000 | 0.559 | 0.508 |
| FairX alpha-precision | 0.094 | 0.045 | 1.000 | 0.386 | 0.420 |
| FairX beta-recall | 0.037 | 0.003 | 1.000 | 0.040 | 0.130 |
| FairX authenticity | 0.860 | 0.998 | 0.000 | 0.792 | 0.845 |
| FairX XGB accuracy | 0.762 | 0.785 | 0.847 | 0.743 |  |
| FairX XGB F1 | 0.434 | 0.586 | 0.675 | 0.117 |  |
| FairX XGB AUROC | 0.629 | 0.725 | 0.774 | 0.520 |  |

The real holdout set has no FairX XGB values, because it cannot be the training set and the test set at once.

### Read the FairX utility metrics

FairX's `DataUtilsMetrics` trains an XGBoost classifier on the first part of a split and tests it on the second part. The script passes the synthetic data as the training part and the real holdout as the test part, so the "FairX XGB" rows in the table above come from a third TSTR evaluation:

```python
split = (X_syn, X_hold, y_syn, y_hold, df["sex"].to_numpy(), holdout["sex"].to_numpy())
out.update({f"FairX XGB {k}": v for k, v in DataUtilsMetrics(split).evaluate_utility().items()})
```

Open `fairx/metrics/datautil/main_utils.py` in your environment and find how FairX computes its `Auroc`. Compare FairX's AUROC with the TSTR AUROC of the random forest and the logistic regression.

### Rank the data sets

Rank CTGAN, TVAE, copy and marginals by each metric in turn. Note every pair of metrics that disagree on the order, and the data set that causes the disagreement.

{{% /steps %}}

## Questions for your lab notes

1. Which metrics rank "copy" as the best data set, and which metric flags it? What does this mean for model selection when you tune a generator on utility metrics alone?
2. In our run, "marginals" had a higher alpha-precision and beta-recall (synthcity) than CTGAN and TVAE, but the lowest TSTR AUROC. Explain how both results can be true, using the definitions in Alaa et al. (2022) and the embedding the implementation uses.
3. TRTS can be higher for a synthetic data set than for the real data. Find a case in your table and explain what it says about that synthetic data. Why do we treat TSTR, not TRTS, as the main utility measure?
4. synthcity and FairX implement the same three metrics, partly from the same code, yet give different numbers for the same data. Find at least two differences in what they do before they compute the scores, for example in encoding, in the columns they include or in the rows they keep. What should a paper report so that a reader can reproduce a value of alpha-precision?
5. FairX computes AUROC from predicted labels. What does an AUROC computed from hard labels equal for a binary classifier, and why is it usually lower than the AUROC from predicted probabilities?
6. You may use only one number to choose between two generators for a downstream classification task in your own research. Which number would you pick, which held-out data would you compute it on, and what would you report next to it?

## Energy use

The script tracks the whole evaluation with one `OfflineEmissionsTracker` and writes `outputs_lab2/emissions.csv`. Our evaluation used 1.21 Wh in 64 s, measured inside the script.

**Question.** Compare the energy of the evaluation with the energy of training CTGAN and TVAE in Lab 1 (`lab-1/outputs/emissions.csv`). Which steps of the evaluation use most of the time? Would it change the balance if you evaluated every checkpoint of a training run, as early stopping on a fidelity metric does?

## Completing the lab

Completing all four labs is part of the [examination](../../07-examination/). As evidence for this lab, the course leader may ask for short lab notes: your answers to the questions above, with the tables they refer to, and the energy figures from `emissions.csv`. Follow the course leader's instructions for the format and the deadline.

## Further reading

- Alaa, A., van Breugel, B., Saveliev, E. S., & van der Schaar, M. (2022). How Faithful is your Synthetic Data? Sample-level Metrics for Evaluating and Auditing Generative Models. *Proceedings of the 39th International Conference on Machine Learning*, PMLR 162, 290–306. [Proceedings page](https://proceedings.mlr.press/v162/alaa22a.html)
- Sikder, M. F., Ramachandranpillai, R., de Leng, D., & Heintz, F. (2024). FairX: A comprehensive benchmarking tool for model analysis using fairness, utility, and explainability. *Proceedings of the 2nd Workshop on Fairness and Bias in AI (AEQUITAS 2024), co-located with ECAI 2024*, CEUR Workshop Proceedings, Vol. 3808. [PDF](https://ceur-ws.org/Vol-3808/paper16.pdf)
- Qian, Z., Davis, R., & van der Schaar, M. (2023). Synthcity: a benchmark framework for diverse use cases of tabular synthetic data. *Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track*. [Proceedings page](https://papers.nips.cc/paper_files/paper/2023/hash/09723c9f291f6056fd1885081859c186-Abstract-Datasets_and_Benchmarks.html)
- Xu, L., Skoularidou, M., Cuesta-Infante, A., & Veeramachaneni, K. (2019). Modeling Tabular data using Conditional GAN. *Advances in Neural Information Processing Systems 32 (NeurIPS 2019)*. [arXiv:1907.00503](https://arxiv.org/abs/1907.00503)
