---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Bt-GAN: Generating Fair Synthetic Healthdata via Bias-transforming Generative Adversarial Networks"
authors: ["Resmi Ramachandranpillai", "Md Fahim Sikder", "David Bergström", "Fredrik Heintz"]
date: 2024-04-25T01:55:33+01:00
doi: "https://doi.org/10.1613/jair.1.15317"

# Schedule page publish date (NOT publication's date).
publishDate: 2023-01-14T01:55:33+01:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["Journal articles"]

# Publication name and optional abbreviated publication name.
publication: "Journal of Artificial Intelligence Research"
publication_short: "JAIR"

abstract: "Synthetic data generation offers a promising solution to enhance the usefulness of Electronic Healthcare Records (EHR) by generating realistic de-identified data. However, the existing literature primarily focuses on the quality of synthetic health data, neglecting the crucial aspect of fairness in downstream predictions. Consequently, models trained on synthetic EHR have faced criticism for producing biased outcomes in target tasks. These biases can arise from either spurious correlations between features or the failure of models to accurately represent sub-groups. To address these concerns, we present Bias-transforming Generative Adversarial Networks (Bt-GAN), a GAN-based synthetic data generator specifically designed for the healthcare domain. In order to tackle spurious correlations (i), we propose an information-constrained Data Generation Process (DGP) that enables the generator to learn a fair deterministic transformation based on a well-defined notion of algorithmic fairness. To overcome the challenge of capturing exact sub-group representations (ii), we incentivize the generator to preserve sub-group densities through score-based weighted sampling. This approach compels the generator to learn from underrepresented regions of the data manifold. To evaluate the effectiveness of our proposed method, we conduct extensive experiments using the Medical Information Mart for Intensive Care (MIMIC-III) database. Our results demonstrate that Bt-GAN achieves state-of-the-art accuracy while significantly improving fairness and minimizing bias amplification. Furthermore, we perform an in-depth explainability analysis to provide additional evidence supporting the validity of our study. In conclusion, our research introduces a novel and professional approach to addressing the limitations of synthetic data generation in the healthcare domain. By incorporating fairness considerations and leveraging advanced techniques such as GANs, we pave the way for more reliable and unbiased predictions in healthcare applications."

# Summary. An optional shortened abstract.
summary: ""

tags: ["synthetic-data-generation", "data-fairness", "medical-domain"]
categories: ["publication"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: "https://www.jair.org/index.php/jair/article/view/15317/27031"
url_code:
url_dataset: "https://physionet.org/content/mimiciii/1.4/"
url_poster:
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
