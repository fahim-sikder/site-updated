---
title: "Guest lecture: Synthetic data in healthcare"
linkTitle: "Guest lecture: Healthcare"
weight: 37
---

**Week 8** · 2 hours · Learning outcome [LO3](../../01-about/#learning-outcomes)

**Guest lecturer:** to be confirmed.

The guest lecture is about synthetic data for health data. Health records are among the most restricted data in research. Data concerning health is a special category under Article 9 of the GDPR, and the European Health Data Space Regulation sets new rules for its secondary use (see [Lecture 1](../lecture-1/#health-data-and-the-european-health-data-space)). The lecture looks at how researchers make and use synthetic health data, and at the privacy and fairness risks of releasing it.

## Background reading

Read at least two of these before the lecture.

- Chen, R. J., Lu, M. Y., Chen, T. Y., Williamson, D. F. K., & Mahmood, F. (2021). Synthetic data in machine learning for medicine and healthcare. *Nature Biomedical Engineering*, 5(6), 493–497. [doi:10.1038/s41551-021-00751-8](https://doi.org/10.1038/s41551-021-00751-8). A short piece on the spread of synthetic data in medical AI and the concerns it raises about software vulnerabilities and current policy.
- Walonoski, J., Kramer, M., Nichols, J., Quina, A., Moesel, C., Hall, D., Duffett, C., Dube, K., Gallagher, T., & McLachlan, S. (2018). Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record. *Journal of the American Medical Informatics Association*, 25(3), 230–238. [doi:10.1093/jamia/ocx079](https://doi.org/10.1093/jamia/ocx079). An open-source simulator of patient lifespans that covers the 10 most common reasons for primary care visits and the 10 chronic conditions with the highest morbidity in the United States.
- Gonzales, A., Guruswamy, G., & Smith, S. R. (2023). Synthetic data in health care: A narrative review. *PLOS Digital Health*, 2(1), e0000082. [doi:10.1371/journal.pdig.0000082](https://doi.org/10.1371/journal.pdig.0000082). A review that identifies seven use cases, from simulation and prediction research to the public release of datasets, and lists publicly available synthetic health datasets.
- Giuffrè, M., & Shung, D. L. (2023). Harnessing the power of synthetic data in healthcare: innovation, application, and privacy. *npj Digital Medicine*, 6, 186. [doi:10.1038/s41746-023-00927-3](https://doi.org/10.1038/s41746-023-00927-3). A review of applications, data quality, bias and re-identification risk, and of the role of regulators.
- Ramachandranpillai, R., Sikder, M. F., Bergström, D., & Heintz, F. (2024). Bt-GAN: Generating Fair Synthetic Healthdata via Bias-transforming Generative Adversarial Networks. *Journal of Artificial Intelligence Research*, 79, 1313–1341. [doi:10.1613/jair.1.15317](https://doi.org/10.1613/jair.1.15317). A generator for synthetic electronic health records that targets fairness in downstream predictions, evaluated on the MIMIC-III database.

## Questions to prepare

Bring one or two of these questions, or your own, to put to the guest lecturer.

1. Which uses of synthetic health data need the statistics of the real data, and which need only valid values and structure, as in software testing?
2. Who decides whether a synthetic health dataset may be shared, and on what evidence? How would a health data access body apply the "anonymised format" of Article 66(2) of the EHDS Regulation to synthetic data?
3. Recital 92 of the EHDS Regulation points to a residual risk of re-identification for rare diseases. How can synthetic data serve small patient groups without exposing them, and without erasing them?
4. How should a model trained on synthetic patient data be validated before it is used in care?
5. Which patient subgroups matter for fairness in the guest's setting, and how do they check that synthetic records represent those subgroups?

> [!NOTE]
> Details follow once the guest lecturer is confirmed.
