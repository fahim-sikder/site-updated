---
title: Paper seminars
weight: 50
---

The course has two paper seminars of 2 hours each. In the seminars, each participant leads the discussion of one paper, with a short summary and questions for the group. Leading one discussion is part of the [examination](../07-examination/).

The papers come from the pools below. The course leader assigns each participant one paper at the start of the course, when you receive the full reading list. Read every paper that is discussed in your seminar, not only your own, so that the group can discuss them.

## Paper seminar 1: generative model families {#paper-seminar-1-generative-model-families}

These papers extend Lecture 2 (VAEs and GANs) and Lecture 3 (diffusion models, transformers and basics of LLMs). Each one changes a training objective, an architecture or a sampling procedure; ask what that change does to the synthetic data (ILO1).

| # | Paper | Theme |
|:-:|---|---|
| 1 | Arjovsky, M., Chintala, S., & Bottou, L. (2017). Wasserstein Generative Adversarial Networks. *ICML*, PMLR 70, 214–223. [PMLR](https://proceedings.mlr.press/v70/arjovsky17a.html) | GAN objectives |
| 2 | Lin, Z., Khetan, A., Fanti, G., & Oh, S. (2018). PacGAN: The power of two samples in generative adversarial networks. *NeurIPS*, 31. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2018/hash/288cc0ff022877bd3df94bc9360b9c5d-Abstract.html) | Mode collapse |
| 3 | Lucic, M., Kurach, K., Michalski, M., Gelly, S., & Bousquet, O. (2018). Are GANs Created Equal? A Large-Scale Study. *NeurIPS*, 31. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2018/hash/e46de7e1bcaaced9a54f1e9d0d2f800d-Abstract.html) | Comparing GANs fairly |
| 4 | Lucas, J., Tucker, G., Grosse, R., & Norouzi, M. (2019). Don't Blame the ELBO! A Linear VAE Perspective on Posterior Collapse. *NeurIPS*, 32. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2019/hash/7e3315fe390974fcf25e44a9445bd821-Abstract.html) | VAE objectives |
| 5 | Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S., & Poole, B. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. *ICLR 2021*. [arXiv:2011.13456](https://arxiv.org/abs/2011.13456) | Diffusion theory |
| 6 | Song, J., Meng, C., & Ermon, S. (2021). Denoising Diffusion Implicit Models. *ICLR 2021*. [arXiv:2010.02502](https://arxiv.org/abs/2010.02502) | Fast sampling |
| 7 | Kotelnikov, A., Baranchuk, D., Rubachev, I., & Babenko, A. (2023). TabDDPM: Modelling Tabular Data with Diffusion Models. *ICML*, PMLR 202, 17564–17579. [PMLR](https://proceedings.mlr.press/v202/kotelnikov23a.html) | Tabular diffusion |
| 8 | Zhang, H., Zhang, J., Srinivasan, B., Shen, Z., Qin, X., Faloutsos, C., Rangwala, H., & Karypis, G. (2024). Mixed-Type Tabular Data Synthesis with Score-based Diffusion in Latent Space. *ICLR 2024*. [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9750610639c3e7a849cff746bf60dbd-Abstract-Conference.html) | Latent tabular diffusion |
| 9 | Borisov, V., Seßler, K., Leemann, T., Pawelczyk, M., & Kasneci, G. (2023). Language Models are Realistic Tabular Data Generators. *ICLR 2023*. [arXiv:2210.06280](https://arxiv.org/abs/2210.06280) | Transformers for tables |
| 10 | Tashiro, Y., Song, J., Song, Y., & Ermon, S. (2021). CSDI: Conditional Score-based Diffusion Models for Probabilistic Time Series Imputation. *NeurIPS*, 34, 24804–24816. [Proceedings](https://proceedings.neurips.cc/paper/2021/hash/cfe8504bda37b575c70ee1a8276f3486-Abstract.html) | Time-series diffusion |
| 11 | Yuan, X., & Qiao, Y. (2024). Diffusion-TS: Interpretable Diffusion for General Time Series Generation. *ICLR 2024*. [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/b5b66077d016c037576cc56a82f97f66-Abstract-Conference.html) | Time-series diffusion |
| 12 | van den Burg, G., & Williams, C. (2021). On Memorization in Probabilistic Deep Generative Models. *NeurIPS*, 34, 27916–27928. [Proceedings](https://proceedings.neurips.cc/paper/2021/hash/eae15aabaa768ae4a5993a8a4f4fa6e4-Abstract.html) | Memorisation |

## Paper seminar 2: privacy and fairness {#paper-seminar-2-privacy-and-fairness}

These papers extend Lecture 5 (privacy) and Lecture 6 (fairness), and several of them study both at once. For each paper, ask what it implies for the decision to release a synthetic dataset (ILO3).

| # | Paper | Theme |
|:-:|---|---|
| 1 | van Breugel, B., Sun, H., Qian, Z., & van der Schaar, M. (2023). Membership Inference Attacks against Synthetic Data through Overfitting Detection. *AISTATS*, PMLR 206, 3493–3514. [PMLR](https://proceedings.mlr.press/v206/breugel23a.html) | Membership inference |
| 2 | Ganev, G., & De Cristofaro, E. (2025). The Inadequacy of Similarity-based Privacy Metrics: Privacy Attacks against "Truly Anonymous" Synthetic Datasets. *IEEE Symposium on Security and Privacy*. [arXiv:2312.05114](https://arxiv.org/abs/2312.05114) | Similarity metrics |
| 3 | Annamalai, M. S. M. S., Gadotti, A., & Rocher, L. (2024). A Linear Reconstruction Approach for Attribute Inference Attacks against Synthetic Data. *33rd USENIX Security Symposium*, 2351–2368. [USENIX](https://www.usenix.org/conference/usenixsecurity24/presentation/annamalai) | Attribute inference |
| 4 | Carlini, N., Hayes, J., Nasr, M., Jagielski, M., Sehwag, V., Tramèr, F., Balle, B., Ippolito, D., & Wallace, E. (2023). Extracting Training Data from Diffusion Models. *32nd USENIX Security Symposium*, 5253–5270. [USENIX](https://www.usenix.org/conference/usenixsecurity23/presentation/carlini) | Memorisation and extraction |
| 5 | McKenna, R., Mullins, B., Sheldon, D., & Miklau, G. (2022). AIM: An Adaptive and Iterative Mechanism for Differentially Private Synthetic Data. *Proceedings of the VLDB Endowment*, 15(11), 2599–2612. [doi:10.14778/3551793.3551817](https://doi.org/10.14778/3551793.3551817) | DP synthetic data |
| 6 | Ganev, G., Annamalai, M. S. M. S., & De Cristofaro, E. (2025). The Elusive Pursuit of Reproducing PATE-GAN: Benchmarking, Auditing, Debugging. *Transactions on Machine Learning Research*. [arXiv:2406.13985](https://arxiv.org/abs/2406.13985) | Auditing DP code |
| 7 | Ganev, G., Oprisanu, B., & De Cristofaro, E. (2022). Robin Hood and Matthew Effects: Differential Privacy Has Disparate Impact on Synthetic Data. *ICML*, PMLR 162, 6944–6959. [PMLR](https://proceedings.mlr.press/v162/ganev22a.html) | Privacy and fairness |
| 8 | Cheng, V., Suriyakumar, V. M., Dullerud, N., Joshi, S., & Ghassemi, M. (2021). Can You Fake It Until You Make It? Impacts of Differentially Private Synthetic Data on Downstream Classification Fairness. *FAccT 2021*, 149–160. [doi:10.1145/3442188.3445879](https://doi.org/10.1145/3442188.3445879) | Privacy and fairness |
| 9 | van Breugel, B., Kyono, T., Berrevoets, J., & van der Schaar, M. (2021). DECAF: Generating Fair Synthetic Data Using Causally-Aware Generative Networks. *NeurIPS*, 34, 22221–22233. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2021/hash/ba9fab001f67381e56e410575874d967-Abstract.html) | Fair generation |
| 10 | Wyllie, S., Shumailov, I., & Papernot, N. (2024). Fairness Feedback Loops: Training on Synthetic Data Amplifies Bias. *FAccT 2024*, 2113–2147. [doi:10.1145/3630106.3659029](https://doi.org/10.1145/3630106.3659029) | Bias amplification |
| 11 | Bhanot, K., Qi, M., Erickson, J. S., Guyon, I., & Bennett, K. P. (2021). The Problem of Fairness in Synthetic Healthcare Data. *Entropy*, 23(9), 1165. [doi:10.3390/e23091165](https://doi.org/10.3390/e23091165) | Fairness in health data |
| 12 | van Breugel, B., Qian, Z., & van der Schaar, M. (2023). Synthetic Data, Real Errors: How (Not) to Publish and Use Synthetic Data. *ICML*, PMLR 202, 34793–34808. [PMLR](https://proceedings.mlr.press/v202/van-breugel23a.html) | Publishing synthetic data |

## Leading a discussion

{{% steps %}}

### Read the paper closely

Read your paper twice: once for its argument, once for its assumptions, its evaluation and what it leaves out.

### Prepare a short summary

Summarise the problem the paper addresses, its method and its main results. Connect it to the lecture it extends.

### Prepare questions for the group

Write questions that open a discussion, for example on the paper's assumptions, its threat model or fairness definition, its evaluation, or what it means for a dataset you work with.

### Lead the discussion

Present your summary, then lead the group through your questions.

{{% /steps %}}
