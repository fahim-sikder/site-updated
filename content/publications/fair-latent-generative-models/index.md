---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Fair Latent Deep Generative Models (FLDGM) for Syntax-agnostic and Fair Synthetic Data Generation"
authors:  ["Resmi Ramachandranpillai", "Md Fahim Sikder", "Fredrik Heintz"]
author_notes:
- "Equal contribution"
- "Equal contribution"
date: 2023-01-14T01:56:14+01:00
doi: "10.3233/FAIA230484"

# Schedule page publish date (NOT publication's date).
publishDate: 2023-01-14T01:56:14+01:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["Conference paper"]

# Publication name and optional abbreviated publication name.
publication: "26th European Conference on Artificial Intelligence, Kraków, Poland, 2023"
publication_short: "ECAI 2023"

abstract: "Deep Generative Models (DGMs) for generating synthetic data with properties such as quality, diversity, fidelity, and privacy is an important research topic. Fairness is one particular aspect that has not received the attention it deserves. One difficulty is training DGMs with an in-process fairness objective, which can disturb the global convergence characteristics. To address this, we propose Fair Latent Deep Generative Models (FLDGMs) as enablers for more flexible and stable training of fair DGMs, by first learning a syntax-agnostic, model-agnostic fair latent representation (low dimensional) of the data. This separates the fairness optimization and data generation processes thereby boosting stability and optimization performance. Moreover, data generation in the low dimensional space enhances  the accessibility of models by reducing computational demands. We conduct extensive experiments on image and tabular domains using Generative Adversarial Networks (GANs) and Diffusion Models (DMs) and compare them to the state-of-the-art in terms of fairness and utility. Our proposed FLDGMs achieve superior performance in generating high-quality, high-fidelity, and high-diversity fair synthetic data compared to the state-of-the-art fair generative models."

# Summary. An optional shortened abstract.
summary: ""

tags: []
categories: []
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: "uploads/fldgm-paper.pdf"
url_code: "https://github.com/fahim-sikder/FLDGM"
url_dataset:
url_poster: "uploads/fldgm-poster.pdf"
url_project:
url_slides: "uploads/FLDGM-limelight.pdf"
url_source:
url_video:

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `internal-project` references `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
projects: []

# Slides (optional).
#   Associate this publication with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
slides: ""
---
