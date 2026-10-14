---
title: "FairCert: Certifiable Error Rate Fairness for ML and LLM Decision Systems"
date: 2026-05-01T23:32:44+02:00
projects:
  - fair-decision-making
# Authors (reference data/authors/*.yaml slugs)
authors:
  - Md Fahim Sikder

# Publication type
# Options: article-journal, paper-conference, thesis, book, chapter, report, patent, manuscript
publication_types: ["paper-conference"]

# Publication venue
publication: "Fifth European Conference on Algorithmic Fairness (ECAF) 2026"
publication_short: "ECAF 2026"

# Abstract
abstract: "

A small FPR gap on one test set does not certify a classifier as fair. A point estimate has no confidence bound, so the observed gap may just be sampling noise. The issue is worst on intersectional subgroups, where number of samples in per-group are small. Researchers today have two options, and neither is adequate. They can report raw gaps with no statistical guarantee, or use existing methods that need white-box access and cover only individual fairness or single attributes. We present FairCert, a black-box auditing framework that produces finite-sample certificates on false positive rate (FPR) and true positive rate (TPR) gaps. It supports binary and multi-class classifiers. The main certificate uses Clopper-Pearson exact intervals with a Bonferroni correction across 𝐾 intersectional groups. Beside certification, we also add two supplementary tools. A permutation test shuffles group labels among the true negatives and recomputes the gap. Restricting to negatives, keeps Type I error valid when base rates differ across groups. And a bootstrap diagnostic serves as an exploratory alternative. We test FairCert on eight datasets covering finance, criminal justice, and vision. The evaluation covers ML classifiers, seven open-source LLMs from 3B to 30B parameters, and image models. Our experiments show that LLM fairness is domain dependent. Mistral-24B has an FPR gap of 0.259 on COMPAS but only 0.009 on ACS Income. Evaluating one attribute at a time hides intersectional gaps. On Credit Default dataset, certification passes at single sensitive attribute but fails at intersectional settings.

"
# Summary (for listing cards)
summary: ""

# DOI
doi:

# Tags
tags:
  - Representation Learning
  - ML for Healthcare
  - Data Fairness
  - Fair Representation Learning
  - Intersectional Bias

# Featured image
image:
  filename:
  caption: 
  focal_point:

# Links
links:
  - name: PDF
    url: "https://proceedings.mlr.press/v350/sikder26a.html"
#   - name: Dataset
#     url: "https://physionet.org/content/mimiciii/1.4/"
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

