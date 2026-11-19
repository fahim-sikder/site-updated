---
title: 5.7 References and embeds
linkTitle: 5.7 References and embeds
weight: 57
course_code: SD-101
---

These shortcodes link a lesson to the rest of your site and to outside resources: your publications, your author profile, shared text blocks, data files, GitHub and Hugging Face.

## Cite one of your publications

The `cite` shortcode shows a publication from `content/publications/`. The `view` option sets the layout: `citation`, `card`, `article-grid` or `date-title-summary`.

{{< cite page="/publications/diffusion-time-series" view="citation" >}}

{{< cite page="/publications/FairX" view="card" >}}

```markdown
{{</* cite page="/publications/diffusion-time-series" view="citation" */>}}
{{</* cite page="/publications/FairX" view="card" */>}}
```

## Mention an author

The `mention` shortcode prints an author's name from `content/authors/`. This course is taught by {{< mention "admin" >}}.

```markdown
This course is taught by {{</* mention "admin" */>}}.
```

> [!NOTE]
> On this site the name is not a working link, because `content/authors/_index.md` turns off author profile pages. Remove the `build` and `cascade` settings in that file to publish the profile pages, and the name then links to them.

## Reuse a text block

The `include` shortcode inserts the content of another page. Write a block once, for example the prerequisites, and include it in every course. The block below comes from `content/snippets/prerequisites.md`, a page that the site never publishes on its own.

{{% include "snippets/prerequisites" %}}

```markdown
{{%/* include "snippets/prerequisites" */%}}
```

## Table from a CSV file

The `table` shortcode reads a CSV file from the lesson folder. Use it for result tables that a script produces. The values are illustrative.

{{< table path="results.csv" header="true" caption="Table 1. Comparison of three generators." >}}

```markdown
{{</* table path="results.csv" header="true" caption="Table 1. Comparison of three generators." */>}}
```

Set `delimiter=";"` for files that separate values with semicolons.

## Cross-reference another page

The `relref` shortcode finds a page by its path and checks the link when the site builds. A typo in the path stops the build with an error, so links between lessons cannot silently break. See [Lesson 3]({{< relref "/courses/synthetic-data/03-evaluation" >}}) or [the TSTR section of Lesson 3]({{< relref "/courses/synthetic-data/03-evaluation#train-on-synthetic-test-on-real" >}}).

```markdown
See [Lesson 3]({{</* relref "/courses/synthetic-data/03-evaluation" */>}}) or
[the TSTR section]({{</* relref "/courses/synthetic-data/03-evaluation#train-on-synthetic-test-on-real" */>}}).
```

## Show a value from the front matter

The `param` shortcode prints a value from the page's front matter, or from the site settings if the page lacks it. This page sets `course_code: SD-101`, so the course code is **{{< param "course_code" >}}**.

```markdown
The course code is **{{</* param "course_code" */>}}**.
```

## GitHub repository card

The `embed` shortcode fetches details of a repository when the site builds, including its description and star count.

{{< embed platform="github" resource="fahim-sikder/FairX" type="repo" >}}

```markdown
{{</* embed platform="github" resource="fahim-sikder/FairX" type="repo" */>}}
```

## Hugging Face card

The same shortcode works for Hugging Face models and datasets.

{{< embed platform="huggingface" resource="scikit-learn/adult-census-income" type="dataset" >}}

```markdown
{{</* embed platform="huggingface" resource="scikit-learn/adult-census-income" type="dataset" */>}}
{{</* embed platform="huggingface" resource="google-bert/bert-base-uncased" type="model" */>}}
```

## Link card for any website

Give `url`, `title` and `description` to make a card for any site.

{{< embed url="https://fahimsikder.com" title="Md Fahim Sikder" description="Research on synthetic data, fairness and privacy in machine learning." >}}

```markdown
{{</* embed url="https://fahimsikder.com" title="Md Fahim Sikder"
    description="Research on synthetic data, fairness and privacy in machine learning." */>}}
```
