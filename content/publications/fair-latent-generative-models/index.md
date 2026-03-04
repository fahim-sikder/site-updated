---
title: "Fair Latent Deep Generative Models (FLDGM) for Syntax-agnostic and Fair Synthetic Data Generation"
date: 2023-01-14T01:56:14+01:00

projects:
  - fair-decision-making

# Authors (reference data/authors/*.yaml slugs)
authors:
  - Resmi Ramachandranpillai
  - Md Fahim Sikder
  - Fredrik Heintz

author_notes:
- "Equal contribution"
- "Equal contribution"

# Publication type
# Options: article-journal, paper-conference, thesis, book, chapter, report, patent, manuscript
publication_types: ["paper-conference"]

# Publication venue
publication: "*26th European Conference on Artificial Intelligence, Kraków, Poland, 2023*"
publication_short: "ECAI 2023"

# Abstract
abstract: >
  Deep Generative Models (DGMs) for generating synthetic data with properties such as quality, diversity, fidelity, and privacy is an important research topic. Fairness is one particular aspect that has not received the attention it deserves. One difficulty is training DGMs with an in-process fairness objective, which can disturb the global convergence characteristics. To address this, we propose Fair Latent Deep Generative Models (FLDGMs) as enablers for more flexible and stable training of fair DGMs, by first learning a syntax-agnostic, model-agnostic fair latent representation (low dimensional) of the data. This separates the fairness optimization and data generation processes thereby boosting stability and optimization performance. Moreover, data generation in the low dimensional space enhances  the accessibility of models by reducing computational demands. We conduct extensive experiments on image and tabular domains using Generative Adversarial Networks (GANs) and Diffusion Models (DMs) and compare them to the state-of-the-art in terms of fairness and utility. Our proposed FLDGMs achieve superior performance in generating high-quality, high-fidelity, and high-diversity fair synthetic data compared to the state-of-the-art fair generative models.

# Summary (for listing cards)
summary: ""

# DOI
doi: "https://doi.org/10.3233/FAIA230484"

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
    url: "uploads/fldgm-paper.pdf"
  - name: Code
    url: "https://github.com/fahim-sikder/FLDGM"
  - name: Slides
    url: "uploads/FLDGM-limelight.pdf"
  - name: Poster
    url: "uploads/fldgm-poster.pdf"
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