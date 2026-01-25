---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Representative Synthetic Data for Fair Decision Making"
authors: ["Md Fahim Sikder"]
date: 2025-12-10T11:16:52+01:00
doi: "10.3384/9789181183757"

# Schedule page publish date (NOT publication's date).
publishDate: 2025-12-10T11:16:52+01:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["Book"]

# Publication name and optional abbreviated publication name.
publication: "Linköping University Electronic Press, 2025"
publication_short: ""

abstract: "Deep generative models and representation learning techniques have become essential to modern machine learning, enabling both the creation of synthetic data and the extraction of meaningful features for downstream tasks. While synthetic data generation promises to address data scarcity concerns, and representation learning forms the backbone of decision-making systems, both approaches can amplify societal biases present in the training data. In high-stakes applications such as healthcare, criminal justice, and financial services, biased synthetic data can pass on discriminatory patterns to new datasets, while biased representation can lead to unfair decisions that disproportionately harm marginalized groups. The challenge becomes more extensive when dealing with intersectional bias, where discrimination occurs at the intersection of multiple sensitive attributes, e.g. race, gender, etc. In this dissertation, we propose approaches for fair synthetic data generation and fair representation learning that target bias mitigation for both individual sensitive attributes and their intersections.

To address model-specific biases in synthetic data generation, we first introduce Fair Latent Deep Generative Models (FLDGMs), a syntax-agnostic framework that first learns low-dimensional fair latent representations via a fairness-aware compression step, and then generates a synthetic fair latent space using either GANs or diffusion models, followed by high-fidelity reconstruction through a decoder. We also present Bias-transforming GAN (Bt-GAN), which tackles healthcare data biases by imposing information-theoretic constraints and preserves subgroup representation using density-aware sampling.

For fair representation, we develop two novel representation learning techniques specifically designed to address intersectional fairness. First, we present a knowledge distillation-based approach, where we distill knowledge from an accuracy-focused teacher into a student model that enforces intersectional fairness constraints, including False Positive Rate (FPR) and demographic parity, effectively reducing FPR disparities in multi-class settings. Second, Diff-Fair uses diffusion-based representation learning to minimize mutual information with sensitive attributes, integrating intersectional and FPR regularizers to reduce demographic and outcome disparities across subgroups, while maintaining strong accuracy in binary and multi-class tasks. Also, to enable systematic evaluation, we introduce FairX, an open-source benchmarking suite that integrates pre-, in-, and post-processing bias mitigation methods alongside fairness, utility, explainability, and synthetic-data evaluation metrics.

Along with fair synthetic data, we also investigate how to capture the distribution of time-series data using generative models. We present TransFusion, a diffusion and transformer-based architecture, that generates high-fidelity, long-sequenced synthetic time-series data (sequence length upto 384).

Together, these contributions advance the generation of synthetic data and fair representations by integrating bias-transforming models, intersectional fairness constraints, robust benchmarking, and long-sequence synthesis, offering practical tools for building more equitable AI systems."

# Summary. An optional shortened abstract.
summary: ""

tags: []
categories: ["Book", "Publication"]
featured: true

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: "https://liu.diva-portal.org/smash/get/diva2:2019506/FULLTEXT01.pdf"
url_code:
url_dataset:
url_poster:
url_project:
url_slides:
url_source: "https://liu.diva-portal.org/smash/record.jsf?pid=diva2%3A2019506&dswid=6974"
url_video:

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: "Cover of the Dissertation"
  focal_point: "Smart"
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
