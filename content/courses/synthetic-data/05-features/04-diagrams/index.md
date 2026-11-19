---
title: 5.4 Diagrams and charts
linkTitle: 5.4 Diagrams and charts
weight: 54
---

You can draw diagrams as text inside a lesson. The site renders Mermaid diagrams, Markmap mind maps and interactive Plotly charts, and loads each library only on pages that use it.

## Flowchart

```mermaid
flowchart LR
    A[Real data] --> B[Pre-processing]
    B --> C{Model}
    C -->|GAN| D[Generator]
    C -->|Diffusion| E[Denoiser]
    D --> F[Synthetic data]
    E --> F
    F --> G[Evaluation]
```

````markdown
```mermaid
flowchart LR
    A[Real data] --> B[Pre-processing]
    B --> C{Model}
    C -->|GAN| D[Generator]
    C -->|Diffusion| E[Denoiser]
    D --> F[Synthetic data]
    E --> F
    F --> G[Evaluation]
```
````

## Sequence diagram

```mermaid
sequenceDiagram
    participant Z as Noise
    participant G as Generator
    participant D as Discriminator
    Z->>G: sample z
    G->>D: fake sample G(z)
    D-->>G: gradient of the loss
    Note over G,D: repeat for each batch
```

````markdown
```mermaid
sequenceDiagram
    participant Z as Noise
    participant G as Generator
    participant D as Discriminator
    Z->>G: sample z
    G->>D: fake sample G(z)
    D-->>G: gradient of the loss
    Note over G,D: repeat for each batch
```
````

## Gantt chart

A Gantt chart can show the course schedule.

```mermaid
gantt
    title Course schedule
    dateFormat YYYY-MM-DD
    section Lectures
    Why synthetic data?     :l1, 2027-01-18, 7d
    Generative models       :l2, after l1, 14d
    Evaluation              :l3, after l2, 7d
    section Assessment
    Project                 :p1, 2027-02-01, 21d
```

````markdown
```mermaid
gantt
    title Course schedule
    dateFormat YYYY-MM-DD
    section Lectures
    Why synthetic data?     :l1, 2027-01-18, 7d
    Generative models       :l2, after l1, 14d
    Evaluation              :l3, after l2, 7d
    section Assessment
    Project                 :p1, 2027-02-01, 21d
```
````

## Pie chart

```mermaid
pie title Grading
    "Project" : 50
    "Exam" : 30
    "Exercises" : 20
```

````markdown
```mermaid
pie title Grading
    "Project" : 50
    "Exam" : 30
    "Exercises" : 20
```
````

## Mind map

A `markmap` block turns a Markdown outline into a mind map that you can pan, zoom, fold and unfold. The `height` option sets its height.

```markmap {height="380px"}
# Synthetic data
## Why
- Data sharing
- Augmentation
- Fairness
## How
- GANs
- Diffusion models
- VAEs
## Evaluation
- Fidelity
- Utility
- Privacy
```

````markdown
```markmap {height="380px"}
# Synthetic data
## Why
- Data sharing
- Augmentation
- Fairness
## How
- GANs
- Diffusion models
- VAEs
## Evaluation
- Fidelity
- Utility
- Privacy
```
````

## Interactive chart

The `chart` shortcode draws a Plotly chart from a JSON file in the page folder. Hover over the bars to see their values. The numbers are illustrative.

{{< chart data="tstr-accuracy" >}}

```markdown
{{</* chart data="tstr-accuracy" */>}}
```

The page folder holds `tstr-accuracy.json`, which follows the Plotly figure format:

```json
{
  "data": [
    { "type": "bar", "name": "Trained on real", "x": ["Logistic regression", "Random forest", "MLP"], "y": [0.85, 0.86, 0.85] },
    { "type": "bar", "name": "Trained on GAN data", "x": ["Logistic regression", "Random forest", "MLP"], "y": [0.80, 0.78, 0.79] }
  ],
  "layout": { "barmode": "group", "yaxis": { "title": { "text": "Accuracy on real test data" } } }
}
```
