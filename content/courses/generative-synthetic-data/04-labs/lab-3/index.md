---
title: "Lab 3: Privacy evaluation"
linkTitle: "Lab 3: Privacy"
weight: 43
---

**Week 6** · 2 hours · Learning outcomes [LO2 and LO3](../../01-about/#learning-outcomes)

## Goal

You train a differentially private generative model at two privacy budgets and measure what the privacy costs in utility. You then evaluate how much the synthetic data reveal about the training rows, with a distance to the closest record and with the DOMIAS membership inference attack, for private and non-private models. The lab ends with a short assessment of the privacy risks of releasing a synthetic data set.

## Learning outcomes

The lab supports [LO2 and LO3](../../01-about/#learning-outcomes). After the lab you should be able to:

- train a differentially private generator and explain what its privacy budget covers and what it does not;
- run a distance-based privacy check and a membership inference attack, and explain why neither proves that data are private;
- assess and document the privacy risks of releasing a synthetic data set.

## Before the lab

- Attend or review [Lecture 5](../../03-lectures/lecture-5/), which runs earlier the same week.
- Complete [Lab 1](../lab-1/). This lab reads the Lab 1 files in `outputs/`: the training, holdout and reference rows and the CTGAN and TVAE data.

## Set-up

Use the course environment from the [Labs](../#set-up) page. Download [lab3_privacy.py](lab3_privacy.py) into a folder `lab-3` next to your Lab 1 folder, and run the commands below from that folder.

The script uses three disjoint sets of 5,000 real rows from Lab 1: the **training** rows that every generator learned from (the members), the **holdout** rows that no generator saw (the non-members), and the **reference** rows, which the attack uses as a sample of the population.

## Tasks

{{% steps %}}

### Train DPGAN at two privacy budgets

```bash
python lab3_privacy.py --data-dir ../lab-1/outputs
```

The script trains synthcity's DPGAN plugin at ε = 1 and ε = 10. DPGAN (Xie et al., 2018) trains the discriminator with differentially private stochastic gradient descent (Abadi et al., 2016). synthcity uses Opacus to clip the gradient of each example and add Gaussian noise. Opacus sets the noise so that the whole training run meets the target ε.

```python
model = Plugins().get(
    "dpgan", epsilon=epsilon, n_iter=n_iter, random_state=seed, device="cpu",
    generator_n_units_hidden=units, discriminator_n_units_hidden=units,
)
model.fit(train)
synthetic = model.generate(count=len(train)).dataframe()
```

We use 100 hidden units per layer instead of the plugin's 500 and 100 training epochs instead of 2,000, because per-example gradients make DP training slow on a CPU. By default the plugin keeps 20% of the training rows aside and checks a detection metric on them every 50 epochs, to stop early and keep the best model. Since δ is not given, synthcity sets it to one over the number of rows it trains on; in our run that was δ ≈ 2.5 × 10<sup>−4</sup>. On our test machine each DPGAN run took about 2.2 minutes (131 s at ε = 1 and 133 s at ε = 10), and the whole script took about 5 minutes (307 s).

> [!NOTE] Why DPGAN
> synthcity also offers the private generators `aim`, `pategan` and `privbayes`. In our tests on these data, `aim` (with the numeric columns cut into a few fixed intervals) returned near-uniform marginals at ε = 1: each of six age bands held about 17% of the rows, against 3% to 26% in the real data. `privbayes` stopped with an error, and we did not use `pategan`. The lab therefore uses DPGAN, which ran without errors. Its output was poor at every budget we tried, as the next task shows.

### Measure the utility cost

The column `TSTR AUROC` of the printed table gives the AUROC on the real holdout set of a logistic regression trained on each data set. The row "real (TRTR)" trains on the real training rows. The script prints the whole table and saves it as `outputs_lab3/privacy_utility.csv`. Our run gave (rounded, with shorter column names):

| Data | TSTR AUROC | Exact copies | Median DCR to train | Median DCR to holdout | Share closer to train | DOMIAS AUROC |
|---|---:|---:|---:|---:|---:|---:|
| CTGAN (no DP) | 0.803 | 0 | 1.472 | 1.477 | 0.482 | 0.502 |
| TVAE (no DP) | 0.825 | 6 | 0.036 | 0.031 | 0.402 | 0.498 |
| copy of train | 0.898 | 5000 | 0.000 | 0.174 | 0.952 | 0.720 |
| DPGAN ε = 1 | 0.744 | 0 | 3.182 | 3.181 | 0.512 | 0.502 |
| DPGAN ε = 10 | 0.341 | 0 | 3.072 | 3.030 | 0.255 | 0.507 |
| real (TRTR) | 0.898 |  |  |  |  |  |

Compare DPGAN at both budgets with the non-private CTGAN and TVAE from Lab 1 and with real data. Then open the DPGAN files in `outputs_lab3/` and look at the rows themselves: in our run, 92% of the DPGAN rows at ε = 1 and 96% at ε = 10 had income `>50K`, against 25% in the real data.

### Distance to the closest record

For every synthetic row, the script finds the closest training row and the closest holdout row, after scaling numeric columns to [0, 1] and one-hot encoding categorical columns:

```python
d_train = NearestNeighbors(n_neighbors=1, algorithm="kd_tree").fit(T).kneighbors(S)[0][:, 0]
d_hold = NearestNeighbors(n_neighbors=1, algorithm="kd_tree").fit(H).kneighbors(S)[0][:, 0]
copies = synthetic.merge(train.drop_duplicates(), how="inner", on=list(train.columns))
```

Read four columns of the table. The first counts the synthetic rows that exactly copy a training row. The next two give the median distance to the closest training row and to the closest holdout row. The last gives the share of synthetic rows that lie closer to a training row than to a holdout row. A generator that does not memorise its training rows should give a share near 0.5, because the training and holdout sets are equally large samples of the same population. The row "copy of train" is the training data itself: a release with no privacy at all.

### Run a membership inference attack

DOMIAS (van Breugel et al., 2023) guesses that a row was in the training data when the synthetic data are denser around it than the population is. It estimates both densities with a Gaussian kernel density estimate and scores each row by their ratio. The script uses synthcity's implementation on 1,000 members (training rows) and 1,000 non-members (holdout rows), with 1,000 reference rows as the population sample:

```python
from synthcity.metrics.eval_privacy import DomiasMIAKDE
result = DomiasMIAKDE(use_cache=False).evaluate(
    X_gt, encode(syn.iloc[:half][keep]), encode(members[keep]), encode(syn.iloc[half:][keep]),
    reference_size=n,
)
```

An AUROC of 0.5 means the attack does no better than a coin flip. A Gaussian kernel density needs every column to vary, so the script leaves out columns that are constant in the synthetic or reference sample and prints their names. In our run, DOMIAS reached an AUROC of 0.72 against the copy of the training data and between 0.49 and 0.51 against every generator. For TVAE the script left out `race` and `native-country`, because TVAE generated a single value in each.

### Change the privacy budget

Train DPGAN at a smaller and a larger budget and write the results to a new folder:

```bash
python lab3_privacy.py --data-dir ../lab-1/outputs --epsilons 0.1 100 --out outputs_lab3_eps
```

On our test machine this took about 6 minutes (369 s). In our run, the TSTR AUROC was 0.480 at ε = 0.1 and 0.459 at ε = 100.

> [!WARNING] DPGAN results change from run to run
> DPGAN gave different data when we ran the same command twice with the same seed on the same machine. In our first run of the default command, the TSTR AUROC was 0.512 at ε = 1 and 0.676 at ε = 10; in the second run, which the table above shows, it was 0.744 and 0.341. Expect your numbers to differ from ours.

### Write a privacy release assessment

Choose one synthetic data set from this lab, and imagine your research group plans to publish it with a paper. Write half a page that covers: what an attacker could learn and about whom; which of your measurements support or weaken that risk, and which risks they cannot rule out; what the formal guarantee covers, if there is one; and whether you would release the data, with which safeguards.

{{% /steps %}}

## Questions for your lab notes

1. How much utility did DPGAN lose at each budget, compared with CTGAN and with real data? In our two runs of the same command, the TSTR AUROC at ε = 1 was 0.512 and 0.744, and at ε = 10 it was 0.676 and 0.341. What do these numbers allow you to conclude about the trade-off between privacy and utility, and what would you need to measure it? Can you separate the cost of privacy from the cost of the smaller network and the short training?
2. For an (ε, δ)-differentially private mechanism, any test that tries to tell two neighbouring data sets apart satisfies TPR ≤ e<sup>ε</sup> · FPR + δ (Kairouz et al., 2015, Theorem 2.1). Compute this bound at FPR = 0.01 for ε = 1 and for ε = 10, with δ = 2.5 × 10<sup>−4</sup> as in our run. Which budget gives a meaningful bound? How do these numbers relate to the DOMIAS AUROC you measured?
3. CTGAN, which has no formal guarantee, gave a distance share near 0.5 and a DOMIAS AUROC near 0.5 in our run. Does this show that its output is safe to release? Use Stadler et al. (2022) and Ganev and De Cristofaro (2025) in your answer.
4. The copy of the training data is the worst possible release, yet in our run the DOMIAS AUROC for it was well below 1 and its distance share was below 1. Explain both numbers. What do they tell you about the power of these tests on Adult?
5. DPGAN at ε = 10 has a formal guarantee, yet in our second run its distance share was 0.255, far from 0.5. In that run, 46% of its rows had the same training row as their nearest neighbour. Why does the share then say little about memorisation? What does this imply for distance checks on synthetic data of low quality?
6. Read `synthcity/plugins/privacy/plugin_dpgan.py`, `synthcity/plugins/core/models/tabular_gan.py` and `gan.py` in your environment. Which steps use the real training rows outside the DP-SGD updates of the discriminator? Look at how the data encoder is fitted and at the default `patience_metric`. What does the ε of DPGAN cover, and what does it not cover?
7. Is synthcity's default δ, one over the number of training rows, small enough? What could a mechanism with δ = 1/n do and still meet the definition?

## Energy use

The script tracks each DPGAN run with `OfflineEmissionsTracker(country_iso_code="SWE")` and writes `outputs_lab3/emissions.csv`. In our run, the two DPGAN runs used 2.20 Wh each.

**Question.** Compare the energy per epoch of DPGAN with that of CTGAN in Lab 1. Where does the extra cost of private training come from? If you had to choose between a smaller ε and a smaller energy budget for your own project, how would you decide?

## Completing the lab

Completing all four labs is part of the [examination](../../07-examination/). As evidence for this lab, the course leader may ask for short lab notes: your answers to the questions above, your privacy release assessment, and the energy figures from `emissions.csv`. Follow the course leader's instructions for the format and the deadline.

## Further reading

- Abadi, M., Chu, A., Goodfellow, I., McMahan, H. B., Mironov, I., Talwar, K., & Zhang, L. (2016). Deep Learning with Differential Privacy. *Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security*, 308–318. [doi:10.1145/2976749.2978318](https://doi.org/10.1145/2976749.2978318)
- Xie, L., Lin, K., Wang, S., Wang, F., & Zhou, J. (2018). Differentially Private Generative Adversarial Network. [arXiv:1802.06739](https://arxiv.org/abs/1802.06739)
- Kairouz, P., Oh, S., & Viswanath, P. (2015). The Composition Theorem for Differential Privacy. *Proceedings of the 32nd International Conference on Machine Learning*, PMLR 37, 1376–1385. [Proceedings page](https://proceedings.mlr.press/v37/kairouz15.html)
- Shokri, R., Stronati, M., Song, C., & Shmatikov, V. (2017). Membership Inference Attacks Against Machine Learning Models. *2017 IEEE Symposium on Security and Privacy*, 3–18. [doi:10.1109/SP.2017.41](https://doi.org/10.1109/SP.2017.41)
- van Breugel, B., Sun, H., Qian, Z., & van der Schaar, M. (2023). Membership Inference Attacks against Synthetic Data through Overfitting Detection. *Proceedings of the 26th International Conference on Artificial Intelligence and Statistics*, PMLR 206, 3493–3514. [Proceedings page](https://proceedings.mlr.press/v206/breugel23a.html)
- Stadler, T., Oprisanu, B., & Troncoso, C. (2022). Synthetic Data – Anonymisation Groundhog Day. *31st USENIX Security Symposium*, 1451–1468. [Proceedings page](https://www.usenix.org/conference/usenixsecurity22/presentation/stadler)
- Ganev, G., & De Cristofaro, E. (2025). The Inadequacy of Similarity-Based Privacy Metrics: Privacy Attacks Against "Truly Anonymous" Synthetic Datasets. *2025 IEEE Symposium on Security and Privacy*, 4007–4025. [doi:10.1109/SP61157.2025.00218](https://doi.org/10.1109/SP61157.2025.00218)
