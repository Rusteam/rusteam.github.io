#!/usr/bin/env python3
"""Convert Medium HTML export to Hugo markdown posts."""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

from bs4 import BeautifulSoup
from markdownify import markdownify as md


SKIP_FILES = {
    # Short comments, not full articles
    "2023-02-13_sounds-curious--can-you-share-more-about-Gitlab-Docker-executor--8fd02619fff3.html",
    "2023-03-20_thanks--great-overview-76bd5e65132b.html",
    "2023-07-06_great-overview--thanks--e82ebe2c221f.html",
    "2023-08-14_If-you-have-labels-I-d-say-start-with-yolov8-as-it-s-easy-to-train-and-lightweight--2d9ee3d519de.html",
    "2023-10-03_this-is-pure-magic-43b00db50481.html",
    "2024-05-27_I-can-see-that-they-forked-ultralytics--even-didn-t-change-pyproject-toml--6fede12bb95c.html",
    "2025-08-14_Awesome-thanks-for-the-honest-walkthrough-f24dd7efdaae.html",
}

# Map filename patterns to clean slugs
SLUG_MAP = {
    "It-s-Possible-to-Win-ML-Hackathon": "win-ml-hackathon",
    "Improve-performance-of-models-deployed-with-Triton": "triton-model-performance",
    "Automate-model-training-with-CI-CD": "automate-training-cicd",
    "Reproducible-data-prep": "reproducible-data-prep",
    "Keep-a-Trainlog-for-machine-learning": "ml-trainlog",
    "YOLOv8--EfficientDet--Faster-R-CNN-or-YOLOv5-for-remote-sensing": "object-detection-remote-sensing",
    "Fine-tune-Segment-Anything-model": "finetune-segment-anything",
    "Zero-training-object-detection": "zero-training-object-detection",
    "Efficient-Frame-Extraction-for-Video-Object-Annotation": "efficient-frame-extraction",
    "Practical-hyper-parameter-tuning-for-any-deep-neural-net": "hyperparameter-tuning",
    "TfIdf---Naive-Bayes-beat-neural-nets": "tfidf-naive-bayes",
    "2023-highlights-of-computer-vision-progress": "cv-highlights-2023",
    "Detect-and-classify-with-zero-labels-and-code": "zero-label-detection",
    "From-notebooks-to-agents--Evolution-of-GPU-workflows-in-deep-learning": "gpu-workflows-evolution",
    "LLM-evaluation-for-RAG-applications": "llm-eval-rag",
    "How-to-share-ML-experiments-and-code-38b29bedc5bf": "share-ml-experiments",
    "How-to-share-ML-experiments-and-code---Part-II": "share-ml-experiments-part2",
    "Mastering-AI-Coding-Agents--Tips-and-Tricks": "ai-coding-agents",
    "A-Beginner-s-Guide-to-Linux-Networking-for-Edge-ML-Deployments": "linux-networking-edge-ml",
    "LLMs-are-easier-than-traditional-deep-learning": "llms-easier-than-dl",
    "Part-III--Tracking": "share-ml-experiments-part3",
}


def extract_tags_from_footer(soup):
    """Try to extract tags from the footer or meta."""
    tags = []
    # Medium exports sometimes have tags in footer links
    footer = soup.find("footer")
    if footer:
        for a in footer.find_all("a"):
            href = a.get("href", "")
            if "/tag/" in href:
                tags.append(a.get_text().strip())
    return tags


def get_slug(filename):
    """Get a clean slug from the filename."""
    # Remove date prefix and hash suffix
    name = re.sub(r"^\d{4}-\d{2}-\d{2}_", "", filename)
    name = re.sub(r"^draft_", "", name)
    name = re.sub(r"-[a-f0-9]{12}\.html$", "", name)
    name = name.rstrip(".html")

    for pattern, slug in SLUG_MAP.items():
        if pattern in name:
            return slug

    # Fallback: clean up the name
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug


def extract_date(filename, soup):
    """Extract date from filename or HTML."""
    # Try filename first
    match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    if match:
        return match.group(1)

    # Try HTML footer
    time_el = soup.find("time")
    if time_el and time_el.get("datetime"):
        dt = datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")

    return None


def extract_canonical_url(soup):
    """Extract the canonical Medium URL."""
    footer = soup.find("footer")
    if footer:
        for a in footer.find_all("a"):
            if "canonical" in a.get_text().lower():
                return a.get("href", "")
    return ""


def convert_file(html_path, output_dir):
    """Convert a single Medium HTML file to Hugo markdown."""
    filename = os.path.basename(html_path)

    if filename in SKIP_FILES:
        print(f"  SKIP (comment): {filename}")
        return None

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Extract title
    title_el = soup.find("h3", class_="graf--title") or soup.find("title")
    title = title_el.get_text().strip() if title_el else filename
    # Escape quotes in title
    title_escaped = title.replace('"', '\\"')

    # Extract date
    date = extract_date(filename, soup)

    # Get slug
    slug = get_slug(filename)

    # Is it a draft?
    is_draft = filename.startswith("draft_")

    # Extract canonical URL
    canonical = extract_canonical_url(soup)

    # Extract the article content (skip the title since we put it in front matter)
    article = soup.find("article")
    if not article:
        print(f"  SKIP (no article): {filename}")
        return None

    # Remove the title h3 to avoid duplication
    title_h3 = article.find("h3", class_="graf--title")
    if title_h3:
        title_h3.decompose()

    # Remove subtitle if it duplicates
    subtitle_el = article.find("h4", class_="graf--subtitle")
    subtitle = ""
    if subtitle_el:
        subtitle = subtitle_el.get_text().strip()
        subtitle_el.decompose()

    # Remove footer (author/date info we already have)
    footer = article.find("footer")
    if footer:
        footer.decompose()

    # Convert images: fix Medium CDN URLs and extract alt text
    for fig in article.find_all("figure"):
        img = fig.find("img")
        if img:
            # Keep the image, remove figure wrapper styling
            figcaption = fig.find("figcaption")
            caption = figcaption.get_text().strip() if figcaption else ""
            if caption and img:
                img["alt"] = caption

    # Handle Medium embeds (mixtapeEmbed) - convert to simple links
    for embed in article.find_all("div", class_="graf--mixtapeEmbed"):
        a = embed.find("a")
        if a:
            href = a.get("href", "")
            text = a.get_text().strip()
            # Replace with a simple link paragraph
            new_p = soup.new_tag("p")
            new_a = soup.new_tag("a", href=href)
            new_a.string = text
            new_p.append(new_a)
            embed.replace_with(new_p)

    # Convert HTML to markdown
    content = md(
        str(article),
        heading_style="atx",
        code_language_callback=lambda _: "",
        strip=["style"],
    )

    # Clean up the markdown
    # Remove excessive blank lines
    content = re.sub(r"\n{4,}", "\n\n\n", content)
    # Clean up image URLs - remove query params from medium CDN
    content = re.sub(r"\(https://cdn-images-1\.medium\.com/max/\d+/", "(https://cdn-images-1.medium.com/max/1200/", content)

    # Build front matter
    front_matter_lines = [
        "---",
        f'title: "{title_escaped}"',
    ]
    if date:
        front_matter_lines.append(f"date: {date}")
    front_matter_lines.append(f'slug: "{slug}"')
    if subtitle:
        front_matter_lines.append(f'description: "{subtitle.replace(chr(34), chr(92)+chr(34))}"')
    if is_draft:
        front_matter_lines.append("draft: true")
    if canonical:
        front_matter_lines.append(f'canonicalURL: "{canonical}"')
    front_matter_lines.append(f'author: "Rustem G"')
    tags = extract_tags_from_footer(soup)
    if tags:
        front_matter_lines.append(f"tags: {tags}")
    front_matter_lines.append("---")

    full_content = "\n".join(front_matter_lines) + "\n\n" + content.strip() + "\n"

    # Write output
    out_filename = f"{slug}.md"
    out_path = os.path.join(output_dir, out_filename)
    os.makedirs(output_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    status = "DRAFT" if is_draft else "OK"
    print(f"  {status}: {filename} -> {out_filename}")
    return out_path


def main():
    medium_dir = sys.argv[1] if len(sys.argv) > 1 else "/tmp/medium-export/posts"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "/Users/rustynail/Projects/rusteam.github.io/content/en/posts"

    html_files = sorted(Path(medium_dir).glob("*.html"))
    print(f"Found {len(html_files)} HTML files in {medium_dir}\n")

    converted = []
    for html_file in html_files:
        result = convert_file(str(html_file), output_dir)
        if result:
            converted.append(result)

    print(f"\nConverted {len(converted)} posts to {output_dir}")


if __name__ == "__main__":
    main()
