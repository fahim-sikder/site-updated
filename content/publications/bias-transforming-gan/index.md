---
title: "Bt-GAN: Generating Fair Synthetic Healthdata via Bias-transforming Generative Adversarial Networks"
date: 2024-04-25T01:55:33+01:00

projects:
  - fair-decision-making

# Authors (reference data/authors/*.yaml slugs)
authors:
  - Resmi-Ramachandranpillai
  - Md-Fahim-Sikder
  - David-Bergström
  - Fredrik-Heintz

# Publication type
# Options: article-journal, paper-conference, thesis, book, chapter, report, patent, manuscript
publication_types: ["article-journal"]

# Publication venue
publication: "*Journal of Artificial Intelligence Research*"
publication_short: "JAIR"

# Abstract
abstract: >
  Synthetic data generation offers a promising solution to enhance the usefulness of Electronic Healthcare Records (EHR) by generating realistic de-identified data. However, the existing literature primarily focuses on the quality of synthetic health data, neglecting the crucial aspect of fairness in downstream predictions. Consequently, models trained on synthetic EHR have faced criticism for producing biased outcomes in target tasks. These biases can arise from either spurious correlations between features or the failure of models to accurately represent sub-groups. To address these concerns, we present Bias-transforming Generative Adversarial Networks (Bt-GAN), a GAN-based synthetic data generator specifically designed for the healthcare domain. In order to tackle spurious correlations (i), we propose an information-constrained Data Generation Process (DGP) that enables the generator to learn a fair deterministic transformation based on a well-defined notion of algorithmic fairness. To overcome the challenge of capturing exact sub-group representations (ii), we incentivize the generator to preserve sub-group densities through score-based weighted sampling. This approach compels the generator to learn from underrepresented regions of the data manifold. To evaluate the effectiveness of our proposed method, we conduct extensive experiments using the Medical Information Mart for Intensive Care (MIMIC-III) database. Our results demonstrate that Bt-GAN achieves state-of-the-art accuracy while significantly improving fairness and minimizing bias amplification. Furthermore, we perform an in-depth explainability analysis to provide additional evidence supporting the validity of our study. In conclusion, our research introduces a novel and professional approach to addressing the limitations of synthetic data generation in the healthcare domain. By incorporating fairness considerations and leveraging advanced techniques such as GANs, we pave the way for more reliable and unbiased predictions in healthcare applications.

# Summary (for listing cards)
summary: ""

# DOI
doi: "https://doi.org/10.1613/jair.1.15317"

# Tags
tags:
  - Synthetic Data Generation
  - ML for Healthcare
  - Data Fairness
  - Generative Models

# Featured image
image:
  filename: featured.jpg
  caption: 
  focal_point: Smart

# Links
links:
  - name: PDF
    url: "https://www.jair.org/index.php/jair/article/view/15317/27031"
  - name: Dataset
    url: "https://physionet.org/content/mimiciii/1.4/"
#   - name: Slides
#     url: slides.pdf
#   - name: Video
#     url: https://youtube.com/...
#   - name: Poster
#     url: poster.pdf

# External link (opens this URL instead of the publication page)
# url_pdf: "https://www.jair.org/index.php/jair/article/view/15317/27031"
# url_code: ""
# url_dataset: "https://physionet.org/content/mimiciii/1.4/"
# url_poster: ""
# url_project: ""
# url_slides: ""
# url_source: ""
# url_video: ""

# Pin to top of listings
featured: false

# Draft
draft: false
---