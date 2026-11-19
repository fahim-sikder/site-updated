---
title: 5.8 Page settings
linkTitle: 5.8 Page settings
weight: 58
lastmod: 2026-11-10
---

The front matter at the top of each lesson file controls how the page appears in the course. This page sets `lastmod`, so a "Last updated" line appears at the bottom.

## Order and titles

| Setting | Effect |
|---|---|
| `title: 2.1 Generative adversarial networks` | Heading at the top of the page and in the browser tab. |
| `linkTitle: 2.1 GANs` | Shorter label for the sidebar, breadcrumbs and previous/next links. |
| `weight: 21` | Position in the sidebar. Lower numbers come first. |
| `summary: ...` | Short description used in lists and link previews. |

## Sidebar

| Setting | Effect |
|---|---|
| `sidebar: { open: true }` | Keeps a chapter expanded in the sidebar. The course home page of this demo uses it. |
| `sidebar: { hidden: true }` | Removes the page from the sidebar. The page is still published and reachable by a link. |

[This hidden page](../09-hidden-page/) uses `sidebar: { hidden: true }`. It is not in the sidebar, but the link still works.

## Page layout

| Setting | Default | Effect |
|---|---|---|
| `toc: false` | `true` | Hides the contents list on the right. |
| `show_breadcrumb: false` | `true` | Hides the breadcrumb trail above the title. |
| `pager: false` | `true` | Hides the previous and next links at the bottom. |
| `show_date: false` | `true` | Hides dates in the previous and next links. This course sets it for every page, since lessons have no dates. |
| `lastmod: 2026-11-10` | none | Shows a "Last updated" line at the bottom of the page. |
| `show_date_updated: false` | `true` | Hides the "Last updated" line even when `lastmod` is set. |
| `math: true` | site setting | Loads the maths renderer on this page only. Your site already turns it on for every page. |
| `draft: true` | `false` | Hides the page from the published site. `hugo server -D` shows drafts locally. |

The hidden page linked above turns off the contents list, the breadcrumb trail and the previous and next links.

## Settings for a whole course

A `cascade` block in a folder's `_index.md` applies settings to every page beneath it. This course uses one in `content/courses/_index.md`:

```yaml
---
title: Courses
type: docs
cascade:
  type: docs
  show_date: false
---
```

The `type: docs` line gives every page the course layout with the sidebar. A new course folder inside `content/courses/` inherits both settings without extra work.

## Settings that need site configuration first

| Setting | What it needs |
|---|---|
| `commentable: true` | A comment provider, such as Disqus or Giscus, set under `features.comment` in `config/_default/params.yaml`. |
| `editable: true` | A repository address set under `features.repository.url` in `params.yaml`. An "Edit this page" link then appears in the contents list. |

## A complete lesson header

```yaml
---
title: 2.1 Generative adversarial networks
linkTitle: 2.1 GANs
summary: Two networks trained against each other.
weight: 21
lastmod: 2026-11-10
toc: true
show_breadcrumb: true
pager: true
sidebar:
  open: false
  hidden: false
draft: false
---
```
