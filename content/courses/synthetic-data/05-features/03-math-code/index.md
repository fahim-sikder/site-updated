---
title: 5.3 Maths and code
linkTitle: 5.3 Maths and code
weight: 53
---

The site renders LaTeX with KaTeX and highlights code with Chroma. Both work on every page without extra settings.

## Inline maths

The generator maps noise $z \sim \mathcal{N}(0, I)$ to a sample $G(z)$. The alternative delimiters \(D(x) \in [0, 1]\) give the same result.

```latex
The generator maps noise $z \sim \mathcal{N}(0, I)$ to a sample $G(z)$.
The alternative delimiters \(D(x) \in [0, 1]\) give the same result.
```

## Display maths

$$
\mathcal{L}_{\text{simple}} = \mathbb{E}_{t, x_0, \epsilon}\left[ \lVert \epsilon - \epsilon_\theta(x_t, t) \rVert^2 \right]
$$

\[
\text{KL}(p \,\|\, q) = \sum_{x} p(x) \log \frac{p(x)}{q(x)}
\]

```latex
$$
\mathcal{L}_{\text{simple}} = \mathbb{E}_{t, x_0, \epsilon}\left[ \lVert \epsilon - \epsilon_\theta(x_t, t) \rVert^2 \right]
$$

\[
\text{KL}(p \,\|\, q) = \sum_{x} p(x) \log \frac{p(x)}{q(x)}
\]
```

## Aligned equations, cases and matrices

$$
\begin{aligned}
\bar{\alpha}_t &= \prod_{s=1}^{t} (1 - \beta_s) \\
x_t &= \sqrt{\bar{\alpha}_t}\, x_0 + \sqrt{1 - \bar{\alpha}_t}\, \epsilon
\end{aligned}
$$

$$
\text{ReLU}(x) =
\begin{cases}
x & \text{if } x > 0 \\
0 & \text{otherwise}
\end{cases}
\qquad
\Sigma = \begin{bmatrix} \sigma_1^2 & \rho \\ \rho & \sigma_2^2 \end{bmatrix}
$$

```latex
$$
\begin{aligned}
\bar{\alpha}_t &= \prod_{s=1}^{t} (1 - \beta_s) \\
x_t &= \sqrt{\bar{\alpha}_t}\, x_0 + \sqrt{1 - \bar{\alpha}_t}\, \epsilon
\end{aligned}
$$
```

## Numbered equations

$$
p_\theta(x_{t-1} \mid x_t) = \mathcal{N}\big(x_{t-1};\, \mu_\theta(x_t, t),\, \Sigma_\theta(x_t, t)\big) \tag{1}
$$

```latex
$$
p_\theta(x_{t-1} \mid x_t) = \mathcal{N}\big(x_{t-1};\, \mu_\theta(x_t, t),\, \Sigma_\theta(x_t, t)\big) \tag{1}
$$
```

## The math shortcode

The `math` shortcode protects a block of LaTeX from Markdown processing. The `$$` delimiters above already do this, so you need the shortcode only for unusual LaTeX that Markdown would otherwise alter.

{{< math >}}
$$
\nabla_\theta \frac{1}{m} \sum_{i=1}^{m} \log D\big(G(z^{(i)})\big)
$$
{{< /math >}}

```markdown
{{</* math */>}}
$$
\nabla_\theta \frac{1}{m} \sum_{i=1}^{m} \log D\big(G(z^{(i)})\big)
$$
{{</* /math */>}}
```

## Code blocks

Name the language after the opening fence to turn on highlighting.

```python
def sample(G, n, z_dim=64):
    """Draw n synthetic samples from the generator."""
    z = torch.randn(n, z_dim)
    with torch.no_grad():
        return G(z)
```

````markdown
```python
def sample(G, n, z_dim=64):
    """Draw n synthetic samples from the generator."""
    z = torch.randn(n, z_dim)
    with torch.no_grad():
        return G(z)
```
````

## Line numbers and highlighted lines

Options in braces after the language add line numbers, highlight lines and set the first line number.

```python {linenos=table, hl_lines=[3, "5-6"], linenostart=10}
def train(G, D, loader, epochs):
    for epoch in range(epochs):
        for real in loader:
            loss_D, loss_G = train_step(G, D, real)
        print(f"epoch {epoch}: D={loss_D:.3f} G={loss_G:.3f}")
        torch.save(G.state_dict(), f"G_{epoch}.pt")
```

````markdown
```python {linenos=table, hl_lines=[3, "5-6"], linenostart=10}
def train(G, D, loader, epochs):
    ...
```
````

## Other languages

```bash
pip install torch pandas scikit-learn
python train.py --epochs 100 --batch-size 256
```

```yaml
model: diffusion
steps: 1000
schedule: cosine
```

```diff
- loss = criterion(D(fake), zeros)
+ loss = criterion(D(fake.detach()), zeros)
```

## The highlight shortcode

The built-in `highlight` shortcode gives the same result as a fenced block.

{{< highlight r "linenos=inline" >}}
library(synthpop)
syn_data <- syn(real_data, seed = 42)
compare(syn_data, real_data)
{{< /highlight >}}

```markdown
{{</* highlight r "linenos=inline" */>}}
library(synthpop)
syn_data <- syn(real_data, seed = 42)
compare(syn_data, real_data)
{{</* /highlight */>}}
```
