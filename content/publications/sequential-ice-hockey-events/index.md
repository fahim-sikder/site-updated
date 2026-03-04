---
title: "Sequential Ice Hockey Events Generation using Generative Adversarial Network"
date: 2022-06-03T10:56:37+02:00

projects:
  - time-series-generation

# Authors (reference data/authors/*.yaml slugs)
authors:
  - Md Fahim Sikder

# Publication type
# Options: article-journal, paper-conference, thesis, book, chapter, report, patent, manuscript
publication_types: ["report"]

# Publication venue
publication: "*Student Project Competition, Linköping Hockey Analytics Conference 2022*"
publication_short: "Student Project Competition, LINHAC 2022"

# Abstract
abstract: >
  We have generated events and coordinates that lead to a hockey goal in this project. Swedish Hockey League data from season 2020-21 for twenty matches provided by Sportlogiq were used that contain event data of those matches. We used TimeGAN to generate event data. TimeGAN learns the distribution of the original time-series data and creates a synthetic version of it. After that, we showed which events led to a goal from the synthetic data. We used principal component analysis (PCA) plots to show the original and synthetic data distributions as a qualitative evaluation. Also, we have used a sequence prediction model to test the synthetic data quantitatively. We compared the synthetic data quality with another two GAN models.

# Summary (for listing cards)
summary: ""

# DOI
doi: "https://doi.org/10.1613/jair.1.15317"

# Tags
tags:
  - Synthetic Data Generation
  - Time Series Generation
  - Sports Analytics
  - Generative Models

# Featured image
image:
  filename: featured.jpg
  caption: "Synthetic Goal Events"
  focal_point: Smart

# Links
links:
  - name: PDF
    url: "uploads/sikder2022-LINHAC.pdf"
  - name: Code
    url: "https://github.com/fahim-sikder/event-generation-ice-hockey"
  - name: Slides
    url: "uploads/LINHAC_slide.pdf"
  - name: Video
    url: "https://youtu.be/IeEa_pt1aQU"
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