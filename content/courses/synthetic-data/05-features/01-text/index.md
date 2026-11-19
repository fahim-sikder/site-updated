---
title: 5.1 Text and Markdown
linkTitle: 5.1 Text and Markdown
weight: 51
---

This page covers standard Markdown plus the extensions that this site enables: highlighting, subscript, superscript, emoji and raw HTML.

## Inline formatting

**Bold**, *italic*, ***bold italic***, ~~strikethrough~~, `inline code`, ==highlighted text==, H<sub>2</sub>O, x^2^, and a [link to Lesson 1](../../01-introduction/). External links such as [PyTorch](https://pytorch.org) work the same way.

```markdown
**Bold**, *italic*, ***bold italic***, ~~strikethrough~~, `inline code`,
==highlighted text==, H<sub>2</sub>O, x^2^, and a [link to Lesson 1](../../01-introduction/).
External links such as [PyTorch](https://pytorch.org) work the same way.
```

> [!NOTE]
> Write subscripts as `<sub>2</sub>`. The shorter `H~2~O` form draws a line through the 2 on this site, because the strikethrough syntax claims the single `~` first.

## Headings with a custom anchor {#custom-anchor}

Headings at levels 2 and 3 appear in the contents list on the right. Add `{#name}` after a heading to fix its anchor, so that links such as [this one](#custom-anchor) survive a change of heading text.

```markdown
## Headings with a custom anchor {#custom-anchor}

Links such as [this one](#custom-anchor) survive a change of heading text.
```

## Lists

1. Collect the real data.
2. Train the generator.
   - Use a held-out validation set.
   - Save a checkpoint after each epoch.
3. Evaluate the synthetic data.

```markdown
1. Collect the real data.
2. Train the generator.
   - Use a held-out validation set.
   - Save a checkpoint after each epoch.
3. Evaluate the synthetic data.
```

## Task lists

Task lists suit lesson checklists.

- [x] Install Python 3.11
- [x] Install PyTorch
- [ ] Download the dataset
- [ ] Train the first GAN

```markdown
- [x] Install Python 3.11
- [x] Install PyTorch
- [ ] Download the dataset
- [ ] Train the first GAN
```

## Definition lists

Definition lists suit glossaries.

Fidelity
: How closely the synthetic data matches the distribution of the real data.

Utility
: How well a model trained on synthetic data performs on real data.

```markdown
Fidelity
: How closely the synthetic data matches the distribution of the real data.

Utility
: How well a model trained on synthetic data performs on real data.
```

## Tables

The colons in the separator row set the alignment of each column.

| Model | Year | Training | Sampling speed |
|:------|:----:|---------:|---------------:|
| GAN | 2014 | Adversarial | Fast |
| VAE | 2013 | Likelihood bound | Fast |
| Diffusion | 2020 | Denoising | Slow |

```markdown
| Model | Year | Training | Sampling speed |
|:------|:----:|---------:|---------------:|
| GAN | 2014 | Adversarial | Fast |
| VAE | 2013 | Likelihood bound | Fast |
| Diffusion | 2020 | Denoising | Slow |
```

## Quotations

> All models are wrong, but some are useful.
>
> George Box

```markdown
> All models are wrong, but some are useful.
>
> George Box
```

## Footnotes

Goodfellow and colleagues introduced the GAN in 2014.[^gan] The footnote text appears at the end of the page.

[^gan]: Goodfellow, I. et al. (2014). Generative adversarial nets. *Advances in Neural Information Processing Systems* 27.

```markdown
Goodfellow and colleagues introduced the GAN in 2014.[^gan]

[^gan]: Goodfellow, I. et al. (2014). Generative adversarial nets.
    *Advances in Neural Information Processing Systems* 27.
```

## Emoji

:rocket: :books: :bulb: :white_check_mark: :warning:

```markdown
:rocket: :books: :bulb: :white_check_mark: :warning:
```

## Raw HTML

Raw HTML works inside Markdown. Press <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to run a notebook cell. Hover over <abbr title="Train on synthetic, test on real">TSTR</abbr> to see its expansion.

```html
Press <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to run a notebook cell.
Hover over <abbr title="Train on synthetic, test on real">TSTR</abbr> to see its expansion.
```

## Horizontal rule

Three hyphens on their own line draw a dividing line.

---

```markdown
---
```

## Hidden author notes

<!-- This note does not appear on the page. -->

An HTML comment keeps a note in the source file without showing it on the page. A comment sits just above this sentence. Anyone who opens the browser's "view source" can still read it, so do not put exam answers in comments.

```html
<!-- This note does not appear on the page. -->
```
