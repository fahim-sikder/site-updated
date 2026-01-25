---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "TransFusion: Generating Long, High-Fidelity Time Series using Diffusion Models with Transformers"
authors: ["Md Fahim Sikder", "Resmi Ramachandranpillai", "Fredrik Heintz"]
date: 2025-04-01T01:55:53+01:00
doi: "https://doi.org/10.1016/j.mlwa.2025.100652"

# Schedule page publish date (NOT publication's date).
publishDate: 2023-01-14T01:55:53+01:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["Journal article"]

# Publication name and optional abbreviated publication name.
publication: "Machine Learning with Applications"
publication_short: "MLWA"

abstract: "The generation of high-quality, long-sequenced time-series data is essential due to its wide range of applications. In the past, standalone Recurrent and Convolutional Neural Network-based Generative Adversarial Networks (GAN) were used to synthesize time-series data. However, they are inadequate for generating long sequences of time-series data due to limitations in the architecture, such as difficulties in capturing long-range dependencies, limited temporal coherence, and scalability challenges. Furthermore, GANs are well known for their training instability and mode collapse problem. To address this, we propose TransFusion, a diffusion, and transformers-based generative model to generate high-quality long-sequence time-series data. We extended the sequence length to 384, surpassing the previous limit, and successfully generated high-quality synthetic data. Also, we introduce two evaluation metrics to evaluate the quality of the synthetic data as well as its predictive characteristics. TransFusion is evaluated using a diverse set of visual and empirical metrics, consistently outperforming the previous state-of-the-art by a significant margin."

# Summary. An optional shortened abstract.
summary: ""

tags: ["generative models", "time-series generation", "synthetic data"]
categories: ["publication"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: "https://www.sciencedirect.com/science/article/pii/S2666827025000350"
url_code: "https://github.com/fahim-sikder/TransFusion"
url_dataset:
url_poster: "uploads/TransFusion-Poster.pdf"
url_project:
url_slides:
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
