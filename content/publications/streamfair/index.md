---
title: "StreamFair: Online Fair Adaptation Under Temporal Intersectional Drift"
date: 2026-05-01T23:35:00+02:00
projects:
  - fair-decision-making
# Authors (reference data/authors/*.yaml slugs)
authors:
  - Md Fahim Sikder
  - Ericka Johnson
  - Fredrik Heintz

# Publication type
# Options: article-journal, paper-conference, thesis, book, chapter, report, patent, manuscript
publication_types: ["article-journal"]

# Publication venue
publication: "AI Transparency Journal 2026"
publication_short: "AITJ 2026"

# Abstract
abstract: "A model that satisfies equalised odds on its training data does not stay fair once the input distribution starts to change, and the gap is the largest on intersectional subgroups whose sample counts may become smaller over time as the stream goes on. We can either let the equalised odds (EO) gap grow over time by doing nothing or apply online learning with cross-entropy which in turn can make the gap worse because the gradient is dominated by the majority intersection group. We present \emph{StreamFair}, which tackles this issue by keeping the deployed model frozen, then attaching a small residual module on top of the frozen model, and training the residual module only when a fairness-aware drift detector detects a shift. The detector observes the worst-intersection EO gap with a cumulative sum and exponentially weighted moving average measurement. Once the detector is triggered and detects drift, the residual module is trained with cross-entropy along with per-intersection penalties on the true-positive rate and false-positive rate gaps and a supervised contrastive term that keeps rate estimates stable on small batches. Our experiments on six datasets/state combinations across different domains show that, \emph{StreamFair} reaches the same level of fairness and accuracy compared to the always adapt fair baseline while using $4$ to $33$x fewer updates."

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
    url: "https://aitj.org/index.php/journal/article/view/26/42"
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

