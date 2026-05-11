# 🕷️ Web Scraper Tool

> A fast and simple web scraping script that extracts titles, links, headings, and images from any website.

**by Bonidex**

---

## Features

- Extracts page title, meta description, headings (h1-h3), links, and images
- Saves results as **JSON** or **CSV**
- Custom User-Agent to avoid basic blocks
- Auto-creates `output/` directory

## Requirements

```bash
pip install requests beautifulsoup4
```

## Usage

```bash
# Basic (saves as JSON)
python scraper.py https://example.com

# Save links as CSV
python scraper.py https://example.com csv
```

## Output

Results are saved in the `output/` folder with a timestamp:
- `output/scrape_YYYYMMDD_HHMMSS.json`
- `output/links_YYYYMMDD_HHMMSS.csv`

## Example Output

```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "headings": [{"tag": "h1", "text": "Example Domain"}],
  "links": [...],
  "images": [...]
}
```

---

> Made by [Bonidex](https://github.com/bonidex)
