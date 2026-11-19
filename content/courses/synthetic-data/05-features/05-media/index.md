---
title: 5.5 Images, video and audio
linkTitle: 5.5 Images, video and audio
weight: 55
---

Put image, video and audio files in the lesson's own folder, next to its `index.md`. The site looks for a file there first, then in the shared library at `assets/media/`, and also accepts a full web address.

## Image with a caption

The text in quotes becomes the caption. Click the image to zoom.

![A pipeline from real data through a generator to synthetic data and evaluation](pipeline.svg "Figure 1. A synthetic data pipeline.")

```markdown
![A pipeline from real data through a generator to synthetic data and evaluation](pipeline.svg "Figure 1. A synthetic data pipeline.")
```

## Image from the shared media library

A file name that is not in the lesson folder is looked up in `assets/media/`. This image is `assets/media/stacked-peaks.svg`.

![Stacked peaks](stacked-peaks.svg "An image from the shared media library.")

```markdown
![Stacked peaks](stacked-peaks.svg "An image from the shared media library.")
```

## The figure shortcode

Hugo's built-in `figure` shortcode adds options that Markdown images lack, such as a width, a link and a separate title.

{{< figure src="pipeline.svg" alt="A synthetic data pipeline" width="400" title="Figure 2" caption="The same pipeline at a width of 400 pixels." link="pipeline.svg" >}}

```markdown
{{</* figure src="pipeline.svg" alt="A synthetic data pipeline" width="400"
    title="Figure 2" caption="The same pipeline at a width of 400 pixels." link="pipeline.svg" */>}}
```

## YouTube

Pass the video ID, which is the part of the address after `v=`. This is the video from the "Teach academic courses" post on your site.

{{< youtube D2vj0WcvH5c >}}

```markdown
{{</* youtube D2vj0WcvH5c */>}}
```

## Video file

The `video` shortcode plays an MP4 or WebM file. Add `controls="true"` to show the player controls; without them, the video plays on a silent loop. This sample clip is in the public domain (CC0) and comes from MDN.

{{< video src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4" controls="true" >}}

```markdown
{{</* video src="lecture-1.mp4" controls="true" */>}}
{{</* video src="https://example.com/clip.mp4" controls="true" */>}}
```

## Audio file

The `audio` shortcode plays an MP3 or MP4 audio file. This sample is also a CC0 clip from MDN.

{{< audio src="https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3" >}}

```markdown
{{</* audio src="podcast-episode-1.mp3" */>}}
```

## Bilibili

The `bilibili` shortcode embeds a video from Bilibili by its BV identifier. We give only the syntax here, since this course has no Bilibili video.

```markdown
{{</* bilibili VIDEO_ID */>}}
```
