---
title: "Representative Synthetic Data for Fair Decision Making"
date: 2025-12-10T11:16:52+01:00

projects:
  - fair-decision-making
  - time-series-generation
  - fairX

# Authors (reference data/authors/*.yaml slugs)
authors:
  - Md Fahim Sikder


# Publication type
# Options: article-journal, paper-conference, thesis, book, chapter, report, patent, manuscript
publication_types: ["thesis"]

# Publication venue
publication: "Linköping University Electronic Press, 2025"
publication_short: ""

# Abstract
abstract: >
  Deep generative models and representation learning techniques have become essential to modern machine learning, enabling both the creation of synthetic data and the extraction of meaningful features for downstream tasks. While synthetic data generation promises to address data scarcity concerns, and representation learning forms the backbone of decision-making systems, both approaches can amplify societal biases present in the training data. In high-stakes applications such as healthcare, criminal justice, and financial services, biased synthetic data can pass on discriminatory patterns to new datasets, while biased representation can lead to unfair decisions that disproportionately harm marginalized groups. The challenge becomes more extensive when dealing with intersectional bias, where discrimination occurs at the intersection of multiple sensitive attributes, e.g. race, gender, etc. In this dissertation, we propose approaches for fair synthetic data generation and fair representation learning that target bias mitigation for both individual sensitive attributes and their intersections.

  To address model-specific biases in synthetic data generation, we first introduce Fair Latent Deep Generative Models (FLDGMs), a syntax-agnostic framework that first learns low-dimensional fair latent representations via a fairness-aware compression step, and then generates a synthetic fair latent space using either GANs or diffusion models, followed by high-fidelity reconstruction through a decoder. We also present Bias-transforming GAN (Bt-GAN), which tackles healthcare data biases by imposing information-theoretic constraints and preserves subgroup representation using density-aware sampling.

  For fair representation, we develop two novel representation learning techniques specifically designed to address intersectional fairness. First, we present a knowledge distillation-based approach, where we distill knowledge from an accuracy-focused teacher into a student model that enforces intersectional fairness constraints, including False Positive Rate (FPR) and demographic parity, effectively reducing FPR disparities in multi-class settings. Second, Diff-Fair uses diffusion-based representation learning to minimize mutual information with sensitive attributes, integrating intersectional and FPR regularizers to reduce demographic and outcome disparities across subgroups, while maintaining strong accuracy in binary and multi-class tasks. Also, to enable systematic evaluation, we introduce FairX, an open-source benchmarking suite that integrates pre-, in-, and post-processing bias mitigation methods alongside fairness, utility, explainability, and synthetic-data evaluation metrics.

  Along with fair synthetic data, we also investigate how to capture the distribution of time-series data using generative models. We present TransFusion, a diffusion and transformer-based architecture, that generates high-fidelity, long-sequenced synthetic time-series data (sequence length upto 384).

  Together, these contributions advance the generation of synthetic data and fair representations by integrating bias-transforming models, intersectional fairness constraints, robust benchmarking, and long-sequence synthesis, offering practical tools for building more equitable AI systems.

# Summary (for listing cards)
summary: ""


# DOI
doi: "https://doi.org/10.3384/9789181183757"

# Tags
tags:
  - Synthetic Data Generation
  - ML for Healthcare
  - Data Fairness
  - Generative Models
  - Intersectional Bias
  - Fair Representation Learning
  - Predictive Model

# Featured image
image:
  filename: featured.jpg
  caption: 
  focal_point: Smart

# Links
links:
  - name: PDF
    url: "https://liu.diva-portal.org/smash/get/diva2:2019506/FULLTEXT01.pdf"
  - name: Source
    url: "https://liu.diva-portal.org/smash/record.jsf?pid=diva2%3A2019506&dswid=6974"
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
featured: true

# Draft
draft: false
---