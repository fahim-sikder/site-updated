---
title: "Promoting Intersectional Fairness through Knowledge Distillation"
date: 2025-10-23T11:21:34+02:00

projects:
  - fair-decision-making

# Authors (reference data/authors/*.yaml slugs)
authors:
  - Md Fahim Sikder
  - Resmi Ramachandranpillai
  - Daniel de Leng
  - Fredrik Heintz

# Publication type
# Options: article-journal, paper-conference, thesis, book, chapter, report, patent, manuscript
publication_types: ["paper-conference"]

# Publication venue
publication: "*28th European Conference on Artificial Intelligence, Bologna, Italy, 2025*"
publication_short: "ECAI 2025"

# Abstract
abstract: >
  As Artificial Intelligence-driven decision-making systems become increasingly popular, ensuring fairness in their outcomes has emerged as a critical and urgent challenge. AI models, often trained on open-source datasets embedded with human and systemic biases, risk producing decisions that disadvantage certain demographics. This challenge intensifies when multiple sensitive attributes interact, leading to intersectional bias, a compounded and uniquely complex form of unfairness. Over the years, various methods have been proposed to address bias at the data and model levels. However, mitigating intersectional bias in decision-making remains an under-explored challenge. Motivated by this gap, we propose a novel framework that leverages knowledge distillation to promote intersectional fairness. Our approach proceeds in two stages: first, a teacher model is trained solely to maximize predictive accuracy, followed by a student model that inherits the teacher's representational knowledge while incorporating intersectional fairness constraints. The student model integrates tailored loss functions that enforce parity in false positive rates and demographic distributions across intersectional groups, alongside an adversarial objective that minimizes protected attribute information within the learned representation. Empirical evaluation across multiple benchmark datasets demonstrates that we achieve a 52% increase in accuracy for multi-class classification and a 61% reduction in average false positive rate across intersectional groups and outperforms state-of-the-art models. This distillation-based methodology provides a more stable optimization opportunity than direct fairness approaches, resulting in substantially fairer representations, particularly for multiple sensitive attributes and underrepresented demographic intersections.

# Summary (for listing cards)
summary: ""

# DOI
doi: "http://doi.org/10.3233/FAIA251214"

# Tags
tags:
  - Fair Representation Learning
  - ML for Healthcare
  - Data Fairness

# Featured image
image:
  filename: featured.jpg
  caption: 
  focal_point: Smart

# Links
links:
  - name: PDF
    url: "uploads/intersectional-KD.pdf"
  - name: Code
    url: "https://github.com/fahim-sikder/FairX"
  - name: Poster
    url: "uploads/Poster-ECAI-KD.pdf"
  - name: Slides
    url: "uploads/Promoting-intersectional.pdf"
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