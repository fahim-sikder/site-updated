---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Promoting Intersectional Fairness through Knowledge Distillation"
authors: ["Md Fahim Sikder", "Resmi Ramachandranpillai", "Daniel de Leng", "Fredrik Heintz"]
date: 2025-10-23T11:21:34+02:00
doi: "http://doi.org/10.3233/FAIA251214"
draft: false

# Schedule page publish date (NOT publication's date).
publishDate: 2025-05-03T11:21:34+02:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["Conference paper"]

# Publication name and optional abbreviated publication name.
publication: "28th European Conference on Artificial Intelligence, Bologna, Italy, 2025"
publication_short: "ECAI 2025"

abstract: "As Artificial Intelligence-driven decision-making systems become increasingly popular, ensuring fairness in their outcomes has emerged as a critical and urgent challenge. AI models, often trained on open-source datasets embedded with human and systemic biases, risk producing decisions that disadvantage certain demographics. This challenge intensifies when multiple sensitive attributes interact, leading to intersectional bias, a compounded and uniquely complex form of unfairness. Over the years, various methods have been proposed to address bias at the data and model levels. However, mitigating intersectional bias in decision-making remains an under-explored challenge. Motivated by this gap, we propose a novel framework that leverages knowledge distillation to promote intersectional fairness. Our approach proceeds in two stages: first, a teacher model is trained solely to maximize predictive accuracy, followed by a student model that inherits the teacher's representational knowledge while incorporating intersectional fairness constraints. The student model integrates tailored loss functions that enforce parity in false positive rates and demographic distributions across intersectional groups, alongside an adversarial objective that minimizes protected attribute information within the learned representation. Empirical evaluation across multiple benchmark datasets demonstrates that we achieve a 52% increase in accuracy for multi-class classification and a 61% reduction in average false positive rate across intersectional groups and outperforms state-of-the-art models. This distillation-based methodology provides a more stable optimization opportunity than direct fairness approaches, resulting in substantially fairer representations, particularly for multiple sensitive attributes and underrepresented demographic intersections."

# Summary. An optional shortened abstract.
summary: ""

tags: []
categories: []
featured: true

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: "uploads/intersectional-KD.pdf"
url_code: "https://github.com/fahim-sikder/FairX"
url_dataset:
url_poster: "uploads/Poster-ECAI-KD.pdf"
url_project:
url_slides: "uploads/Promoting-intersectional.pdf"
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
