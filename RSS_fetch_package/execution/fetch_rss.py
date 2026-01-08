import feedparser
import json
import os
import argparse
from datetime import datetime

def fetch_feeds(feed_urls):
    all_posts = []
    
    for url in feed_urls:
        print(f"Fetching {url}...")
        try:
            feed = feedparser.parse(url)
            if feed.bozo:
                print(f"  Warning: Potential issue with feed {url}: {feed.bozo_exception}")

            for entry in feed.entries:
                # Add source URL for potential debugging/tracking
                entry['source_feed'] = url
                # Convert struct_time to something serializable (string) immediately or keep as raw
                 # feedparser entries are largely dict-like but contain time.struct_time which isn't json serializable
                # We will extract what we need in the cleaning step, so for "raw", we'll just dump a simplified version
                # or rely on standard keys. 
                # To be safe for JSON dump, we'll build a simple dict
                
                post = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', ''),
                    'content': entry.get('content', [{'value': ''}])[0]['value'] if 'content' in entry else '',
                    'id': entry.get('id', ''),
                    'source_feed': url
                }
                
                # Check for media/content if 'content' text is empty but 'summary' exists
                if not post['content'] and post['summary']:
                    post['content'] = post['summary']
                
                all_posts.append(post)
                
        except Exception as e:
            print(f"  Error fetching {url}: {e}")
            
    return all_posts

def main():
    parser = argparse.ArgumentParser(description="Fetch RSS feeds")
    parser.add_argument("--feeds", nargs="+", help="List of RSS feed URLs", required=True)
    parser.add_argument("--output", help="Output JSON file path", default=".tmp/raw_posts.json")
    
    args = parser.parse_args()
    
    # Ensure output dir exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    posts = fetch_feeds(args.feeds)
    print(f"Fetched {len(posts)} total posts.")
    
    with open(args.output, 'w') as f:
        json.dump(posts, f, indent=2)

if __name__ == "__main__":
    main()
