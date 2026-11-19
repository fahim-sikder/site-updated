---
title: 5.6 Interactive elements
linkTitle: 5.6 Interactive elements
weight: 56
---

These elements help structure a lesson: toggles for hints and answers, numbered steps, link cards, buttons, icons and QR codes.

## Toggle: spoiler

The `spoiler` shortcode hides content until the reader clicks. It suits quiz answers.

**Question.** Why does the discriminator receive `fake.detach()` and not `fake`?

{{< spoiler text="Show the answer" >}}
Detaching stops the discriminator loss from sending gradients into the generator. The generator is updated separately, with its own loss.
{{< /spoiler >}}

```markdown
{{</* spoiler text="Show the answer" */>}}
Detaching stops the discriminator loss from sending gradients into the generator.
{{</* /spoiler */>}}
```

## Toggle: details

Hugo's built-in `details` shortcode does the same job and can start open.

{{< details summary="Hint for Exercise 2" >}}
Start with a learning rate of 0.0002 for both networks, and use the Adam optimiser with `betas=(0.5, 0.999)`.
{{< /details >}}

{{< details summary="This toggle starts open" open=true >}}
Set `open=true` to show the content when the page loads.
{{< /details >}}

```markdown
{{</* details summary="Hint for Exercise 2" */>}}
Start with a learning rate of 0.0002 for both networks.
{{</* /details */>}}

{{</* details summary="This toggle starts open" open=true */>}}
Set `open=true` to show the content when the page loads.
{{</* /details */>}}
```

## Steps

The `steps` shortcode numbers each level-three heading inside it. Use the `{{%/* */%}}` form so that the headings are processed as Markdown.

{{% steps %}}

### Install the packages

Run `pip install torch pandas`.

### Download the data

Download the dataset and save it as `data/adult.csv`.

### Run the notebook

Open `lesson-2.ipynb` and run every cell.

{{% /steps %}}

```markdown
{{%/* steps */%}}

### Install the packages

Run `pip install torch pandas`.

### Download the data

Download the dataset and save it as `data/adult.csv`.

{{%/* /steps */%}}
```

## Cards

Cards are large links, with an optional icon and subtitle. The `cols` option sets the number of columns.

{{< cards cols="3" >}}
  {{< card url="../../01-introduction/" icon="book-open" title="Lesson 1" subtitle="Why synthetic data?" >}}
  {{< card url="../../02-generative-models/" icon="cpu-chip" title="Lesson 2" subtitle="Generative models" >}}
  {{< card url="https://pytorch.org" icon="globe-alt" title="PyTorch" subtitle="External links open in a new tab." >}}
{{< /cards >}}

```markdown
{{</* cards cols="3" */>}}
  {{</* card url="../../01-introduction/" icon="book-open" title="Lesson 1" subtitle="Why synthetic data?" */>}}
  {{</* card url="../../02-generative-models/" icon="cpu-chip" title="Lesson 2" subtitle="Generative models" */>}}
  {{</* card url="https://pytorch.org" icon="globe-alt" title="PyTorch" subtitle="External links open in a new tab." */>}}
{{</* /cards */>}}
```

## Buttons

The `button` shortcode has four styles, four sizes, five corner shapes and an optional icon.

{{< button url="../../01-introduction/" style="primary" icon="play-circle" >}}Start the course{{< /button >}}

{{< button url="../../04-exercises/" style="secondary" >}}Exercises{{< /button >}}

{{< button url="https://github.com/fahim-sikder/FairX" style="outline" new_tab="true" icon="brands/github" >}}Course code{{< /button >}}

{{< button url="../../03-evaluation/" style="ghost" icon="arrow-right" icon_position="right" >}}Skip to evaluation{{< /button >}}

{{< button url="../../01-introduction/" size="lg" rounded="full" align="center" icon="academic-cap" >}}Large, round and centred{{< /button >}}

```markdown
{{</* button url="../../01-introduction/" style="primary" icon="play-circle" */>}}Start the course{{</* /button */>}}
{{</* button url="../../04-exercises/" style="secondary" */>}}Exercises{{</* /button */>}}
{{</* button url="https://github.com/fahim-sikder/FairX" style="outline" new_tab="true" icon="brands/github" */>}}Course code{{</* /button */>}}
{{</* button url="../../03-evaluation/" style="ghost" icon="arrow-right" icon_position="right" */>}}Skip to evaluation{{</* /button */>}}
{{</* button url="../../01-introduction/" size="lg" rounded="full" align="center" icon="academic-cap" */>}}Large, round and centred{{</* /button */>}}
```

| Option | Values |
|---|---|
| `style` | `primary` (default), `secondary`, `outline`, `ghost` |
| `size` | `sm`, `md` (default), `lg`, `xl` |
| `rounded` | `sm`, `md` (default), `lg`, `xl`, `full` |
| `align` | `left` (default), `center`, `right` |
| `icon_position` | `left` (default), `right` |
| `new_tab` | `true` opens the link in a new tab |

## Icons

The `icon` shortcode places an icon inside text. Four icon packs are available: Heroicons (the default), brand logos, Academicons and Devicon.

{{< icon name="academic-cap" >}} Heroicons &nbsp;
{{< icon name="brands/github" >}} Brands &nbsp;
{{< icon name="academicons/google-scholar" >}} Academicons &nbsp;
{{< icon name="devicon/python" >}} Devicon &nbsp;
{{< icon name="devicon/pytorch" >}} PyTorch &nbsp;
{{< icon name="devicon/jupyter" >}} Jupyter

```markdown
{{</* icon name="academic-cap" */>}} Heroicons
{{</* icon name="brands/github" */>}} Brands
{{</* icon name="academicons/google-scholar" */>}} Academicons
{{</* icon name="devicon/python" */>}} Devicon
```

## In-page contents

The `toc` shortcode lists the headings of the page. On wide screens the contents list on the right already does this, so the shortcode appears only on narrow screens such as phones.

{{< toc is_open=true >}}

```markdown
{{</* toc is_open=true */>}}
```

## QR code

Hugo's built-in `qr` shortcode draws a QR code at build time. Show one on a lecture slide so that students can open the course on their phones.

{{< qr text="https://fahimsikder.com/courses/synthetic-data/" alt="QR code for the course page" />}}

```markdown
{{</* qr text="https://fahimsikder.com/courses/synthetic-data/" alt="QR code for the course page" / */>}}
```
