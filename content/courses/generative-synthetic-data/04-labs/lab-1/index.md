---
title: "Lab 1: Train generative models and find failure modes"
linkTitle: "Lab 1: Failure modes"
weight: 41
---

**Week 4** · 2 hours · Learning outcome [LO1](../../01-about/#learning-outcomes)

## Goal

You train four generative models from three families on the same data and look for their failure modes: what each model gets wrong in the data it produces. CTGAN (a GAN) and TVAE (a variational autoencoder) learn the Adult census table. TimeGAN (a GAN for sequences) and TransFusion (a diffusion model with a transformer) learn a set of sine sequences. You then link each failure you find, such as a missing category or a set of near-identical samples, to the training objective of the model, its training budget or its data encoding.

## Learning outcomes

The lab supports [LO1](../../01-about/#learning-outcomes): analyse how the training objectives of the main families of generative models relate to their failure modes. After the lab you should be able to:

- train tabular and time-series generative models from the command line and log their energy use;
- compare real and synthetic data with marginal plots, differences in pairwise association and 2D projections;
- find failure modes in synthetic data, such as a missing category, a collapsed mode or a set of near-identical samples, and explain each through the model's objective, its training budget or its data encoding.

## Before the lab

- Attend or review [Lecture 2](../../03-lectures/lecture-2/) on VAEs and GANs and [Lecture 3](../../03-lectures/lecture-3/) on diffusion and transformer-based models. [Paper seminar 1](../../05-paper-seminars/#paper-seminar-1-generative-model-families), earlier the same week, covers the same model families.
- Set up the environment as described on the [Labs](../#set-up) page.
- Read the README of [CTGAN](https://github.com/sdv-dev/CTGAN) and of [TransFusion](https://github.com/fahim-sikder/TransFusion).

## Set-up

Download the two scripts for this lab into an empty folder, for example `lab-1`:

- [lab1_tabular.py](lab1_tabular.py) trains CTGAN and TVAE on Adult and compares their output.
- [lab1_timeseries.py](lab1_timeseries.py) trains TimeGAN and TransFusion on sine sequences and compares their output.

The time-series script imports the TransFusion model from its repository. Clone it into the same folder, at the commit we tested:

```bash
git clone https://github.com/fahim-sikder/TransFusion.git
git -C TransFusion checkout 7be6389a083152dfe7067198bc797b3f8bcfd8f9
```

Run every command in this lab from the `lab-1` folder, with the course environment active.

**Data.** The tabular script downloads the Adult data set (Becker and Kohavi, 1996) from [OpenML (data set 1590)](https://www.openml.org/d/1590) through scikit-learn on its first run and caches it in your home folder. The [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/2/adult) publishes Adult under the CC BY 4.0 licence, and OpenML lists it as public. The script drops the census sampling weight `fnlwgt` and the rows with missing values, which leaves 45,222 rows. It then draws three disjoint sets of 5,000 rows with a fixed seed: a training set, a holdout set and a reference set. Labs 2 and 3 reuse these files, so keep the `outputs` folder. The sine sequences are generated in the script with the same recipe as the [TimeGAN code](https://github.com/jsyoon0823/TimeGAN): each of the five features is sin(*f t* + *p*), with *f* and *p* drawn from U(0, 0.1), rescaled to [0, 1].

> [!NOTE] Our test machine
> We ran every command on this page on a desktop PC with an AMD Ryzen 5 5500 CPU (6 cores) and 32 GB RAM, under Windows 11, with CPU-only PyTorch. The run times we report come from that machine. A laptop may take longer; every script has arguments that make the runs smaller.

## Tasks

{{% steps %}}

### Train CTGAN and TVAE

Run the tabular script with 100 training epochs for each model:

```bash
python lab1_tabular.py --epochs 100
```

The script trains both models on the 5,000 training rows, samples 5,000 synthetic rows from each, and writes everything to `outputs/`: the three data splits, `synthetic_ctgan.csv`, `synthetic_tvae.csv`, three figures and the CodeCarbon log `emissions.csv`. The core of the training step is short:

```python
models = {
    "CTGAN": CTGAN(epochs=args.epochs, verbose=False),
    "TVAE": TVAE(epochs=args.epochs),
}
for name, model in models.items():
    model.set_random_state(args.seed)
    df, seconds, energy = train_model(name, model, train, args.out)
```

where `train_model` calls `model.fit(train, discrete_columns=CATEGORICAL)` inside a CodeCarbon tracker and then `model.sample(len(train))`. On our test machine the whole script took about 2 minutes (126 s). It printed:

```text
train (5000, 14), holdout (5000, 14), reference (5000, 14)
CTGAN: trained in 91 s, 1.71 Wh
TVAE: trained in 19 s, 0.34 Wh
model  train seconds  energy Wh
CTGAN             91       1.71
 TVAE             19       0.34
real: share of '>50K' = 0.249, capital-gain = 0: 0.919, capital-gain < 0: 0.000
                                      CTGAN   TVAE
mean |diff| Pearson (numeric)         0.087  0.082
mean |diff| Cramer's V (categorical)  0.103  0.119
education matches education-num       0.255  0.934
share of '>50K'                       0.318  0.238
capital-gain = 0                      0.002  0.020
capital-gain < 0                      0.225  0.547
```

### Compare the tabular output

Open the three figures in `outputs/`:

- `marginals.png`: the distribution of six columns in the real and the synthetic data;
- `association_differences.png`: the absolute difference between real and synthetic data in Pearson correlation (numeric pairs) and Cramér's V (categorical pairs);
- `pca.png`: real and synthetic rows projected on the first two principal components of the encoded real data.

Below the mean differences in association, the printed table gives four more numbers per model. The first is the share of rows where `education` and `education-num` agree as they do in the real data, where each education level has exactly one number. The second is the share of rows with income `>50K`. The last two are the shares of rows with a capital gain of exactly zero and of below zero; the line that starts with `real:` gives the same shares for the real training data. Write down at least three differences between CTGAN and TVAE that you can see in the figures or the table.

### Change the training budget

Train both models again with fewer epochs and write the result to a new folder:

```bash
python lab1_tabular.py --epochs 20 --out outputs_e20
```

On our test machine this took 48 s. Compare the printed table with the one from 100 epochs. In our run, TVAE trained for 20 epochs produced no rows with income `>50K`.

### Change how CTGAN samples categories

CTGAN conditions its generator on one category of one discrete column at a time. Open `ctgan/data_sampler.py` in your environment (run `python -c "import ctgan, os; print(os.path.dirname(ctgan.__file__))"` to find it) and read `__init__` and `sample_original_condvec`. Then turn off the log-frequency option in `lab1_tabular.py`:

```diff
-        "CTGAN": CTGAN(epochs=args.epochs, verbose=False),
+        "CTGAN": CTGAN(epochs=args.epochs, verbose=False, log_frequency=False),
```

Run the script again with a new output folder, and compare the `sex` and `race` panels of `marginals.png` with your first run:

```bash
python lab1_tabular.py --epochs 100 --out outputs_nolog
```

On our test machine this run took 122 s. In our run, the share of women in the CTGAN data was 0.465 with the default setting and 0.478 with `log_frequency=False`, against 0.311 in the real training data. The share of the group Black went from 0.065 to 0.193, against 0.092 in the real data. Undo the change afterwards, so that Labs 2 to 4 use the default model.

### Train TimeGAN and TransFusion

Run the time-series script:

```bash
python lab1_timeseries.py --transfusion-dir TransFusion
```

The script generates 500 sine sequences of length 24 with 5 features. It trains synthcity's TimeGAN plugin for 100 iterations and a small TransFusion model for 200 epochs, samples 500 sequences from each, and writes the results to `outputs_ts/`. Both configurations are much smaller than the defaults, so that they fit in a lab session:

```python
# TimeGAN through synthcity; the static data and the outcome are constant dummies,
# and clusters is 5 unless you set --timegan-clusters
model = Plugins().get(
    "timegan", n_iter=n_iter, batch_size=128, random_state=seed, device="cpu",
    generator_n_units_hidden=50, discriminator_n_units_hidden=50, encoder_max_clusters=clusters,
)

# TransFusion: train.py in the repository uses hidden_dim=256, num_layers=6,
# n_head=8, timesteps=1000 and 5000 epochs
model = TransEncoder(features=dim, latent_dim=64, num_heads=4, num_layers=2, ff_size=256)
diffusion = GaussianDiffusion1D(
    model, seq_length=seq_len, timesteps=timesteps,
    objective="pred_v", loss_type="l2", beta_schedule="cosine",
)
```

We call the TransFusion classes directly instead of running the repository's `train.py`, because `train.py` uses `DataFrame.append`, which pandas 2 removed. Like `train.py`, the script trains with `objective="pred_v"`: the transformer predicts the velocity *v*, a weighted difference of the noise and the clean sequence, and not the noise itself. `GaussianDiffusion1D` also accepts `pred_noise` and `pred_x0`. [Lecture 3](../../03-lectures/lecture-3/) discusses how these objectives relate to the one described in the TransFusion paper. On our test machine the script took about 5 minutes (315 s). It printed:

```text
TimeGAN: 240 s, 3.99 Wh
TransFusion epoch 50: loss 0.1414
TransFusion epoch 100: loss 0.1041
TransFusion epoch 150: loss 0.1488
TransFusion epoch 200: loss 0.0969
TransFusion: 58 s, 1.08 Wh
      model  seconds  energy Wh
    TimeGAN      240       3.99
TransFusion       58       1.08
               min    max   mean  std across sequences  lag-1 autocorrelation
data
real         0.500  1.000  0.746                 0.046                  0.997
TimeGAN      0.524  0.988  0.805                 0.005                  0.872
TransFusion  0.294  1.000  0.741                 0.037                  0.987
```

### Compare the time-series output

Open `ts_samples.png` (four real and four synthetic sequences per model) and `ts_projections.png` (PCA and t-SNE of the flattened sequences). In the printed table, "std across sequences" is the standard deviation of the per-sequence mean: it measures how much the sequences differ from each other. "lag-1 autocorrelation" measures how smooth the sequences are.

In our run, the TimeGAN sequences had a step shape and were nearly identical to each other: the standard deviation across sequences was 0.005, against 0.046 for the real data. This is a sign of mode collapse. The TransFusion sequences spread over the real data in the PCA and t-SNE plots, but were noisier than the real sine curves. Check whether your run shows the same, and look at the figures before you trust the numbers.

### Change TimeGAN's data encoding

synthcity encodes each feature with a Gaussian mixture before TimeGAN sees it, in the same way that CTGAN encodes numeric columns: the model learns which mixture mode a value belongs to and where it lies within that mode. The script lets the encoder use up to 5 modes per feature. Train TimeGAN alone with a single mode:

```bash
python lab1_timeseries.py --transfusion-dir TransFusion --models timegan --timegan-clusters 1 --out outputs_ts_c1
```

On our test machine this took about 3.5 minutes (219 s). Every generated sequence was the same smooth curve, with the five features almost on top of each other; the standard deviation across sequences was 0.000. Compare `outputs_ts_c1/ts_samples.png` with `outputs_ts/ts_samples.png`.

> [!NOTE] More training did not help in our tests
> We also trained TimeGAN with up to 20 modes, with an LSTM in place of the default RNN, and for 500 iterations in place of 100. In every case the standard deviation across sequences stayed at about 0.005, against 0.046 for the real data. Other jobs ran on the machine during these tests, so we do not report their run times.

{{% /steps %}}

## Questions for your lab notes

1. CTGAN trains its generator against a critic with a Wasserstein loss and a gradient penalty. The critic judges packs of ten rows, and a cross-entropy term ties each generated row to its conditional category. TVAE maximises an evidence lower bound: a reconstruction term (Gaussian for numeric columns, cross-entropy for categorical columns) minus a KL term. Read `ctgan/synthesizers/ctgan.py` and `tvae.py` to check. Which of the differences you wrote down in task 2 can you explain through these objectives, and which ones need another explanation, such as the data encoding or the training budget?
2. In the real data, 91.9% of the rows have a capital gain of exactly zero and none is negative. In our run, CTGAN and TVAE produced almost no zeros, and 22.5% and 54.7% of their rows had a negative capital gain. Both models encode each numeric column with a Bayesian Gaussian mixture (mode-specific normalisation; see `ctgan/data_transformer.py`). Explain how this encoding can produce the result, and propose a change to the data preparation that would avoid it.
3. In the real data, `education` determines `education-num` exactly. Why might a model with a reconstruction loss keep this rule better than an adversarial model? What does the result suggest about using synthetic data where such rules matter, for example in medical records?
4. Did turning off `log_frequency` bring the `sex` and `race` marginals closer to the real data? Use the code you read in task 4 to decide whether the conditional sampling can explain the gap, and propose another explanation that you could test with the scripts, for example with the 20-epoch run.
5. Several models in this lab produced data that looked acceptable in one view and poor in another. Give one example, and argue which view a user of the synthetic data should trust.
6. In our run, the GAN for sequences collapsed while the diffusion model did not, although TimeGAN trained about four times as long (240 s against 58 s). List the explanations that fit this observation: the adversarial objective, the number of parameter updates, the architecture, the data encoding, the synthcity implementation or our small configuration. Which of them does task 7 rule in or out? Design an experiment that separates two of the others.
7. Every number in this lab comes from a single run with one seed. Pick one conclusion you would draw from your results and say how many runs you would need before you would state it in a paper.

## Energy use

Each script wraps every training run in a CodeCarbon `OfflineEmissionsTracker` and appends one row per run to `emissions.csv` in the output folder. In `lab1_tabular.py` this looks as follows:

```python
tracker = OfflineEmissionsTracker(
    country_iso_code="SWE",
    project_name=f"lab1-{name}",
    output_dir=str(out),
    log_level="error",
)
tracker.start()
start = time.perf_counter()
model.fit(train, discrete_columns=CATEGORICAL)
seconds = time.perf_counter() - start
tracker.stop()
energy_kwh = tracker.final_emissions_data.energy_consumed
```

Open `outputs/emissions.csv` and `outputs_ts/emissions.csv`. Compare `energy_consumed` (kWh) and `duration` (seconds) across the four models, and look at the columns `cpu_power`, `gpu_power`, `ram_power` and `tracking_mode`. In our runs, CTGAN used 1.71 Wh, TVAE 0.34 Wh, TimeGAN 3.99 Wh and TransFusion 1.08 Wh.

**Question.** Our test machine has a graphics card that PyTorch never used, yet CodeCarbon reported a non-zero `gpu_power` for every run. What does the default `tracking_mode` of `machine` measure, and how would the numbers change with `tracking_mode="process"`? Which of the two would you report for a training run in a paper, and why?

## Completing the lab

Completing all three labs is part of the [examination](../../07-examination/). As evidence for this lab, the course leader may ask for short lab notes: your answers to the questions above, with the tables and figures they refer to, and the energy figures from `emissions.csv`. Follow the course leader's instructions for the format and the deadline.

## Further reading

- Xu, L., Skoularidou, M., Cuesta-Infante, A., & Veeramachaneni, K. (2019). Modeling Tabular data using Conditional GAN. *Advances in Neural Information Processing Systems 32 (NeurIPS 2019)*. [arXiv:1907.00503](https://arxiv.org/abs/1907.00503)
- Yoon, J., Jarrett, D., & van der Schaar, M. (2019). Time-series Generative Adversarial Networks. *Advances in Neural Information Processing Systems 32 (NeurIPS 2019)*. [Proceedings page](https://papers.nips.cc/paper_files/paper/2019/hash/c9efe5f26cd17ba6216bbe2a7d26d490-Abstract.html)
- Ho, J., Jain, A. N., & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. *Advances in Neural Information Processing Systems 33 (NeurIPS 2020)*. [Proceedings page](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)
- Sikder, M. F., Ramachandranpillai, R., & Heintz, F. (2025). TransFusion: Generating long, high fidelity time series using diffusion models with transformers. *Machine Learning with Applications*, 20, 100652. [doi:10.1016/j.mlwa.2025.100652](https://doi.org/10.1016/j.mlwa.2025.100652)
- Qian, Z., Davis, R., & van der Schaar, M. (2023). Synthcity: a benchmark framework for diverse use cases of tabular synthetic data. *Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track*. [Proceedings page](https://papers.nips.cc/paper_files/paper/2023/hash/09723c9f291f6056fd1885081859c186-Abstract-Datasets_and_Benchmarks.html)
- Becker, B., & Kohavi, R. (1996). Adult [Dataset]. UCI Machine Learning Repository. [doi:10.24432/C5XW20](https://doi.org/10.24432/C5XW20)
