---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "TransFusion: Generating Long, High-Fidelity Time Series using Diffusion Models with Transformers"
date: 2025-04-01T01:55:53+01:00

projects:
  - time-series-generation
# Authors (reference data/authors/*.yaml slugs)
authors:
  - Md-Fahim-Sikder
  - Resmi-Ramachandranpillai
  - Fredrik-Heintz

# Publication type
# Options: article-journal, paper-conference, thesis, book, chapter, report, patent, manuscript
publication_types: ["article-journal"]

# Publication venue
publication: "*Machine Learning with Applications*"
publication_short: "MLWA"

# Abstract
abstract: >
  The generation of high-quality, long-sequenced time-series data is essential due to its wide range of applications. In the past, standalone Recurrent and Convolutional Neural Network-based Generative Adversarial Networks (GAN) were used to synthesize time-series data. However, they are inadequate for generating long sequences of time-series data due to limitations in the architecture, such as difficulties in capturing long-range dependencies, limited temporal coherence, and scalability challenges. Furthermore, GANs are well known for their training instability and mode collapse problem. To address this, we propose TransFusion, a diffusion, and transformers-based generative model to generate high-quality long-sequence time-series data. We extended the sequence length to 384, surpassing the previous limit, and successfully generated high-quality synthetic data. Also, we introduce two evaluation metrics to evaluate the quality of the synthetic data as well as its predictive characteristics. TransFusion is evaluated using a diverse set of visual and empirical metrics, consistently outperforming the previous state-of-the-art by a significant margin.

# Summary (for listing cards)
summary: ""

# DOI
doi: "https://doi.org/10.1016/j.mlwa.2025.100652"

# Tags
tags:
  - Synthetic Data Generation
  - Time Series Generation
  - Generative Models
  - Synthetic Data Evaluation

# Featured image
image:
  filename: featured.png
  caption: 
  focal_point: Smart

# Links
links:
  - name: PDF
    url: "https://www.sciencedirect.com/science/article/pii/S2666827025000350"
  - name: Code
    url: "https://github.com/fahim-sikder/TransFusion"
  - name: Poster
    url: "uploads/TransFusion-Poster.pdf"

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