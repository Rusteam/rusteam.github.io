# Intelligence & Art

Bilingual blog (EN/RU) about machine learning, computer vision, and AI engineering.

## Quick start

```bash
# Install Hugo
brew install hugo

# Clone with theme submodule
git clone --recurse-submodules git@github.com:Rusteam/rusteam.github.io.git

# Run locally
hugo server -D

# Build for production
hugo --minify
```

## Content

- English posts: `content/en/posts/`
- Russian posts: `content/ru/posts/`
- About pages: `content/en/about.md`, `content/ru/about.md`
- Static assets: `static/images/`

### New post

```bash
hugo new content/en/posts/my-post.md
```

Add front matter:
```yaml
---
title: "Post title"
date: 2026-04-06
slug: "my-post"
author: "Rustem G"
tags: ["machine-learning"]
---
```

## Deploy

Deployed to GitHub Pages via GitHub Actions on push to `master`.

## TODO

- [ ] Set up GoatCounter account at goatcounter.com
- [ ] Change GitHub Pages source to "GitHub Actions" in repo settings
- [ ] Add `MEDIUM_TOKEN` secret to repo for automated Medium cross-posting
- [ ] Test Medium cross-post workflow with a draft post
- [ ] Review converted Medium posts for formatting issues
