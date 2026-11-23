---
title: Reading list
weight: 80
---

The course literature mainly consists of peer-reviewed research articles, with selected book chapters and regulatory guidance. This page collects the required reading for every lecture, the paper pools for the two [paper seminars](../05-paper-seminars/) and background reading by topic.

> [!NOTE]
> The reading list changes with each course run, since generative modelling moves quickly.

## Required reading by lecture

Read these before the lecture.

### Lecture 1: Why synthetic data?

- Jordon, James, Lukasz Szpruch, Florimond Houssiau, Mirko Bottarelli, Giovanni Cherubin, Carsten Maple, Samuel N. Cohen, and Adrian Weller. 2022. “Synthetic Data -- What, Why and How?” [Link](https://arxiv.org/abs/2205.03257)
- Stadler, Theresa, Bristena Oprisanu, and Carmela Troncoso. 2022. “Synthetic Data – Anonymisation Groundhog Day.” Pp. 1451–68 in 31st USENIX Security Symposium (USENIX Security 22). Boston, MA: USENIX Association. [Link](https://www.usenix.org/conference/usenixsecurity22/presentation/stadler)
- European Data Protection Board (2026). Guidelines 02/2026 on Anonymisation, version 1.0. [PDF](https://www.edpb.europa.eu/system/files_en?file=2026-09/edpb_guidelines_202602_anonymisation_v1_en_0.pdf)

### Lecture 2: VAEs and GANs

- Kingma, Diederik P., and Max Welling. 2022. “Auto-Encoding Variational Bayes.”, ICLR 2014 [Link](https://arxiv.org/abs/1312.6114)
- Goodfellow, Ian J., Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. 2014. “Generative Adversarial Nets.” in Advances in Neural Information Processing Systems. Vol. 27. Curran Associates, Inc. [Link](https://papers.nips.cc/paper_files/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html)
- Xu, Lei, Maria Skoularidou, Alfredo Cuesta-Infante, and Kalyan Veeramachaneni. 2019. “Modeling Tabular Data Using Conditional GAN.” in Advances in Neural Information Processing Systems. Vol. 32. Curran Associates, Inc. [Link](https://proceedings.neurips.cc/paper_files/paper/2019/hash/254ed7d2de3b23ab10936522dd547b78-Abstract.html)
- Yoon, Jinsung, Daniel Jarrett, and Mihaela van der Schaar. 2019. “Time-Series Generative Adversarial Networks.” in Advances in Neural Information Processing Systems. Vol. 32. Curran Associates, Inc. [Link](https://proceedings.neurips.cc/paper_files/paper/2019/hash/c9efe5f26cd17ba6216bbe2a7d26d490-Abstract.html)

### Lecture 3: Diffusion models, transformers and basics of LLMs

- Ho, Jonathan, Ajay Jain, and Pieter Abbeel. 2020. “Denoising Diffusion Probabilistic Models.” Pp. 6840–51 in Advances in Neural Information Processing Systems. Vol. 33. Curran Associates, Inc. [Link](https://proceedings.neurips.cc/paper_files/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is All you Need. *Advances in Neural Information Processing Systems*, 30. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Sikder, M. F., Ramachandranpillai, R., & Heintz, F. (2025). TransFusion: Generating long, high fidelity time series using diffusion models with transformers. *Machine Learning with Applications*, 20, 100652. [doi:10.1016/j.mlwa.2025.100652](https://doi.org/10.1016/j.mlwa.2025.100652) · [arXiv:2307.12667](https://arxiv.org/abs/2307.12667) · [Publication page](/publications/diffusion-time-series/)

### Lecture 4: Evaluating synthetic data: fidelity and utility

- Alaa, A., van Breugel, B., Saveliev, E. S., & van der Schaar, M. (2022). How Faithful is your Synthetic Data? Sample-level Metrics for Evaluating and Auditing Generative Models. *Proceedings of the 39th International Conference on Machine Learning*, PMLR 162, 290–306. [PMLR](https://proceedings.mlr.press/v162/alaa22a.html) · [arXiv:2102.08921](https://arxiv.org/abs/2102.08921)
- Sikder, M. F., Ramachandranpillai, R., de Leng, D., & Heintz, F. (2024). FairX: A comprehensive benchmarking tool for model analysis using fairness, utility, and explainability. *Proceedings of the 2nd Workshop on Fairness and Bias in AI (AEQUITAS 2024), co-located with ECAI 2024*, CEUR Workshop Proceedings, Vol. 3808. [PDF](https://ceur-ws.org/Vol-3808/paper16.pdf) · [arXiv:2406.14281](https://arxiv.org/abs/2406.14281) · [Publication page](/publications/fairx/)

### Lecture 5: Privacy: differential privacy and attacks

- Dwork, C., & Roth, A. (2014). The Algorithmic Foundations of Differential Privacy. *Foundations and Trends in Theoretical Computer Science*, 9(3–4), 211–407. [doi:10.1561/0400000042](https://doi.org/10.1561/0400000042)
- Jordon, J., Yoon, J., & van der Schaar, M. (2019). PATE-GAN: Generating Synthetic Data with Differential Privacy Guarantees. *International Conference on Learning Representations (ICLR 2019)*. [OpenReview](https://openreview.net/forum?id=S1zk9iRqF7)
- Zhang, Z., Wang, T., Li, N., Honorio, J., Backes, M., He, S., Chen, J., & Zhang, Y. (2021). PrivSyn: Differentially Private Data Synthesis. *30th USENIX Security Symposium*, 929–946. [USENIX](https://www.usenix.org/conference/usenixsecurity21/presentation/zhang-zhikun)

### Lecture 6: Fairness in synthetic data

- Ramachandranpillai, R., Sikder, M. F., Bergström, D., & Heintz, F. (2024). Bt-GAN: Generating Fair Synthetic Healthdata via Bias-transforming Generative Adversarial Networks. *Journal of Artificial Intelligence Research*, 79, 1313–1341. [doi:10.1613/jair.1.15317](https://doi.org/10.1613/jair.1.15317) · [Publication page](/publications/bias-transforming-gan/)
- Sikder, M. F., Ramachandranpillai, R., de Leng, D., & Heintz, F. (2024). FairX (see Lecture 4).

### Guest lecture: synthetic data

The background reading follows once the guest lecturer is confirmed.

## Paper seminars

The [paper seminars page](../05-paper-seminars/) lists the paper pools for seminar 1 (generative model families) and seminar 2 (privacy and fairness).

## Background reading by topic

### Books, monographs and tutorials

- Barocas, S., Hardt, M., & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. [fairmlbook.org](https://fairmlbook.org/)
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Microsoft Research](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/)
- Drechsler, J. (2011). *Synthetic Datasets for Statistical Disclosure Control: Theory and Implementation*. Lecture Notes in Statistics, Vol. 201. Springer. [doi:10.1007/978-1-4614-0326-5](https://doi.org/10.1007/978-1-4614-0326-5)
- Goodfellow, I. (2016). NIPS 2016 Tutorial: Generative Adversarial Networks. *arXiv:1701.00160*. [arXiv](https://arxiv.org/abs/1701.00160)
- Kingma, D. P., & Welling, M. (2019). An Introduction to Variational Autoencoders. *Foundations and Trends in Machine Learning*, 12(4), 307–392. [doi:10.1561/2200000056](https://doi.org/10.1561/2200000056) · [arXiv:1906.02691](https://arxiv.org/abs/1906.02691)
- Luo, C. (2022). Understanding Diffusion Models: A Unified Perspective. *arXiv:2208.11970*. [arXiv](https://arxiv.org/abs/2208.11970)
- Ponomareva, N., et al. (2023). How to DP-fy ML: A Practical Guide to Machine Learning with Differential Privacy. *Journal of Artificial Intelligence Research*, 77, 1113–1201. [doi:10.1613/jair.1.14649](https://doi.org/10.1613/jair.1.14649)

### Law, regulation and guidance

- Regulation (EU) 2016/679 (General Data Protection Regulation). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- Regulation (EU) 2024/1689 (Artificial Intelligence Act). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- Regulation (EU) 2026/1744 amending Regulation (EU) 2024/1689 (Digital Omnibus on AI). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2026/1744/oj)
- Regulation (EU) 2025/327 (European Health Data Space). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2025/327/oj)
- Article 29 Data Protection Working Party (2014). Opinion 05/2014 on Anonymisation Techniques (WP216). [PDF](https://ec.europa.eu/justice/article-29/documentation/opinion-recommendation/files/2014/wp216_en.pdf)
- Near, J. P., Darais, D., Lefkovitz, N., & Howarth, G. S. (2025). *Guidelines for Evaluating Differential Privacy Guarantees*. NIST Special Publication 800-226. [doi:10.6028/NIST.SP.800-226](https://doi.org/10.6028/NIST.SP.800-226)

### Origins in statistical disclosure control

- Rubin, D. B. (1993). Discussion: Statistical Disclosure Limitation. *Journal of Official Statistics*, 9(2), 461–468. [PDF](https://www.scb.se/contentassets/ca21efb41fee47d293bbee5bf7be7fb3/discussion-statistical-disclosure-limitation2.pdf)
- Little, R. J. A. (1993). Statistical Analysis of Masked Data. *Journal of Official Statistics*, 9(2), 407–426. [PDF](https://www.scb.se/contentassets/ca21efb41fee47d293bbee5bf7be7fb3/statistical-analysis-of-masked-data.pdf)
- Raghunathan, T. E., Reiter, J. P., & Rubin, D. B. (2003). Multiple Imputation for Statistical Disclosure Limitation. *Journal of Official Statistics*, 19(1), 1–16. [PDF](https://www.scb.se/contentassets/ca21efb41fee47d293bbee5bf7be7fb3/multiple-imputation-for-statistical-disclosure-limitation.pdf)

### Evaluation and benchmarks

- Qian, Z., Davis, R., & van der Schaar, M. (2023). Synthcity: a benchmark framework for diverse use cases of tabular synthetic data. *Advances in Neural Information Processing Systems*, 36, Datasets and Benchmarks Track. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2023/hash/09723c9f291f6056fd1885081859c186-Abstract-Datasets_and_Benchmarks.html)
- Snoke, J., Raab, G. M., Nowok, B., Dibben, C., & Slavković, A. (2018). General and specific utility measures for synthetic data. *Journal of the Royal Statistical Society Series A*, 181(3), 663–688. [doi:10.1111/rssa.12358](https://doi.org/10.1111/rssa.12358)
- Theis, L., van den Oord, A., & Bethge, M. (2016). A note on the evaluation of generative models. *International Conference on Learning Representations (ICLR 2016)*. [arXiv:1511.01844](https://arxiv.org/abs/1511.01844)

### Energy use of machine learning

- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D., & Pineau, J. (2020). Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning. *Journal of Machine Learning Research*, 21(248), 1–43. [JMLR](https://jmlr.org/papers/v21/20-312.html)
- Lacoste, A., Luccioni, A., Schmidt, V., & Dandres, T. (2019). Quantifying the Carbon Emissions of Machine Learning. *arXiv:1910.09700*. [arXiv](https://arxiv.org/abs/1910.09700)
- Luccioni, S., Jernite, Y., & Strubell, E. (2024). Power Hungry Processing: Watts Driving the Cost of AI Deployment? *Proceedings of the 2024 ACM Conference on Fairness, Accountability, and Transparency (FAccT '24)*, 85–99. [doi:10.1145/3630106.3658542](https://doi.org/10.1145/3630106.3658542)
- Strubell, E., Ganesh, A., & McCallum, A. (2019). Energy and Policy Considerations for Deep Learning in NLP. *Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics*, 3645–3650. [ACL Anthology](https://aclanthology.org/P19-1355/)
- CodeCarbon documentation: methodology. [docs.codecarbon.io](https://docs.codecarbon.io/latest/explanation/methodology/)

### Work by the examiner on these topics

- Ramachandranpillai, R., Sikder, M. F., & Heintz, F. (2023). Fair Latent Deep Generative Models (FLDGMs) for Syntax-Agnostic and Fair Synthetic Data Generation. *ECAI 2023*, Frontiers in Artificial Intelligence and Applications, Vol. 372, 1938–1945. [doi:10.3233/FAIA230484](https://doi.org/10.3233/FAIA230484) · [Publication page](/publications/fair-latent-generative-models/)
- Sikder, M. F., Ramachandranpillai, R., de Leng, D., & Heintz, F. (2025). Promoting Intersectional Fairness Through Knowledge Distillation. *ECAI 2025*, Frontiers in Artificial Intelligence and Applications, Vol. 413, 3427–3434. [doi:10.3233/FAIA251214](https://doi.org/10.3233/FAIA251214) · [Publication page](/publications/promoting-intersectional-fainress/)
- Bt-GAN, FairX and TransFusion appear in the required reading above.
