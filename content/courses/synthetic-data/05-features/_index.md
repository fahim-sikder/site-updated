---
title: 5. Feature showcase
linkTitle: 5. Feature showcase
weight: 50
---

This chapter demonstrates every content feature that a course page on this site can use. Each page shows the rendered result first and the Markdown source beneath it, so you can copy the source into your own lessons.

{{< cards cols="2" >}}
  {{< card url="01-text/" icon="pencil-square" title="5.1 Text and Markdown" subtitle="Formatting, lists, tables, footnotes, emoji and raw HTML." >}}
  {{< card url="02-callouts/" icon="light-bulb" title="5.2 Callouts" subtitle="All 16 alert box types and custom titles." >}}
  {{< card url="03-math-code/" icon="code-bracket" title="5.3 Maths and code" subtitle="LaTeX equations, highlighted code and line numbers." >}}
  {{< card url="04-diagrams/" icon="chart-bar" title="5.4 Diagrams and charts" subtitle="Mermaid diagrams, mind maps and Plotly charts." >}}
  {{< card url="05-media/" icon="photo" title="5.5 Images, video and audio" subtitle="Figures, YouTube, video files and audio files." >}}
  {{< card url="06-interactive/" icon="puzzle-piece" title="5.6 Interactive elements" subtitle="Toggles, steps, cards, buttons, icons and QR codes." >}}
  {{< card url="07-references/" icon="link" title="5.7 References and embeds" subtitle="Citations, CSV tables, reusable snippets and repository cards." >}}
  {{< card url="08-page-settings/" icon="cog-6-tooth" title="5.8 Page settings" subtitle="Front matter options that control the course layout." >}}
{{< /cards >}}

## Feature index

| Feature | Syntax | Page |
|---|---|---|
| Bold, italic, strikethrough, highlight | `**b**`, `*i*`, `~~s~~`, `==h==` | [5.1](01-text/) |
| Subscript and superscript | `H<sub>2</sub>O`, `x^2^` | [5.1](01-text/) |
| Lists, task lists, definition lists | `-`, `1.`, `- [x]`, `: ` | [5.1](01-text/) |
| Tables, footnotes, emoji, raw HTML | `\|`, `[^1]`, `:rocket:`, `<kbd>` | [5.1](01-text/) |
| Hidden author notes | `comment` shortcode | [5.1](01-text/) |
| Callouts (16 types) | `> [!NOTE]` | [5.2](02-callouts/) |
| Maths (inline and display) | `$...$`, `$$...$$`, `\(...\)`, `\[...\]` | [5.3](03-math-code/) |
| Code with line numbers and highlights | fenced code with `{linenos=table}` | [5.3](03-math-code/) |
| Mermaid diagrams | fenced code with `mermaid` | [5.4](04-diagrams/) |
| Mind maps | fenced code with `markmap` | [5.4](04-diagrams/) |
| Interactive charts | `chart` shortcode with Plotly JSON | [5.4](04-diagrams/) |
| Images and figures | `![alt](file "caption")`, `figure` | [5.5](05-media/) |
| YouTube, Bilibili, video, audio | `youtube`, `bilibili`, `video`, `audio` | [5.5](05-media/) |
| Toggles | `spoiler`, `details` | [5.6](06-interactive/) |
| Steps, cards, buttons, icons | `steps`, `cards`, `button`, `icon` | [5.6](06-interactive/) |
| In-page contents, QR codes | `toc`, `qr` | [5.6](06-interactive/) |
| Citations, mentions | `cite`, `mention` | [5.7](07-references/) |
| CSV tables, reusable snippets | `table`, `include` | [5.7](07-references/) |
| Cross-references, page values | `relref`, `param` | [5.7](07-references/) |
| GitHub, Hugging Face and link cards | `embed` | [5.7](07-references/) |
| Sidebar, contents, pager, dates | front matter | [5.8](08-page-settings/) |
