---
title: "Lecture 3: Diffusion models, transformers and LLMs"
linkTitle: "L3: Diffusion, transformers, LLMs"
weight: 33
---

**Week 3** · 2 hours · Learning outcome [LO1](../../01-about/#learning-outcomes)

## Slides

{{< slides "gmsd-lecture-3" >}}

## Overview

[Lecture 2](../lecture-2/) covered two families that produce a sample in one network pass: the variational autoencoder (VAE) and the generative adversarial network (GAN). This lecture covers two families that generate step by step. A diffusion model learns to reverse a fixed process that turns data into Gaussian noise, so it produces a sample through many denoising passes. An autoregressive transformer produces a sequence one token at a time, each token conditioned on the ones before it. Transformers also serve as the denoising network inside diffusion models; TransFusion uses this design to generate long time series.

The lecture follows the question behind LO1: how does the training objective shape the synthetic data? You derive the diffusion objective from a variational bound and see what the common simplification gives up. You then see how diffusion is adapted to mixed-type tables and to time series, and how a table can be written as text for a large language model (LLM). The lecture closes with a comparison of the four families on likelihood, sample quality, mode coverage, sampling cost, conditioning, memorisation and energy. Evaluation metrics are only named here: [Lecture 4](../lecture-4/) treats them in depth, and [Lecture 5](../lecture-5/) and [Lecture 6](../lecture-6/) cover privacy and fairness.

## Learning goals

After this lecture, you should be able to:

1. Derive the closed form of $q(x_t \mid x_0)$ and the noise-prediction loss of Ho et al. (2020) from the variational bound, and explain what the simplified loss changes in the synthetic data (LO1).
2. Relate noise prediction to score estimation, and explain how DDIM sampling and classifier-free guidance change the sampling cost and the diversity of the samples (LO1).
3. Describe how TabDDPM, TabSyn, CSDI, Diffusion-TS, TransFusion and GReaT handle mixed-type tables and time series, and argue which of them suits a dataset from your own field (LO1, LO4).
4. Explain what the long-sequence discriminative and predictive scores of TransFusion measure, and what they cannot detect (LO2).
5. Compare VAEs, GANs, diffusion models and autoregressive transformers on likelihood, sample quality, sampling cost and memorisation, and judge what the memorisation evidence implies for releasing a synthetic dataset (LO1, LO3).

## Before the lecture

Read these three papers before the lecture.

- Ho, J., Jain, A., & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. *Advances in Neural Information Processing Systems*, 33, 6840–6851. [Proceedings](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html) · [arXiv:2006.11239](https://arxiv.org/abs/2006.11239)

  *What to look for:* the steps in Section 3 that turn the variational bound into the loss $L_\text{simple}$, and how the CIFAR-10 results change when the authors train on $L_\text{simple}$ instead of the bound.
- Sikder, M. F., Ramachandranpillai, R., & Heintz, F. (2025). TransFusion: Generating long, high fidelity time series using diffusion models with transformers. *Machine Learning with Applications*, 20, 100652. [doi:10.1016/j.mlwa.2025.100652](https://doi.org/10.1016/j.mlwa.2025.100652) · [arXiv:2307.12667](https://arxiv.org/abs/2307.12667) · [Code](https://github.com/fahim-sikder/TransFusion) · [Publication page](/publications/diffusion-time-series/)

  *What to look for:* which part of the DDPM pipeline the transformer encoder replaces, and how the two proposed scores (LDS and LPS) are computed.
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is All you Need. *Advances in Neural Information Processing Systems*, 30. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)

  *What to look for:* how scaled dot-product attention and the positional encoding work in Section 3, since both reappear in TransFusion and in the language models that generate tables as text.

## Lecture notes

### From one network pass to many

In Lecture 2 the VAE maximised a lower bound on $\log p_\theta(x)$ with a learned encoder, and the GAN trained a generator against a discriminator. Diffusion models keep a variational bound but fix the encoder: a forward process adds Gaussian noise over $T$ steps, and only the reverse process is learned. [Sohl-Dickstein et al. (2015)](https://proceedings.mlr.press/v37/sohl-dickstein15.html) introduced the idea: destroy the structure of the data slowly, then learn a reverse process that restores it. [Ho et al. (2020)](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html) made it competitive on images with a reparameterised loss. [Luo (2022)](https://arxiv.org/abs/2208.11970) derives the same bound by treating a diffusion model as a Markovian hierarchical VAE.

### The forward process and its closed form

Let $x_0 \sim q(x_0)$ be one data point, for example a normalised table row or a multivariate time series. The forward process is a Markov chain with a variance schedule $\beta_1, \dots, \beta_T$:

$$
q(x_t \mid x_{t-1}) = \mathcal{N}\big(x_t;\ \sqrt{1-\beta_t}\, x_{t-1},\ \beta_t I\big), \qquad t = 1, \dots, T.
$$

Define $\alpha_t = 1 - \beta_t$ and $\bar{\alpha}_t = \prod_{s=1}^{t} \alpha_s$. Then $x_t$ can be drawn from $x_0$ in one step ([Ho et al., 2020](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)):

$$
q(x_t \mid x_0) = \mathcal{N}\big(x_t;\ \sqrt{\bar{\alpha}_t}\, x_0,\ (1-\bar{\alpha}_t) I\big), \qquad x_t = \sqrt{\bar{\alpha}_t}\, x_0 + \sqrt{1-\bar{\alpha}_t}\, \epsilon, \quad \epsilon \sim \mathcal{N}(0, I).
$$

**Derivation.** Write one step as $x_t = \sqrt{\alpha_t}\, x_{t-1} + \sqrt{1-\alpha_t}\, \epsilon_t$ and substitute the previous step:

$$
x_t = \sqrt{\alpha_t \alpha_{t-1}}\, x_{t-2} + \sqrt{\alpha_t (1-\alpha_{t-1})}\, \epsilon_{t-1} + \sqrt{1-\alpha_t}\, \epsilon_t .
$$

The two noise terms are independent zero-mean Gaussians, so their sum is Gaussian with variance $\alpha_t(1-\alpha_{t-1}) + 1 - \alpha_t = 1 - \alpha_t \alpha_{t-1}$. Induction over the remaining steps gives the closed form.

The closed form has two consequences. Training never simulates the chain: it draws a random $t$ and noises $x_0$ directly. And when $\bar{\alpha}_T \approx 0$, $q(x_T \mid x_0)$ is close to $\mathcal{N}(0, I)$ for every $x_0$, so sampling can start from a fixed prior.

The schedule decides how fast information is destroyed. Ho et al. use $T = 1000$ and a linear schedule from $\beta_1 = 10^{-4}$ to $\beta_T = 0.02$. [Nichol and Dhariwal (2021)](https://proceedings.mlr.press/v139/nichol21a.html) found that this schedule destroys information faster than necessary on 32×32 and 64×64 images. They proposed a cosine schedule: $\bar{\alpha}_t = f(t)/f(0)$ with $f(t) = \cos^2\big(\tfrac{t/T + s}{1+s} \cdot \tfrac{\pi}{2}\big)$, $s = 0.008$, and $\beta_t$ clipped at 0.999. TransFusion uses the cosine schedule ([Sikder et al., 2025](https://doi.org/10.1016/j.mlwa.2025.100652)). Treat the schedule as a hyperparameter to tune for your data.

### The reverse process and the variational bound

The generative model runs the chain backwards from $p(x_T) = \mathcal{N}(0, I)$ with learned Gaussian transitions:

$$
p_\theta(x_{t-1} \mid x_t) = \mathcal{N}\big(x_{t-1};\ \mu_\theta(x_t, t),\ \Sigma_\theta(x_t, t)\big).
$$

Training minimises a bound on the negative log-likelihood, which splits into one term per step:

$$
\begin{aligned}
\mathbb{E}\big[-\log p_\theta(x_0)\big] \le \mathbb{E}_q\Big[ & \underbrace{D_\text{KL}\big(q(x_T \mid x_0) \,\|\, p(x_T)\big)}_{L_T} \\
& + \sum_{t > 1} \underbrace{D_\text{KL}\big(q(x_{t-1} \mid x_t, x_0) \,\|\, p_\theta(x_{t-1} \mid x_t)\big)}_{L_{t-1}} \underbrace{-\log p_\theta(x_0 \mid x_1)}_{L_0} \Big].
\end{aligned}
$$

$L_T$ has no parameters. The terms $L_{t-1}$ are tractable because the forward posterior, conditioned on $x_0$, is Gaussian, $q(x_{t-1} \mid x_t, x_0) = \mathcal{N}\big(x_{t-1};\ \tilde{\mu}_t(x_t, x_0),\ \tilde{\beta}_t I\big)$, with

$$
\tilde{\mu}_t(x_t, x_0) = \frac{\sqrt{\bar{\alpha}_{t-1}}\, \beta_t}{1-\bar{\alpha}_t}\, x_0 + \frac{\sqrt{\alpha_t}\, (1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t}\, x_t,
\qquad
\tilde{\beta}_t = \frac{1-\bar{\alpha}_{t-1}}{1-\bar{\alpha}_t}\, \beta_t .
$$

Ho et al. fix $\Sigma_\theta = \sigma_t^2 I$ and report similar results for $\sigma_t^2 = \beta_t$ and $\sigma_t^2 = \tilde{\beta}_t$. A KL divergence between two Gaussians with fixed variances reduces to a squared distance between their means:

$$
L_{t-1} = \mathbb{E}_q\Big[ \frac{1}{2\sigma_t^2} \big\| \tilde{\mu}_t(x_t, x_0) - \mu_\theta(x_t, t) \big\|^2 \Big] + C .
$$

### From the bound to noise prediction

Substitute $x_0 = (x_t - \sqrt{1-\bar{\alpha}_t}\, \epsilon)/\sqrt{\bar{\alpha}_t}$ into $\tilde{\mu}_t$. The coefficient of $x_t$ simplifies to $1/\sqrt{\alpha_t}$, which gives $\tilde{\mu}_t = \frac{1}{\sqrt{\alpha_t}}\big(x_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\, \epsilon\big)$. Ho et al. therefore give $\mu_\theta$ the same form, with a network $\epsilon_\theta(x_t, t)$ that predicts the noise. The step loss becomes a weighted regression on the noise:

$$
L_{t-1} - C = \mathbb{E}_{x_0, \epsilon}\Big[ \frac{\beta_t^2}{2\sigma_t^2\, \alpha_t\, (1-\bar{\alpha}_t)} \big\| \epsilon - \epsilon_\theta\big(\sqrt{\bar{\alpha}_t}\, x_0 + \sqrt{1-\bar{\alpha}_t}\, \epsilon,\ t\big) \big\|^2 \Big].
$$

Ho et al. drop the weight and sample $t$ uniformly from $\{1, \dots, T\}$:

$$
L_\text{simple}(\theta) = \mathbb{E}_{t, x_0, \epsilon}\Big[ \big\| \epsilon - \epsilon_\theta\big(\sqrt{\bar{\alpha}_t}\, x_0 + \sqrt{1-\bar{\alpha}_t}\, \epsilon,\ t\big) \big\|^2 \Big].
$$

Sampling follows the learned chain. For $t = T, \dots, 1$, with $z \sim \mathcal{N}(0, I)$ for $t > 1$ and $z = 0$ at $t = 1$:

$$
x_{t-1} = \frac{1}{\sqrt{\alpha_t}}\Big( x_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}\, \epsilon_\theta(x_t, t) \Big) + \sigma_t z .
$$

Three consequences follow for synthetic data.

1. **A regression problem.** Each step is a supervised denoising task with a known target. There is no discriminator and no minimax game.
2. **The weighting trades likelihood for sample quality.** Ho et al. state that $L_\text{simple}$ down-weights the terms for small $t$, so the network spends more effort on the harder denoising tasks at large $t$. On CIFAR-10 they report an FID of 3.17 and a bound of at most 3.75 bits per dimension with $L_\text{simple}$, against an FID of 13.51 and at most 3.70 bits per dimension with the true bound. They note that their log-likelihoods are not competitive with other likelihood-based models. [Nichol and Dhariwal (2021)](https://proceedings.mlr.press/v139/nichol21a.html) learn the variance and add the bound with a small weight, $L_\text{hybrid} = L_\text{simple} + 0.001\, L_\text{vlb}$; they report 2.94 bits per dimension on CIFAR-10.
3. **Sampling is expensive.** One sample costs $T$ network evaluations, 1000 in Ho et al., against one for a VAE decoder or a GAN generator.

> [!IMPORTANT] Record the choices that the network does not show
> The schedule, the loss weighting and the number of sampling steps set the sample quality, the likelihood and the sampling cost. When you compare a diffusion model with a GAN in Lab 1, record these choices next to the results.

### Scores and the SDE view

The score of a density is $\nabla_x \log p(x)$; learning it avoids the normalising constant ([Hyvärinen, 2005](https://www.jmlr.org/papers/v6/hyvarinen05a.html)). [Vincent (2011)](https://doi.org/10.1162/NECO_a_00142) showed that regressing onto the score of a Gaussian corruption kernel is equivalent to score matching on the corrupted density; this is denoising score matching. For the forward process above,

$$
\nabla_{x_t} \log q(x_t \mid x_0) = -\frac{x_t - \sqrt{\bar{\alpha}_t}\, x_0}{1-\bar{\alpha}_t} = -\frac{\epsilon}{\sqrt{1-\bar{\alpha}_t}} .
$$

So $L_\text{simple}$ at step $t$ is denoising score matching with the score model $s_\theta(x_t, t) = -\epsilon_\theta(x_t, t)/\sqrt{1-\bar{\alpha}_t}$, a link that Ho et al. make explicit. [Song and Ermon (2019)](https://proceedings.neurips.cc/paper/2019/hash/3001ef257407d5a371a96dcd947c7d93-Abstract.html) had already generated samples from estimated scores with annealed Langevin dynamics.

[Song et al. (2021)](https://arxiv.org/abs/2011.13456) take the limit $T \to \infty$. The forward process becomes a stochastic differential equation (SDE), $dx = f(x, t)\, dt + g(t)\, dw$, and its time reversal is again a diffusion process:

$$
dx = \big[ f(x, t) - g(t)^2\, \nabla_x \log p_t(x) \big]\, dt + g(t)\, d\bar{w} .
$$

A score model $s_\theta(x, t)$ is trained by denoising score matching, weighted by $\lambda(t)$ over time. DDPM corresponds to the variance-preserving SDE $dx = -\tfrac{1}{2}\beta(t)\, x\, dt + \sqrt{\beta(t)}\, dw$, and the model of Song and Ermon to a variance-exploding SDE. A deterministic probability flow ODE shares the marginals $p_t$:

$$
dx = \big[ f(x, t) - \tfrac{1}{2} g(t)^2\, \nabla_x \log p_t(x) \big]\, dt .
$$

The SDE view has three consequences. Training and sampling separate: one score model can be sampled with different solvers. The ODE gives exact likelihoods through the instantaneous change of variables formula; Song et al. report 2.99 bits per dimension on uniformly dequantised CIFAR-10. And the ODE is a deterministic map between noise and data, so a real record can be encoded into noise and decoded again.

### Faster sampling with DDIM

[Song, Meng and Ermon (2021)](https://arxiv.org/abs/2010.02502) define non-Markovian forward processes with the same marginals $q(x_t \mid x_0)$. The training objective is unchanged, so a trained DDPM can be sampled with DDIM without retraining. In DDPM notation, one step estimates the clean sample and then moves towards $x_{t-1}$:

$$
\hat{x}_0 = \frac{x_t - \sqrt{1-\bar{\alpha}_t}\, \epsilon_\theta(x_t, t)}{\sqrt{\bar{\alpha}_t}}, \qquad
x_{t-1} = \sqrt{\bar{\alpha}_{t-1}}\, \hat{x}_0 + \sqrt{1-\bar{\alpha}_{t-1}-\sigma_t^2}\, \epsilon_\theta(x_t, t) + \sigma_t z .
$$

> [!WARNING] Notation
> The DDIM paper writes $\alpha_t$ for the cumulative product that Ho et al. call $\bar{\alpha}_t$. Check which convention a paper or code base uses before you compare equations.

The parameter $\sigma_t$ sets the stochasticity through a hyperparameter $\eta$: $\eta = 1$ recovers the DDPM sampler and $\eta = 0$ gives the deterministic DDIM sampler. Sampling on a subsequence of the $T$ steps skips steps; Song, Meng and Ermon report high-quality samples 10 to 50 times faster in wall-clock time than DDPM. Progressive distillation goes further: it trains a student that needs half the steps of its teacher, and repeats this down to as few as 4 steps ([Salimans and Ho, 2022](https://arxiv.org/abs/2202.00512)). Denoising diffusion GANs instead model large denoising steps with a conditional GAN, because the Gaussian reverse step holds only for small steps ([Xiao et al., 2022](https://arxiv.org/abs/2112.07804)).

### Conditioning and guidance

Synthetic data often needs a condition $c$: a class label, a sensitive attribute or a set of observed values. Bayes' rule splits the conditional score:

$$
\nabla_{x_t} \log p(x_t \mid c) = \nabla_{x_t} \log p(x_t) + \nabla_{x_t} \log p(c \mid x_t).
$$

Classifier guidance trains a classifier $p_\phi(c \mid x_t)$ on noisy inputs and adds its gradient, scaled by $s$, at each step. [Dhariwal and Nichol (2021)](https://proceedings.neurips.cc/paper/2021/hash/49ad23d1ec9fa4bd8d77d02681df5cfa-Abstract.html) report that scales above 1 trade recall, a measure of diversity, for precision. Classifier-free guidance removes the separate classifier ([Ho and Salimans, 2022](https://arxiv.org/abs/2207.12598)). One network $\epsilon_\theta(x_t, c)$ is trained with $c$ replaced by a null token with probability $p_\text{uncond}$ (0.1 and 0.2 worked equally well, 0.5 worse). At sampling time, with guidance weight $w$:

$$
\tilde{\epsilon}_\theta(x_t, c) = (1 + w)\, \epsilon_\theta(x_t, c) - w\, \epsilon_\theta(x_t).
$$

Because $\epsilon_\theta$ is a scaled negative score, $\epsilon_\theta(x_t, c) - \epsilon_\theta(x_t)$ is proportional to $-\nabla_{x_t} \log p(c \mid x_t)$, an implicit classifier. In their ImageNet experiments, the best FID came from small weights ($w = 0.1$ or $0.3$) and the best Inception score from $w \ge 4$; larger weights gave less varied samples. Each guided step needs two network evaluations.

> [!QUESTION] Guidance and small groups
> Guidance trades diversity for fidelity within each condition. If $c$ marks a small subgroup of a table, that trade-off acts on the rows you have least of. Treat the effect on group-level statistics as an open question to test; [Lecture 6](../lecture-6/) returns to it.

### Diffusion for tabular data

Gaussian diffusion assumes continuous coordinates, but a table mixes numerical and categorical columns. Two routes exist.

**Discrete diffusion per column.** Multinomial diffusion ([Hoogeboom et al., 2021](https://proceedings.neurips.cc/paper/2021/hash/67d96d458abdef21792e6d8e590244e7-Abstract.html)) works on one-hot vectors $x \in \{0, 1\}^K$. Each step keeps the category with probability $1 - \beta_t$ and resamples it uniformly over the $K$ categories with probability $\beta_t$:

$$
q(x_t \mid x_{t-1}) = \mathcal{C}\big(x_t \mid (1-\beta_t)\, x_{t-1} + \beta_t / K\big), \qquad
q(x_t \mid x_0) = \mathcal{C}\big(x_t \mid \bar{\alpha}_t\, x_0 + (1-\bar{\alpha}_t) / K\big).
$$

The network predicts a probability vector $\hat{x}_0$, which is plugged into the closed-form posterior $q(x_{t-1} \mid x_t, \hat{x}_0)$.

[TabDDPM (Kotelnikov et al., 2023)](https://proceedings.mlr.press/v202/kotelnikov23a.html) combines the two processes: Gaussian diffusion on quantile-transformed numerical features, and a separate multinomial diffusion for each categorical feature. An MLP denoiser is trained on $L_\text{simple}$ plus the multinomial KL terms, divided by the number of categorical features. The model is class-conditional for classification datasets; for regression, the target is one more numerical feature. Measured by the distance to the closest real record (DCR), Kotelnikov et al. find TabDDPM more private than SMOTE and less private than the GAN and VAE baselines, partly because those baselines have lower utility. They also state that DCR is not an ultimate privacy measure.

**Diffusion in a learned latent space.** [TabSyn (Zhang et al., 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9750610639c3e7a849cff746bf60dbd-Abstract-Conference.html) first trains a VAE with a column-wise tokeniser and a transformer encoder and decoder, which maps each mixed-type row to a continuous embedding. A score-based diffusion model with noise level $\sigma(t) = t$ then runs in this latent space, as latent diffusion does for images ([Rombach et al., 2022](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html)). Zhang et al. report their best results with fewer than 20 network evaluations, and error rates 86% and 67% lower than the most competitive baselines for column-wise distributions and pair-wise column correlations. TabSyn treats only unconditional generation, and its authors report that TabDDPM fails to generate meaningful content on one of their datasets.

Memorisation is a live concern for both routes. [Fang et al. (2025)](https://proceedings.mlr.press/v267/fang25f.html) find that tabular diffusion models reproduce training records, increasingly so with more training epochs, and propose TabCutMix, which swaps feature segments between training rows of the same class.

### Diffusion for time series

Following TransFusion, a time series is $x \in \mathbb{R}^{N \times D}$ with sequence length $N$ and $D$ features. Three tasks recur: imputation, forecasting and unconditional generation.

**CSDI** ([Tashiro et al., 2021](https://proceedings.neurips.cc/paper/2021/hash/cfe8504bda37b575c70ee1a8276f3486-Abstract.html)) imputes missing values with a conditional denoiser $\epsilon_\theta(x_t^\text{ta}, t \mid x_0^\text{co})$, where $x_0^\text{co}$ are observed values and $x^\text{ta}$ the imputation targets. Training masks some observed values and uses them as targets, much as masked language modelling does. Each residual layer has a temporal and a feature transformer. With $T = 50$, Tashiro et al. report improvements of 40–65% over existing probabilistic imputation methods on healthcare and environmental data, and note that sampling is slower than for other generative models.

**Diffusion-TS** ([Yuan and Qiao, 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/b5b66077d016c037576cc56a82f97f66-Abstract-Conference.html)) uses an encoder-decoder transformer whose decoder separates trend (a polynomial regressor) from seasonality (Fourier bases). It predicts the clean sample instead of the noise and adds a Fourier-domain term to the loss. Forecasting and imputation use reconstruction-based guidance at sampling time, without retraining. The main benchmark uses length 24, with longer runs up to 256.

**TransFusion** ([Sikder et al., 2025](https://doi.org/10.1016/j.mlwa.2025.100652)) targets long sequences. Its authors argue that recurrent and convolutional GANs fail to capture long-range dependencies and suffer from mode collapse. TransFusion keeps the DDPM training and sampling algorithms and replaces the denoising network with a transformer encoder. A linear layer maps the $D$ features to the hidden size, positional encoding marks the time steps, the encoder applies self-attention over the whole sequence, and a second linear layer maps back to $D$ features. Sikder et al. use a hidden size of 256, 8 heads, 6 encoder layers, Adam with learning rate $10^{-4}$, 5000 epochs, the cosine schedule and the noise-prediction loss. Experiments cover four datasets (Sine, Stock, Energy with 28 features, and Air Quality) at lengths 100 and 384, against eight baselines including TimeGAN, GT-GAN and the diffusion model TimeGrad. In an ablation, a transformer GAN and a diffusion model with a GRU denoiser both perform worse.

> [!NOTE] The released code
> In the [code](https://github.com/fahim-sikder/TransFusion), the diffusion step is embedded and prepended to the sequence as an extra token. The defaults are $T = 1000$ and the cosine schedule. The `objective` argument of `train.py` selects the target, `pred_noise`, `pred_x0` or `pred_v`, with `pred_v` as the default: the $v$-parameterisation of [Salimans and Ho (2022)](https://arxiv.org/abs/2202.00512), who write $z_t = \alpha_t x + \sigma_t \epsilon$ and $v = \alpha_t \epsilon - \sigma_t x$. Note which target you train in Lab 1.

TransFusion proposes two scores for long sequences, which replace the recurrent networks in the discriminative and predictive scores of TimeGAN ([Yoon et al., 2019](https://proceedings.neurips.cc/paper/2019/hash/c9efe5f26cd17ba6216bbe2a7d26d490-Abstract.html)) with transformers:

- **Long-Sequence Discriminative Score (LDS).** A transformer-encoder classifier is trained to separate real sequences (labelled original) from synthetic ones (labelled fake). On held-out data, $\text{LDS} = |0.5 - \text{accuracy}|$. Lower is better; 0 means that the classifier is at chance.
- **Long-Sequence Predictive Score (LPS).** A transformer is trained on synthetic data to predict the next feature vector and is tested on real data. LPS is the mean absolute error; lower is better. A variant predicts five steps ahead.

The paper also reports the Jensen-Shannon divergence, α-precision and β-recall ([Alaa et al., 2022](https://proceedings.mlr.press/v162/alaa22a.html)), a coverage score, and PCA and t-SNE plots; Lecture 4 covers these. Two limits of LDS matter here. Its value depends on the capacity and training of the classifier, so a weak classifier gives a low LDS for any data. And a generator that copies its training sequences also gets an LDS near 0, so LDS must be paired with a memorisation test from Lecture 5. The paper names slower sampling than GANs as a limitation, and fair synthetic time series as future work.

### Transformer-based generative models

The transformer ([Vaswani et al., 2017](https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)) is built from scaled dot-product attention, run in parallel over $h$ heads:

$$
\text{Attention}(Q, K, V) = \text{softmax}\Big( \frac{Q K^\top}{\sqrt{d_k}} \Big) V, \qquad
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h)\, W^O ,
$$

with $\text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)$ and sinusoidal positional encodings for order. A self-attention layer connects any two positions in one step. Its cost per layer is $O(n^2 \cdot d)$ for sequence length $n$ and width $d$. This quadratic cost limits sequence length on fixed hardware; Sikder et al. expect longer sequences to be feasible given adequate GPU memory.

An autoregressive transformer factorises the joint distribution by the chain rule, $p_\theta(x) = \prod_{i=1}^{n} p_\theta(x_i \mid x_{<i})$, and is trained by maximum likelihood on the next token. A causal mask prevents leftward information flow in the decoder. The likelihood is exact, but sampling needs $n$ sequential network passes.

**Tables as text.** [GReaT (Borisov et al., 2023)](https://arxiv.org/abs/2210.06280) writes each row as clauses such as "Occupation is doctor, Gender is female, Age is 34". Tabular features have no natural order, so the clauses are shuffled at random during training. Borisov et al. fine-tune a distilled GPT-2 (about 82 million parameters) and GPT-2 (over 355 million). Sampling starts from a feature name or any set of known values, which gives arbitrary conditioning without retraining. The design has costs. Numbers are generated as character strings. Invalid outputs are discarded; their rate stayed below 11% in the experiments of Borisov et al. Fine-tuning takes hours, against about a minute for CTGAN in their timing experiment. And because each row is seen under many feature orders, the model need not assign a row the same probability under two orders.

**Transformers as denoisers.** A denoising transformer has no causal mask: it attends over the whole noisy input and iterates over noise levels, not positions. DiT replaces the U-Net backbone of latent image diffusion with a transformer over latent patches ([Peebles and Xie, 2023](https://openaccess.thecvf.com/content/ICCV2023/html/Peebles_Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.html)). CSDI, Diffusion-TS, TransFusion and the TabSyn autoencoder all use transformer layers.

### Comparing the families

The table summarises the evidence from this lecture and Lecture 2. Each cell rests on the source named in it or on a derivation above.

| | VAE | GAN | Diffusion model | Autoregressive transformer |
|---|---|---|---|---|
| Training objective | Evidence lower bound ([Kingma and Welling, 2014](https://arxiv.org/abs/1312.6114)) | Minimax game between generator and discriminator ([Goodfellow et al., 2014](https://proceedings.neurips.cc/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html)) | Variational bound, in practice the reweighted $L_\text{simple}$ (Ho et al., 2020) | Next-token log-likelihood (chain rule) |
| Likelihood | Lower bound | None; implicit model | Bound; exact through the probability flow ODE (Song et al., 2021) | Exact, for a given token order |
| Quality and mode coverage | Faithful mode coverage, often low sample quality ([Xiao et al., 2022](https://arxiv.org/abs/2112.07804)) | High quality, poor mode coverage (Xiao et al., 2022) | High quality and good mode coverage, slow sampling (Xiao et al., 2022) | Not part of the comparison by Xiao et al. |
| Network passes per sample | 1 | 1 | $T$ (1000 in Ho et al.); fewer with DDIM; 2 per step with classifier-free guidance | 1 per token, in sequence |
| Conditioning | Conditional VAE ([Sohn et al., 2015](https://proceedings.neurips.cc/paper/2015/hash/8d55a249e6baa5c06772297520da2051-Abstract.html)) | Conditional generator, for example CTGAN ([Xu et al., 2019](https://proceedings.neurips.cc/paper/2019/hash/254ed7d2de3b23ab10936522dd547b78-Abstract.html)) | Classifier or classifier-free guidance; observed values (CSDI) | Prompt with known values (GReaT) |
| Memorisation evidence | Occurs, and differs from overfitting ([van den Burg and Williams, 2021](https://proceedings.neurips.cc/paper/2021/hash/eae15aabaa768ae4a5993a8a4f4fa6e4-Abstract.html)) | Less leakage than diffusion models in the experiments of Carlini et al. (2023) | Training images extracted ([Carlini et al., 2023](https://www.usenix.org/conference/usenixsecurity23/presentation/carlini)); tabular memorisation grows with epochs (Fang et al., 2025) | Verbatim training text extracted from GPT-2 ([Carlini et al., 2021](https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting)) |

**Likelihood is not sample quality.** [Theis et al. (2016)](https://arxiv.org/abs/1511.01844) show that log-likelihood and the visual quality of samples are largely independent in high dimensions, and conclude that a generative model should be evaluated for its intended application. The DDPM result above, a better FID with a worse bound, is one instance. For synthetic data the application is a downstream task with privacy and fairness requirements, which Lectures 4 to 6 measure directly.

**Memorisation.** [Carlini et al. (2023)](https://www.usenix.org/conference/usenixsecurity23/presentation/carlini) extract over a thousand training images from Stable Diffusion and Imagen. Duplicated training images are far more likely to be memorised, and Carlini et al. conclude that diffusion models are much less private than earlier generative models such as GANs. Their membership inference attack on CIFAR-10 diffusion models reaches a true positive rate above 70% at a 1% false positive rate, and their attempt at differentially private training on CIFAR-10 diverged. The objective itself points the same way. With $n$ training points, $q_t$ is a mixture of $n$ Gaussians, and a model that learns its exact score inverts the forward process back to the training points. [Gu et al. (2025)](https://arxiv.org/abs/2310.02664) make this argument and find that memorisation appears more readily on smaller datasets. Generalisation therefore depends on the network not reaching the optimum of its own objective, which is a direct release risk for a small clinical table (Lecture 5).

**Energy and cost.** [Luccioni et al. (2024)](https://doi.org/10.1145/3630106.3658542) measured inference energy across tasks: image generation used a mean of 2.9 kWh per 1,000 inferences, against 0.002 kWh for text classification. For a diffusion model, sampling energy grows with the number of network evaluations per sample. Training can still be cheaper than for a GAN: TransFusion trained in 5 hours against nearly 28 hours for GT-GAN, with all experiments on an NVIDIA A100 GPU (Sikder et al., 2025). In the labs, log training and sampling energy separately with CodeCarbon.

### Open problems

- **Generalisation versus memorisation.** When does a diffusion model trained on a few thousand rows generalise instead of copying? Gu et al. (2025) and Fang et al. (2025) give partial answers.
- **Mixed types.** Separate Gaussian and multinomial processes (TabDDPM) compete with a learned latent space (TabSyn). The comparisons cited here come from the authors of the methods.
- **Few-step sampling.** DDIM, progressive distillation and denoising diffusion GANs were evaluated on images. Among the sources here, only TabSyn reports few-step sampling for tables.
- **Long sequences.** Attention cost grows with $n^2$; TransFusion reaches length 384.
- **Evaluating long sequences.** How should the classifier and predictor behind LDS and LPS be chosen and reported, so that scores are comparable across papers?

## Discussion questions

**Question 1.** Ho et al. (2020) replace the weighted bound with $L_\text{simple}$. Which noise levels gain weight, and why does this improve FID while worsening the bound? For a synthetic table that will be used to fit a downstream classifier, would you rather train on $L_\text{simple}$, the bound, or $L_\text{hybrid}$?

{{< spoiler text="Show a model answer" >}}
With $\sigma_t^2 = \beta_t$ and the linear schedule, the weight $\beta_t^2 / (2\sigma_t^2 \alpha_t (1-\bar{\alpha}_t))$ is about 0.5 at $t = 1$ and about 0.01 at large $t$. Dropping it therefore moves effort towards large $t$, where the network must recover coarse structure from heavy noise. Ho et al. find that this gives better samples (FID 3.17 against 13.51 on CIFAR-10), while the bound, which weights the small-$t$ terms that $L_\text{simple}$ neglects, gets slightly worse. For a downstream classifier, what matters is whether the joint distribution of features and label is right, and neither FID nor bits per dimension measures that directly (Theis et al., 2016). A defensible answer is to train with $L_\text{simple}$ or $L_\text{hybrid}$ and select by a utility measure from Lecture 4, while reporting the bound so that models stay comparable.
{{< /spoiler >}}

**Question 2.** Show that if a diffusion model learned the exact score of $q_t(x_t) = \frac{1}{n}\sum_{i=1}^{n} \mathcal{N}\big(x_t; \sqrt{\bar{\alpha}_t}\, x^{(i)}, (1-\bar{\alpha}_t) I\big)$, sampling would return training points. What, then, makes diffusion models generalise, and what does this imply for a synthetic dataset built from 2,000 patient records?

{{< spoiler text="Show a model answer" >}}
The reverse SDE and the probability flow ODE with the exact score reproduce the marginals of the forward process. At $t = 0$ that marginal is the empirical distribution, which puts all its mass on the $n$ training points, so every sample is a training point. Generalisation comes from approximation: limited capacity, the inductive bias of the network and finite training keep $s_\theta$ away from the exact empirical score. Gu et al. (2025) find that memorisation appears more readily on smaller datasets, and Fang et al. (2025) find that it grows with training epochs on tables. For 2,000 records you should therefore expect a real risk of near-copies, test for them (Lecture 5) and treat the number of epochs as a privacy-relevant choice, not only a utility one.
{{< /spoiler >}}

**Question 3.** You train a classifier-free guided diffusion model on a table and condition on a sensitive attribute with a small group. Predict what happens to the diversity of the generated rows for that group as $w$ grows, and design an experiment that would test your prediction.

{{< spoiler text="Show a hint" >}}
Use the implicit-classifier reading of guidance: a large $w$ pushes samples towards rows that a classifier would assign to the group with high confidence. Compare per-group statistics (marginals, within-group variance, coverage) of the real and synthetic data over a range of $w$, with several seeds. Lecture 4 gives you the metrics and Lecture 6 the fairness criteria.
{{< /spoiler >}}

**Question 4.** TransFusion reports a low LDS on a dataset. List three different generators that would all achieve a low LDS, and say which of them you would be willing to release. Which complementary measurements would separate them?

{{< spoiler text="Show a model answer" >}}
A generator that models the distribution well; a generator that copies the training sequences; and any generator evaluated with a classifier that is too weak or poorly trained to separate the two classes. Only the first is releasable. To separate them, check classifier capacity (for example its accuracy on a known easy pair), add a memorisation or membership test (Lecture 5), and add utility and diversity measures such as LPS, β-recall or coverage (Lecture 4).
{{< /spoiler >}}

**Question 5.** Compare GReaT and TabDDPM for a table with high-precision numerical columns and many categorical columns. Consider the likelihood each model defines, numerical precision, sampling cost and the privacy questions raised by a pretrained language model.

{{< spoiler text="Show a hint" >}}
GReaT defines a likelihood over the tokens of one serialisation and writes numbers as text; TabDDPM models numerical columns as continuous values after a quantile transformation and categorical columns with multinomial diffusion. Count network passes per row for each. For privacy, ask what the pretrained model already contains and whether fine-tuning on a small table can make it reproduce rows.
{{< /spoiler >}}

**Question 6.** For the dataset in your own project, which of the four families would you start with, given that the labs run on a laptop CPU? Justify the choice with the comparison table, and state the sampling budget (steps per sample and number of samples) you could afford.

## Further reading

- Luo, C. (2022). Understanding Diffusion Models: A Unified Perspective. [arXiv:2208.11970](https://arxiv.org/abs/2208.11970). A tutorial that derives diffusion models as Markovian hierarchical VAEs and shows the equivalence of predicting the clean input, the noise and the score.
- Song, Y., & Ermon, S. (2019). Generative Modeling by Estimating Gradients of the Data Distribution. *Advances in Neural Information Processing Systems*, 32. [Proceedings](https://proceedings.neurips.cc/paper/2019/hash/3001ef257407d5a371a96dcd947c7d93-Abstract.html). The score-based route to diffusion: noise at several levels and annealed Langevin dynamics.
- Nichol, A. Q., & Dhariwal, P. (2021). Improved Denoising Diffusion Probabilistic Models. *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139, 8162–8171. [PMLR](https://proceedings.mlr.press/v139/nichol21a.html). The cosine schedule, learned variances and competitive likelihoods.
- Karras, T., Aittala, M., Aila, T., & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. *Advances in Neural Information Processing Systems*, 35, 26565–26577. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2022/hash/a98846e9d9cc01cfb87eb694d946ce6b-Abstract-Conference.html). Separates the sampling process, the training process and the preconditioning of the score network.
- Xiao, Z., Kreis, K., & Vahdat, A. (2022). Tackling the Generative Learning Trilemma with Denoising Diffusion GANs. *International Conference on Learning Representations*. [arXiv:2112.07804](https://arxiv.org/abs/2112.07804). The quality, coverage and speed trilemma behind the comparison table.
- Peebles, W., & Xie, S. (2023). Scalable Diffusion Models with Transformers. *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 4195–4205. [CVF](https://openaccess.thecvf.com/content/ICCV2023/html/Peebles_Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.html). A transformer backbone for latent diffusion.
- Kim, J., Lee, C., & Park, N. (2023). STaSy: Score-based Tabular data Synthesis. *International Conference on Learning Representations*. [arXiv:2210.04018](https://arxiv.org/abs/2210.04018). A score-based tabular model trained with self-paced learning and fine-tuning.
- Rasul, K., Seward, C., Schuster, I., & Vollgraf, R. (2021). Autoregressive Denoising Diffusion Models for Multivariate Probabilistic Time Series Forecasting. *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139, 8857–8868. [PMLR](https://proceedings.mlr.press/v139/rasul21a.html). TimeGrad, a diffusion baseline in the TransFusion experiments.
- Somepalli, G., Singla, V., Goldblum, M., Geiping, J., & Goldstein, T. (2023). Diffusion Art or Digital Forgery? Investigating Data Replication in Diffusion Models. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 6048–6058. [CVF](https://openaccess.thecvf.com/content/CVPR2023/html/Somepalli_Diffusion_Art_or_Digital_Forgery_Investigating_Data_Replication_in_Diffusion_CVPR_2023_paper.html). Detects replicated training content in generated images.
- Fang, Z., Jiang, Z., Chen, H., Li, X., & Li, J. (2025). Understanding and Mitigating Memorization in Diffusion Models for Tabular Data. *Proceedings of the 42nd International Conference on Machine Learning*, PMLR 267, 15976–16005. [PMLR](https://proceedings.mlr.press/v267/fang25f.html). Memorisation in tabular diffusion and the TabCutMix mitigation.

## References

- Alaa, A., van Breugel, B., Saveliev, E. S., & van der Schaar, M. (2022). How Faithful is your Synthetic Data? Sample-level Metrics for Evaluating and Auditing Generative Models. *Proceedings of the 39th International Conference on Machine Learning*, PMLR 162, 290–306. [PMLR](https://proceedings.mlr.press/v162/alaa22a.html)
- Borisov, V., Seßler, K., Leemann, T., Pawelczyk, M., & Kasneci, G. (2023). Language Models are Realistic Tabular Data Generators. *International Conference on Learning Representations*. [arXiv:2210.06280](https://arxiv.org/abs/2210.06280)
- Carlini, N., Hayes, J., Nasr, M., Jagielski, M., Sehwag, V., Tramèr, F., Balle, B., Ippolito, D., & Wallace, E. (2023). Extracting Training Data from Diffusion Models. *32nd USENIX Security Symposium*, 5253–5270. [USENIX](https://www.usenix.org/conference/usenixsecurity23/presentation/carlini)
- Carlini, N., Tramèr, F., Wallace, E., Jagielski, M., Herbert-Voss, A., Lee, K., Roberts, A., Brown, T., Song, D., Erlingsson, Ú., Oprea, A., & Raffel, C. (2021). Extracting Training Data from Large Language Models. *30th USENIX Security Symposium*, 2633–2650. [USENIX](https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting)
- Dhariwal, P., & Nichol, A. (2021). Diffusion Models Beat GANs on Image Synthesis. *Advances in Neural Information Processing Systems*, 34, 8780–8794. [Proceedings](https://proceedings.neurips.cc/paper/2021/hash/49ad23d1ec9fa4bd8d77d02681df5cfa-Abstract.html)
- Fang, Z., Jiang, Z., Chen, H., Li, X., & Li, J. (2025). Understanding and Mitigating Memorization in Diffusion Models for Tabular Data. *Proceedings of the 42nd International Conference on Machine Learning*, PMLR 267, 15976–16005. [PMLR](https://proceedings.mlr.press/v267/fang25f.html)
- Goodfellow, I. J., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A., & Bengio, Y. (2014). Generative Adversarial Nets. *Advances in Neural Information Processing Systems*, 27. [Proceedings](https://proceedings.neurips.cc/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html)
- Gu, X., Du, C., Pang, T., Li, C., Lin, M., & Wang, Y. (2025). On Memorization in Diffusion Models. *Transactions on Machine Learning Research*. [arXiv:2310.02664](https://arxiv.org/abs/2310.02664)
- Ho, J., Jain, A., & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. *Advances in Neural Information Processing Systems*, 33, 6840–6851. [Proceedings](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)
- Ho, J., & Salimans, T. (2022). Classifier-Free Diffusion Guidance. [arXiv:2207.12598](https://arxiv.org/abs/2207.12598). A short version appeared at the NeurIPS 2021 Workshop on Deep Generative Models and Downstream Applications.
- Hoogeboom, E., Nielsen, D., Jaini, P., Forré, P., & Welling, M. (2021). Argmax Flows and Multinomial Diffusion: Learning Categorical Distributions. *Advances in Neural Information Processing Systems*, 34, 12454–12465. [Proceedings](https://proceedings.neurips.cc/paper/2021/hash/67d96d458abdef21792e6d8e590244e7-Abstract.html)
- Hyvärinen, A. (2005). Estimation of Non-Normalized Statistical Models by Score Matching. *Journal of Machine Learning Research*, 6(24), 695–709. [JMLR](https://www.jmlr.org/papers/v6/hyvarinen05a.html)
- Karras, T., Aittala, M., Aila, T., & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. *Advances in Neural Information Processing Systems*, 35, 26565–26577. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2022/hash/a98846e9d9cc01cfb87eb694d946ce6b-Abstract-Conference.html)
- Kim, J., Lee, C., & Park, N. (2023). STaSy: Score-based Tabular data Synthesis. *International Conference on Learning Representations*. [arXiv:2210.04018](https://arxiv.org/abs/2210.04018)
- Kingma, D. P., & Welling, M. (2014). Auto-Encoding Variational Bayes. *International Conference on Learning Representations*. [arXiv:1312.6114](https://arxiv.org/abs/1312.6114)
- Kotelnikov, A., Baranchuk, D., Rubachev, I., & Babenko, A. (2023). TabDDPM: Modelling Tabular Data with Diffusion Models. *Proceedings of the 40th International Conference on Machine Learning*, PMLR 202, 17564–17579. [PMLR](https://proceedings.mlr.press/v202/kotelnikov23a.html)
- Luccioni, S., Jernite, Y., & Strubell, E. (2024). Power Hungry Processing: Watts Driving the Cost of AI Deployment? *Proceedings of the 2024 ACM Conference on Fairness, Accountability, and Transparency*, 85–99. [doi:10.1145/3630106.3658542](https://doi.org/10.1145/3630106.3658542)
- Luo, C. (2022). Understanding Diffusion Models: A Unified Perspective. [arXiv:2208.11970](https://arxiv.org/abs/2208.11970)
- Nichol, A. Q., & Dhariwal, P. (2021). Improved Denoising Diffusion Probabilistic Models. *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139, 8162–8171. [PMLR](https://proceedings.mlr.press/v139/nichol21a.html)
- Peebles, W., & Xie, S. (2023). Scalable Diffusion Models with Transformers. *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 4195–4205. [CVF](https://openaccess.thecvf.com/content/ICCV2023/html/Peebles_Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.html)
- Rasul, K., Seward, C., Schuster, I., & Vollgraf, R. (2021). Autoregressive Denoising Diffusion Models for Multivariate Probabilistic Time Series Forecasting. *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139, 8857–8868. [PMLR](https://proceedings.mlr.press/v139/rasul21a.html)
- Rombach, R., Blattmann, A., Lorenz, D., Esser, P., & Ommer, B. (2022). High-Resolution Image Synthesis With Latent Diffusion Models. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 10684–10695. [CVF](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html)
- Salimans, T., & Ho, J. (2022). Progressive Distillation for Fast Sampling of Diffusion Models. *International Conference on Learning Representations*. [arXiv:2202.00512](https://arxiv.org/abs/2202.00512)
- Sikder, M. F., Ramachandranpillai, R., & Heintz, F. (2025). TransFusion: Generating long, high fidelity time series using diffusion models with transformers. *Machine Learning with Applications*, 20, 100652. [doi:10.1016/j.mlwa.2025.100652](https://doi.org/10.1016/j.mlwa.2025.100652) · [arXiv:2307.12667](https://arxiv.org/abs/2307.12667)
- Sohl-Dickstein, J., Weiss, E., Maheswaranathan, N., & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. *Proceedings of the 32nd International Conference on Machine Learning*, PMLR 37, 2256–2265. [PMLR](https://proceedings.mlr.press/v37/sohl-dickstein15.html)
- Sohn, K., Yan, X., & Lee, H. (2015). Learning Structured Output Representation using Deep Conditional Generative Models. *Advances in Neural Information Processing Systems*, 28. [Proceedings](https://proceedings.neurips.cc/paper/2015/hash/8d55a249e6baa5c06772297520da2051-Abstract.html)
- Somepalli, G., Singla, V., Goldblum, M., Geiping, J., & Goldstein, T. (2023). Diffusion Art or Digital Forgery? Investigating Data Replication in Diffusion Models. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 6048–6058. [CVF](https://openaccess.thecvf.com/content/CVPR2023/html/Somepalli_Diffusion_Art_or_Digital_Forgery_Investigating_Data_Replication_in_Diffusion_CVPR_2023_paper.html)
- Song, J., Meng, C., & Ermon, S. (2021). Denoising Diffusion Implicit Models. *International Conference on Learning Representations*. [arXiv:2010.02502](https://arxiv.org/abs/2010.02502)
- Song, Y., & Ermon, S. (2019). Generative Modeling by Estimating Gradients of the Data Distribution. *Advances in Neural Information Processing Systems*, 32. [Proceedings](https://proceedings.neurips.cc/paper/2019/hash/3001ef257407d5a371a96dcd947c7d93-Abstract.html)
- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S., & Poole, B. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. *International Conference on Learning Representations*. [arXiv:2011.13456](https://arxiv.org/abs/2011.13456)
- Tashiro, Y., Song, J., Song, Y., & Ermon, S. (2021). CSDI: Conditional Score-based Diffusion Models for Probabilistic Time Series Imputation. *Advances in Neural Information Processing Systems*, 34, 24804–24816. [Proceedings](https://proceedings.neurips.cc/paper/2021/hash/cfe8504bda37b575c70ee1a8276f3486-Abstract.html)
- Theis, L., van den Oord, A., & Bethge, M. (2016). A note on the evaluation of generative models. *International Conference on Learning Representations*. [arXiv:1511.01844](https://arxiv.org/abs/1511.01844)
- van den Burg, G. J. J., & Williams, C. K. I. (2021). On Memorization in Probabilistic Deep Generative Models. *Advances in Neural Information Processing Systems*, 34, 27916–27928. [Proceedings](https://proceedings.neurips.cc/paper/2021/hash/eae15aabaa768ae4a5993a8a4f4fa6e4-Abstract.html)
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is All you Need. *Advances in Neural Information Processing Systems*, 30. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)
- Vincent, P. (2011). A Connection Between Score Matching and Denoising Autoencoders. *Neural Computation*, 23(7), 1661–1674. [doi:10.1162/NECO_a_00142](https://doi.org/10.1162/NECO_a_00142)
- Xiao, Z., Kreis, K., & Vahdat, A. (2022). Tackling the Generative Learning Trilemma with Denoising Diffusion GANs. *International Conference on Learning Representations*. [arXiv:2112.07804](https://arxiv.org/abs/2112.07804)
- Xu, L., Skoularidou, M., Cuesta-Infante, A., & Veeramachaneni, K. (2019). Modeling Tabular data using Conditional GAN. *Advances in Neural Information Processing Systems*, 32. [Proceedings](https://proceedings.neurips.cc/paper/2019/hash/254ed7d2de3b23ab10936522dd547b78-Abstract.html)
- Yoon, J., Jarrett, D., & van der Schaar, M. (2019). Time-series Generative Adversarial Networks. *Advances in Neural Information Processing Systems*, 32. [Proceedings](https://proceedings.neurips.cc/paper/2019/hash/c9efe5f26cd17ba6216bbe2a7d26d490-Abstract.html)
- Yuan, X., & Qiao, Y. (2024). Diffusion-TS: Interpretable Diffusion for General Time Series Generation. *International Conference on Learning Representations*. [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/b5b66077d016c037576cc56a82f97f66-Abstract-Conference.html)
- Zhang, H., Zhang, J., Srinivasan, B., Shen, Z., Qin, X., Faloutsos, C., Rangwala, H., & Karypis, G. (2024). Mixed-Type Tabular Data Synthesis with Score-based Diffusion in Latent Space. *International Conference on Learning Representations*. [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9750610639c3e7a849cff746bf60dbd-Abstract-Conference.html)

You train TransFusion on time-series data in [Lab 1](../../04-labs/lab-1/).
