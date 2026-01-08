# Reddit Daily Summary Directive (Clustered Insights)

## Goal
Create a high-quality "newsletter-style" daily summary of Reddit posts. 
Instead of processing posts individually, we **Cluster** them by topic first to identify "Stories", then evaluate and summarize those stories.

## Inputs
- **RSS Feeds**: A list of Subreddit RSS URLs.
- **LLM Provider**: Gemini (via `google-generativeai`).

## Workflow Steps

### 1. Collect
- **Tool**: `execution/fetch_rss.py`
- **Action**: Fetch latest 100 posts from each feed.
- **Output**: `.tmp/raw_posts.json`

### 2. Clean
- **Tool**: `execution/clean_reddit_data.py`
- **Action**: 
    - Normalize fields & Filter (72h window).
    - Deduplicate.
- **Output**: `.tmp/clean_posts.json`

### 3. Cluster (NEW)
- **Tool**: `execution/cluster_stories.py`
- **Action**:
    - Generate Embeddings for all posts (Title + Snippet).
    - Use Clustering (e.g. Agglomerative/DBSCAN) to group related posts into "Stories".
- **Output**: `.tmp/clustered_posts.json`

### 4. Evaluate Clusters (NEW)
- **Tool**: `execution/evaluate_clusters.py`
- **Action**: 
    - Evaluate each *Cluster* as a unit.
    - Check if the "Story" is Signal vs Noise.
- **Output**: `.tmp/signal_clusters.json`

### 5. Summarize & Distribute (NEW)
- **Tool**: `execution/summarize_clusters.py`
- **Action**: 
    - Write a narrative summary for each Signal Cluster.
    - Compile into a newsletter format.
- **Output**: `outputs/newsletter_YYYY-MM-DD.txt`

## Edge Cases
- **Singletons**: Posts that don't cluster with anything. Evaluate them individually or group as "Other News".
- **Huge Clusters**: If a cluster is too big, might need sub-clustering (v2).
