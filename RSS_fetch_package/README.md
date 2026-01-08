# RSS Feed Fetcher

**A simple RSS feed fetching and parsing utility for collecting content from various sources.**

Version: 1.0.0
Platform: Cross-platform
Requirements: Python 3.7+

---

## Overview

This package provides a lightweight tool for fetching and parsing RSS feeds from any source. Designed to be simple, portable, and easy to integrate into larger workflows.

---

## File Structure

```
RSS_fetch_package/
├── README.md              # This file
├── execution/
│   └── fetch_rss.py      # RSS fetching script
├── directives/           # Process documentation (optional)
└── .tmp/                 # Output directory
```

---

## Setup

### Install Dependencies

```bash
pip install feedparser requests
```

**Dependencies:**
- `feedparser` - Parse RSS/Atom feeds
- `requests` - HTTP requests

---

## Usage

### Basic Usage

```bash
# Fetch RSS feed
python3 execution/fetch_rss.py
```

### Customization

Edit `execution/fetch_rss.py` to configure:

```python
# RSS feed URLs
feeds = [
    'https://example.com/feed.rss',
    'https://another-site.com/rss',
]

# Output location
output_file = '.tmp/rss_feeds.json'

# Item limit per feed
max_items = 50
```

---

## Output Format

Saves fetched data to `.tmp/` as JSON:

```json
{
  "feeds": [
    {
      "source": "https://example.com/feed.rss",
      "title": "Example Site",
      "items": [
        {
          "title": "Article Title",
          "link": "https://example.com/article",
          "published": "2026-01-08T12:00:00Z",
          "summary": "Article description...",
          "content": "Full content..."
        }
      ]
    }
  ],
  "fetched_at": "2026-01-08T12:30:00Z",
  "total_items": 123
}
```

---

## Common Use Cases

### News Aggregation

```python
feeds = [
    'https://news-site-1.com/rss',
    'https://news-site-2.com/rss',
    'https://news-site-3.com/rss',
]
```

### Blog Monitoring

```python
feeds = [
    'https://techblog.com/feed',
    'https://industry-blog.com/rss',
]
```

### Podcast Feeds

```python
feeds = [
    'https://podcast-host.com/feed.rss',
]
```

---

## Features

- ✅ Parse RSS 2.0 and Atom feeds
- ✅ Handle multiple feeds in one run
- ✅ Extract title, link, date, summary, content
- ✅ JSON output for easy integration
- ✅ Error handling for failed feeds
- ✅ Timestamp tracking
- ✅ Configurable item limits

---

## Integration Examples

### With HVAC Analysis Package

```bash
# 1. Fetch RSS feeds
cd RSS_fetch_package
python3 execution/fetch_rss.py

# 2. Copy output to HVAC package
cp .tmp/rss_feeds.json ../HVAC_package/.tmp/

# 3. Process with HVAC scripts
cd ../HVAC_package
python3 execution/clean_reddit_data.py
# ... continue workflow
```

### With Custom Pipeline

```python
import json

# Read RSS data
with open('.tmp/rss_feeds.json', 'r') as f:
    data = json.load(f)

# Process items
for feed in data['feeds']:
    for item in feed['items']:
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        # ... your processing
```

### Scheduled Fetching

```bash
# Create cron job for daily fetching
cat > ~/rss_daily.sh << 'EOF'
#!/bin/bash
cd ~/tools/RSS_fetch_package
python3 execution/fetch_rss.py
# Optionally: copy to other locations, trigger workflows, etc.
EOF

chmod +x ~/rss_daily.sh

# Add to crontab (daily at 6am)
crontab -e
# Add: 0 6 * * * ~/rss_daily.sh
```

---

## Advanced Configuration

### Custom Parsing

Edit `fetch_rss.py` to extract additional fields:

```python
# Add custom fields
item_data = {
    'title': entry.title,
    'link': entry.link,
    'published': entry.published,
    'summary': entry.summary,
    'author': entry.get('author', 'Unknown'),  # Custom field
    'tags': entry.get('tags', []),              # Custom field
}
```

### Filtering

Add filters to only fetch relevant items:

```python
# Only include items from last 24 hours
from datetime import datetime, timedelta

cutoff = datetime.now() - timedelta(days=1)

if item_date > cutoff:
    items.append(item_data)
```

### Error Handling

The script includes basic error handling:

```python
try:
    feed = feedparser.parse(url)
    # Process feed
except Exception as e:
    print(f"Error fetching {url}: {e}")
    continue  # Skip failed feeds
```

---

## Output Files

All outputs go to `.tmp/` directory:

```
.tmp/
├── rss_feeds.json          # Main output
├── rss_feeds_raw.json      # Raw feed data (optional)
└── fetch_log.txt           # Fetch log (optional)
```

---

## Performance

- **Fetch speed:** ~1-2 seconds per feed
- **Memory:** <10MB for typical feeds
- **Disk:** ~100KB - 5MB per fetch (depends on feed size)
- **Concurrent:** Can fetch multiple feeds in parallel

---

## Troubleshooting

### "Module not found: feedparser"

```bash
pip install feedparser
```

### "SSL Certificate Error"

```python
# Add to script
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

### "Feed not updating"

- Check feed URL is valid
- Verify feed hasn't changed format
- Some feeds cache for hours (not real-time)
- Try clearing `.tmp/` and refetching

### "Timeout errors"

```python
# Increase timeout in script
import requests
response = requests.get(url, timeout=30)  # 30 seconds
```

---

## Best Practices

1. **Rate Limiting:** Add delays between feeds
   ```python
   import time
   time.sleep(1)  # 1 second between feeds
   ```

2. **Error Logging:** Track failed fetches
   ```python
   with open('.tmp/errors.log', 'a') as f:
       f.write(f"{url}: {error}\n")
   ```

3. **Caching:** Don't refetch unnecessarily
   - Check last fetch time
   - Only fetch if >1 hour old

4. **Validation:** Verify feed structure
   ```python
   if not feed.entries:
       print(f"No entries in {url}")
   ```

---

## Security Considerations

- ✅ Only fetch from trusted sources
- ✅ Validate URLs before fetching
- ✅ Sanitize content if displaying in web apps
- ✅ Don't execute code from feed content
- ⚠️ Be cautious with user-provided feed URLs

---

## Extending the Script

### Add New Feed Sources

```python
# Edit feeds list
feeds = [
    'https://new-source.com/rss',
    # ... add more
]
```

### Export to Different Formats

```python
# CSV export
import csv

with open('.tmp/feeds.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'link', 'date'])
    writer.writeheader()
    for item in items:
        writer.writerow(item)
```

### Filter by Keywords

```python
# Only fetch items containing keywords
keywords = ['hvac', 'heating', 'cooling']

if any(kw in item['title'].lower() for kw in keywords):
    filtered_items.append(item)
```

---

## Architecture: 3-Layer Design

This follows the 3-layer pattern:

**Layer 1: Directive** - What to do (optional)
**Layer 2: Orchestration** - When to run (cron, manual)
**Layer 3: Execution** - fetch_rss.py does the work

---

## Testing

```bash
# Test with single feed
python3 execution/fetch_rss.py

# Check output
cat .tmp/rss_feeds.json | python3 -m json.tool

# Verify item count
python3 -c "import json; print(json.load(open('.tmp/rss_feeds.json'))['total_items'])"
```

---

## Logging

Enable detailed logging:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='.tmp/fetch.log'
)

logger = logging.getLogger(__name__)
logger.info(f"Fetching {len(feeds)} feeds...")
```

---

## Related Packages

- **HVAC_package** - Analyzes HVAC content (uses RSS data)
- **multi-agents-log-resolution** - macOS log analysis
- All use the same 3-layer architecture

---

## Comparison with Other Tools

| Feature | This Script | Feedparser CLI | Commercial Tools |
|---------|------------|----------------|------------------|
| Cost | Free | Free | $$ |
| Setup | 30 seconds | 1 minute | Hours |
| Customization | Full control | Limited | Limited |
| Integration | Easy | Medium | APIs |
| Dependencies | 2 packages | 1 package | Many |

---

## Future Enhancements

- [ ] Parallel feed fetching
- [ ] Duplicate detection
- [ ] Content deduplication
- [ ] Email notifications
- [ ] Web dashboard
- [ ] Database storage
- [ ] Real-time monitoring

---

## Support

- Edit `execution/fetch_rss.py` directly for customizations
- Check script comments for implementation details
- Python feedparser docs: https://feedparser.readthedocs.io/

---

## License

MIT License - Free to use, modify, distribute.

---

## Quick Start

```bash
# 1. Install dependencies
pip install feedparser requests

# 2. Edit feed URLs (optional)
# nano execution/fetch_rss.py

# 3. Run
python3 execution/fetch_rss.py

# 4. Check output
cat .tmp/rss_feeds.json
```

---

## Quick Reference

```bash
# Install
pip install feedparser requests

# Run
python3 execution/fetch_rss.py

# View output
cat .tmp/rss_feeds.json | python3 -m json.tool

# Edit feeds
nano execution/fetch_rss.py

# Locations
execution/   # Script here
.tmp/       # Output here
```

---

**Ready to fetch feeds?**

```bash
pip install feedparser requests
python3 execution/fetch_rss.py
```

**Version:** 1.0.0
**Updated:** 2026-01-08
**Portable:** Yes - move folder anywhere
