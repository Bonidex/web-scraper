"""
Web Scraper Tool
Author: Bonidex
Description: Scrapes titles, links, and metadata from any website.
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import os
from datetime import datetime


def scrape(url: str, output_format: str = "json"):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    print(f"[*] Scraping: {url}")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    data = {
        "url": url,
        "scraped_at": datetime.now().isoformat(),
        "title": soup.title.string.strip() if soup.title else "N/A",
        "meta_description": "",
        "headings": [],
        "links": [],
        "images": [],
    }

    # Meta description
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        data["meta_description"] = meta.get("content", "")

    # Headings (h1-h3)
    for tag in ["h1", "h2", "h3"]:
        for h in soup.find_all(tag):
            text = h.get_text(strip=True)
            if text:
                data["headings"].append({"tag": tag, "text": text})

    # Links
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if href.startswith("http"):
            data["links"].append({"text": text or "N/A", "href": href})

    # Images
    for img in soup.find_all("img", src=True):
        src = img["src"]
        alt = img.get("alt", "")
        if src.startswith("http"):
            data["images"].append({"alt": alt, "src": src})

    # Save output
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if output_format == "json":
        filename = f"output/scrape_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[+] Saved to {filename}")

    elif output_format == "csv":
        filename = f"output/links_{timestamp}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["text", "href"])
            writer.writeheader()
            writer.writerows(data["links"])
        print(f"[+] Links saved to {filename}")

    print(f"\n--- Results ---")
    print(f"Title       : {data['title']}")
    print(f"Description : {data['meta_description'][:100]}...")
    print(f"Headings    : {len(data['headings'])}")
    print(f"Links       : {len(data['links'])}")
    print(f"Images      : {len(data['images'])}")

    return data


if __name__ == "__main__":
    import sys

    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    fmt = sys.argv[2] if len(sys.argv) > 2 else "json"
    scrape(url, fmt)
