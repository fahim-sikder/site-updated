---
title: 5.2 Callouts
linkTitle: 5.2 Callouts
weight: 52
---

Callouts draw attention to a note, a tip or a warning. They use the GitHub and Obsidian alert syntax: a quotation that starts with `[!TYPE]`. The theme supports 16 types.

## Basic syntax

> [!NOTE]
> The generator never sees the real data directly. It learns only through the discriminator.

```markdown
> [!NOTE]
> The generator never sees the real data directly. It learns only through the discriminator.
```

## Custom title

Text after the type replaces the default title.

> [!TIP] Study tip
> Re-derive the GAN objective by hand before you read the code.

```markdown
> [!TIP] Study tip
> Re-derive the GAN objective by hand before you read the code.
```

## All 16 types

> [!NOTE]
> Use `[!NOTE]` for background information.

> [!INFO]
> Use `[!INFO]` for neutral information.

> [!TIP]
> Use `[!TIP]` for advice that saves time.

> [!IMPORTANT]
> Use `[!IMPORTANT]` for a point that students must not miss.

> [!WARNING]
> Use `[!WARNING]` for a common mistake.

> [!CAUTION]
> Use `[!CAUTION]` for an action with risky consequences.

> [!DANGER]
> Use `[!DANGER]` for an action that can destroy work or leak data.

> [!SUCCESS]
> Use `[!SUCCESS]` for an expected result.

> [!FAILURE]
> Use `[!FAILURE]` for an error that students are likely to meet.

> [!BUG]
> Use `[!BUG]` for a known problem in the course code.

> [!QUESTION]
> Use `[!QUESTION]` for a question to think about.

> [!EXAMPLE]
> Use `[!EXAMPLE]` for a worked example.

> [!QUOTE]
> Use `[!QUOTE]` for a quotation from a paper or book.

> [!ABSTRACT]
> Use `[!ABSTRACT]` for a short overview of a lesson.

> [!SUMMARY]
> Use `[!SUMMARY]` for the key points at the end of a lesson.

> [!TODO]
> Use `[!TODO]` for a task that students must complete.

```markdown
> [!NOTE]
> [!INFO]
> [!TIP]
> [!IMPORTANT]
> [!WARNING]
> [!CAUTION]
> [!DANGER]
> [!SUCCESS]
> [!FAILURE]
> [!BUG]
> [!QUESTION]
> [!EXAMPLE]
> [!QUOTE]
> [!ABSTRACT]
> [!SUMMARY]
> [!TODO]
```

> [!WARNING] Deprecated syntax
> The older `callout` shortcode still works but prints a deprecation warning when the site builds. Use the alert syntax on this page instead.
