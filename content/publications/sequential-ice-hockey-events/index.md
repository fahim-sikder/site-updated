---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Sequential Ice Hockey Events Generation using Generative Adversarial Network"
authors: ["Md Fahim Sikder"]
date: 2022-06-03T10:56:37+02:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2022-06-09T10:56:37+02:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["Report"]

# Publication name and optional abbreviated publication name.
publication: "Student Project Competition, Linköping Hockey Analytics Conference 2022"
publication_short: "Student Project Competition, LINHAC 2022"

abstract: "We have generated events and coordinates that lead to a hockey goal in this project. Swedish Hockey League data from season 2020-21 for twenty matches provided by Sportlogiq were used that contain event data of those matches. We used TimeGAN to generate event data. TimeGAN learns the distribution of the original time-series data and creates a synthetic version of it. After that, we showed which events led to a goal from the synthetic data. We used principal component analysis (PCA) plots to show the original and synthetic data distributions as a qualitative evaluation. Also, we have used a sequence prediction model to test the synthetic data quantitatively. We compared the synthetic data quality with another two GAN models."

# Summary. An optional shortened abstract.
summary: ""

tags: ["Ice Hockey", "Machine Learning", "Generative Models", "Deep Learning", "Artificial Intelligence", "TimeGAN", "Sports Analytics", "LINHAC"]
categories: []
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: "uploads/sikder2022-LINHAC.pdf"
url_code: "https://github.com/fahim-sikder/event-generation-ice-hockey"
url_dataset:
url_poster:
url_project:
url_slides: "uploads/LINHAC_slide.pdf"
url_source:
url_video: "https://youtu.be/IeEa_pt1aQU"

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: "Synthetic Goal Events"
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
