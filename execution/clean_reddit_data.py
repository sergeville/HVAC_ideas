import json
import os
import argparse
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from bs4 import BeautifulSoup
import re

def clean_html(html_content):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def parse_date(date_str):
    if not date_str:
        return None
    try:
        # feedparser usually handles this well but we are reading raw json now
        return date_parser.parse(date_str)
    except:
        return None

def clean_posts(input_file, output_file, hours_window=72):
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found.")
        return

    with open(input_file, 'r') as f:
        raw_posts = json.load(f)

    cleaned_posts = []
    seen_links = set()
    
    cutoff_time = datetime.now(datetime.now().astimezone().tzinfo) - timedelta(hours=hours_window)

    for post in raw_posts:
        link = post.get('link')
        if not link or link in seen_links:
            continue
        
        # Parse date
        pub_date = parse_date(post.get('published'))
        
        # If we can't parse date, we might choose to keep it or drop it. 
        # For now, if we can't parse, we treat as 'now' or skip? 
        # Safer to skip if we strictly enforce the window.
        if not pub_date:
            continue
            
        # Ensure timezone awareness for comparison
        if pub_date.tzinfo is None:
             # Assume local if none, or UTC. Let's make cutoff naive if needed or make pub_date aware
             # Usually parser.parse returns naive if no tz in string.
             # Simplest: make both naive for comparison if one is naive
             pass # dateutil parser usually does a good job.

        # Comparing offsets can be tricky. Let's rely on dateutil to handle parsing correctly
        # and if pub_date is older than cutoff, skip.
        # To avoid crash on offset-naive vs offset-aware:
        if pub_date.tzinfo is None and cutoff_time.tzinfo is not None:
             pub_date = pub_date.replace(tzinfo=cutoff_time.tzinfo)
        elif pub_date.tzinfo is not None and cutoff_time.tzinfo is None:
             cutoff_time = cutoff_time.replace(tzinfo=pub_date.tzinfo)

        if pub_date < cutoff_time:
            continue

        clean_entry = {
            'title': post.get('title', '').strip(),
            'link': link,
            'timestamp': pub_date.isoformat(),
            'text': clean_html(post.get('content', '')),
            # RSS often doesn't give vote/comment counts directly unless in specific fields
            # We'll initialize them to 0 or extract from description if possible, but standard RSS doesn't guarantee this.
            'upvotes': 0, # Placeholder
            'comments': 0, # Placeholder
            'source_feed': post.get('source_feed')
        }
        
        cleaned_posts.append(clean_entry)
        seen_links.add(link)

    print(f"Processed {len(raw_posts)} raw posts -> {len(cleaned_posts)} cleaned posts (window: {hours_window}h).")
    
    with open(output_file, 'w') as f:
        json.dump(cleaned_posts, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Clean raw Reddit posts")
    parser.add_argument("--input", default=".tmp/raw_posts.json", help="Input raw JSON file")
    parser.add_argument("--output", default=".tmp/clean_posts.json", help="Output cleaned JSON file")
    parser.add_argument("--hours", type=int, default=72, help="Filter posts within last N hours")
    
    args = parser.parse_args()
    clean_posts(args.input, args.output, args.hours)

if __name__ == "__main__":
    main()
