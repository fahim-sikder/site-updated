---
title: Reading list
weight: 80
---

The course literature mainly consists of peer-reviewed research articles, with selected book chapters and regulatory guidance. This page collects the required reading for every lecture.

> [!NOTE]
> The reading list changes with each course run, since generative modelling moves quickly.

## Required reading by lecture

Read these before the lecture.

### Lecture 1: Why synthetic data?

- Jordon, James, Lukasz Szpruch, Florimond Houssiau, Mirko Bottarelli, Giovanni Cherubin, Carsten Maple, Samuel N. Cohen, and Adrian Weller. 2022. “Synthetic Data -- What, Why and How?” [Link](https://arxiv.org/abs/2205.03257)
- Stadler, Theresa, Bristena Oprisanu, and Carmela Troncoso. 2022. “Synthetic Data – Anonymisation Groundhog Day.” Pp. 1451–68 in 31st USENIX Security Symposium (USENIX Security 22). Boston, MA: USENIX Association. [Link](https://www.usenix.org/conference/usenixsecurity22/presentation/stadler)
- European Data Protection Board (2026). Guidelines 02/2026 on Anonymisation, version 1.0. [PDF](https://www.edpb.europa.eu/system/files_en?file=2026-09/edpb_guidelines_202602_anonymisation_v1_en_0.pdf)

### Lecture 2: VAEs and GANs

- Kingma, Diederik P., and Max Welling. 2013. “Auto-Encoding Variational Bayes.”, [Link](https://arxiv.org/abs/1312.6114)
- Goodfellow, Ian J., Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. 2014. “Generative Adversarial Nets.” in Advances in Neural Information Processing Systems. Vol. 27. Curran Associates, Inc. [Link](https://papers.nips.cc/paper_files/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html)
- Xu, Lei, Maria Skoularidou, Alfredo Cuesta-Infante, and Kalyan Veeramachaneni. 2019. “Modeling Tabular Data Using Conditional GAN.” in Advances in Neural Information Processing Systems. Vol. 32. Curran Associates, Inc. [Link](https://proceedings.neurips.cc/paper_files/paper/2019/hash/254ed7d2de3b23ab10936522dd547b78-Abstract.html)
- Arjovsky, Martin, Soumith Chintala, and Léon Bottou. 2017. “Wasserstein Generative Adversarial Networks.” Pp. 214–23 in Proceedings of the 34th International Conference on Machine Learning. PMLR. [Link](https://proceedings.mlr.press/v70/arjovsky17a.html)
- Yoon, Jinsung, Daniel Jarrett, and Mihaela van der Schaar. 2019. “Time-Series Generative Adversarial Networks.” in Advances in Neural Information Processing Systems. Vol. 32. Curran Associates, Inc. [Link](https://proceedings.neurips.cc/paper_files/paper/2019/hash/c9efe5f26cd17ba6216bbe2a7d26d490-Abstract.html)

### Lecture 3: Diffusion models, transformers and basics of LLMs

- Ho, Jonathan, Ajay Jain, and Pieter Abbeel. 2020. “Denoising Diffusion Probabilistic Models.” Pp. 6840–51 in Advances in Neural Information Processing Systems. Vol. 33. Curran Associates, Inc. [Link](https://proceedings.neurips.cc/paper_files/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)
- Vaswani, Ashish, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. “Attention Is All You Need.” in Advances in Neural Information Processing Systems. Vol. 30. Curran Associates, Inc. [Link](https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)
- Sikder, Md Fahim, Resmi Ramachandranpillai, and Fredrik Heintz. 2025. “TransFusion: Generating Long, High Fidelity Time Series Using Diffusion Models with Transformers.” Machine Learning with Applications 100652. doi:10.1016/j.mlwa.2025.100652. [Link](https://www.sciencedirect.com/science/article/pii/S2666827025000350)
- Shumailov, Ilia, Zakhar Shumaylov, Yiren Zhao, Nicolas Papernot, Ross Anderson, and Yarin Gal. 2024. “AI Models Collapse When Trained on Recursively Generated Data.” Nature 631(8022):755–59. doi:10.1038/s41586-024-07566-y. [Link](https://www.nature.com/articles/s41586-024-07566-y)
- Bender, Emily M., Timnit Gebru, Angelina McMillan-Major, and Shmargaret Shmitchell. 2021. “On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? 🦜.” Pp. 610–23 in Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency. Virtual Event Canada: ACM. [Link](https://dl.acm.org/doi/abs/10.1145/3442188.3445922)



### Lecture 4: Evaluating synthetic data: fidelity and utility

- Alaa, Ahmed, Boris Van Breugel, Evgeny S. Saveliev, and Mihaela van der Schaar. 2022. “How Faithful Is Your Synthetic Data? Sample-Level Metrics for Evaluating and Auditing Generative Models.” Pp. 290–306 in Proceedings of the 39th International Conference on Machine Learning. PMLR. [Link](https://proceedings.mlr.press/v162/alaa22a.html)
- Weerts, Hilde, Miroslav Dudík, Richard Edgar, Adrin Jalali, Roman Lutz, and Michael Madaio. 2023. “Fairlearn: Assessing and Improving Fairness of AI Systems.” Journal of Machine Learning Research 24(257):1–8. [Link](https://www.jmlr.org/papers/v24/23-0389.html)
- Sikder, Md Fahim, Resmi Ramachandranpillai, Daniel de Leng, and Fredrik Heintz. 2024. “FairX: A Comprehensive Benchmarking Tool for Model Analysis Using Fairness, Utility, and Explainability.” in Proceedings of the 2nd Workshop on Fairness and Bias in AI. Vol. 3808, CEUR Workshop Proceedings, edited by R. Calegari, V. Dignum, and B. O’Sullivan. Santiago de Compostela, Spain: CEUR. [Link](https://ceur-ws.org/Vol-3808/paper16.pdf)

### Lecture 5: Privacy: differential privacy and attacks

- Abadi, Martin, Andy Chu, Ian Goodfellow, H. Brendan McMahan, Ilya Mironov, Kunal Talwar, and Li Zhang. 2016. “Deep Learning with Differential Privacy.” Pp. 308–18 in Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security. Vienna Austria: ACM. [Link](https://dl.acm.org/doi/abs/10.1145/2976749.2978318)
- Jordon, James, Jinsung Yoon, and Mihaela van der Schaar. 2018. “PATE-GAN: Generating Synthetic Data with Differential Privacy Guarantees.” [Link](https://openreview.net/forum?id=S1zk9iRqF7)
- Zhang, Zhikun, Tianhao Wang, Ninghui Li, Jean Honorio, Michael Backes, Shibo He, Jiming Chen, and Yang Zhang. 2021. “PrivSyn: Differentially Private Data Synthesis.” Pp. 929–46 in 30th USENIX security symposium (USENIX security 21). USENIX Association. [Link](https://www.usenix.org/conference/usenixsecurity21/presentation/zhang-zhikun)
- McKenna, Ryan, Gerome Miklau, and Daniel Sheldon. 2021. “Winning the NIST Contest: A Scalable and General Approach to Differentially Private Synthetic Data.” Journal of Privacy and Confidentiality 11(3). doi:10.29012/jpc.778. [Link](https://journalprivacyconfidentiality.org/index.php/jpc/article/view/778)

### Lecture 6: Fairness in synthetic data

- Xu, Depeng, Shuhan Yuan, Lu Zhang, and Xintao Wu. 2018. “FairGAN: Fairness-Aware Generative Adversarial Networks.” Pp. 570–75 in 2018 IEEE International Conference on Big Data (Big Data). Seattle, WA, USA: IEEE. [Link](https://ieeexplore.ieee.org/abstract/document/8622525)
- Choi, Kristy, Aditya Grover, Trisha Singh, Rui Shu, and Stefano Ermon. 2020. “Fair Generative Modeling via Weak Supervision.” Pp. 1887–98 in Proceedings of the 37th International Conference on Machine Learning. PMLR. [Link](https://proceedings.mlr.press/v119/choi20a.html)
- Friedrich, Felix, Manuel Brack, Lukas Struppek, Dominik Hintersdorf, Patrick Schramowski, Sasha Luccioni, and Kristian Kersting. 2025. “Auditing and Instructing Text-to-Image Generation Models on Fairness.” AI and Ethics 5(3):2103–23. doi:10.1007/s43681-024-00531-5. [Link](https://link.springer.com/article/10.1007/s43681-024-00531-5)
- Ramachandranpillai, Resmi, Md Fahim Sikder, David Bergström, and Fredrik Heintz. 2024. “Bt-GAN: Generating Fair Synthetic Healthdata via Bias-Transforming Generative Adversarial Networks.” Journal of Artificial Intelligence Research 79:1313–41. doi:10.1613/jair.1.15317. [Link](/publications/bias-transforming-gan/)
