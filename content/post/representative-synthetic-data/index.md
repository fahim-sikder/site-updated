---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Teaching Machines to Be Fair: The Fight Against Algorithmic Bias"
subtitle: ""
summary: ""
authors: ["Md Fahim Sikder"]
tags: ["Data Fairness", "Generative Models", "Intersectional Fairness", "Representation Learning", "Synthetic Datas"]
categories: ["Blog Post"]
date: 2025-12-10T11:05:01+01:00
lastmod: 2025-12-10T11:05:01+01:00
featured: false
draft: true

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---
## When AI Gets It Wrong: Teaching Machines to Be Fair

Picture this: You are applying for a loan, and an AI system instantly rejects your application. Not because your credit score or income, but because you belong to a demographic group that was historically denied loans. The algorithm learned from past data that reflected decades of discrimination. Now it is repeating those same mistakes at lightning speed.

This is the problem I have been wrestling with for the past few years of my PhD at Linköping University. How do we build AI systems that recognize and counteract bias instead of amplifying it?

## The Hidden Problem in AI Systems

AI models learn from historical data. Sounds reasonable, right? But here is the catch: historical data is messy, biased, and often reflects societal inequalities we are tyring to overcome. When we train models on healthcare records, criminal justice data, or financial information, we are essentially teaching them to maintaining existing discrimination.

The problem gets even trickier when we consider intersectional bias, where the compounded discrimination affects people with multiple marginalized identities. An AI system might appear "fair" when look at sensitive attribute like race or gender alone. But what about darker-skinned women? Or elderly individuals from minority communities? These intersectional groups often face unique forms of discrimination that traditional fairness approaches completely miss.

## Two Paths to Fair AI

My research explores two strategies for tackling these challenges:

First, I developed methods to generate synthetic data that removes discriminatory patterns while keeping the data useful for real-world applications. Think of it as creating practice datasets where AI can learn to make good decisions without picking up our bad habits. 

I created two systems for this: Bt-GAN for healthcare data, which tackles the challenge of medical records where biases run deep, and FLDGMs (Fair Latent Deep Generative Models), which works across different types of data.

The results were promising. When we tested Bt-GAN on real healthcare datasets, it achieved near-perfect demographic parity (reducing discrimination from 23.9% to just 0.1%) while maintaining the data quality needed for clinical predictions. FLDGMs showed similar success across financial and criminal justice datasets, proving that fair AI does not have to sacrifice accuracy.

<!-- Second, I developed techniques that teach AI models to extract "fair features" from biased data. Instead of treating fairness as an add-on, these approaches bake it directly into how the model understands and represents information. One method uses knowledge distillation where, a teacher model learns to be accurate, then transfers that knowledge to a student model that's also constrained to be fair. Another approach, called Diff-Fair, uses diffusion models to gradually refine representations until sensitive attributes like race or gender become irrelevant to the decision-making process. -->

Second, I developed techniques that teach AI models to extract "fair features" from biased data. Instead of treating fairness as something you add at the end, these approaches build it directly into how the model understands and represents information. 

One method uses knowledge distillation—a teacher model learns to be accurate, then passes that knowledge to a student model that's also trained to be fair. Another approach, called Diff-Fair, uses diffusion models to gradually refine how the AI sees the data, making sensitive attributes like race or gender irrelevant to its decisions.

## Making Fairness Measurable

One of the frustrating aspects of fairness research has been the lack of standardized tools. Researchers were using different metrics, different evaluation methods, and it was nearly impossiblem to compare approaches or know what acutually works in practice.

To address this, I built FairX, an open-source benchmarking platform that provides a unified way to evaluate both fairness and data quality. It's designed for researchers and practitioners who need to assess whether their AI systems are actually fair, not just whether they seem fair on paper.