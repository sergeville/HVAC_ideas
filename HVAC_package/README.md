# HVAC Ideas Analysis System

**A collection of Python scripts for analyzing HVAC-related discussions from Reddit.**

Version: 1.0.0
Platform: Cross-platform
Requirements: Python 3.7+, API keys (Reddit, OpenAI/Anthropic)

---

## Overview

This package contains tools for:
- Cleaning and evaluating Reddit posts for relevance
- Clustering similar stories/discussions
- Generating summaries and insights
- Evaluating cluster quality

**Note:** For RSS feed fetching, see the separate `RSS_fetch_package`

---

## File Structure

```
HVAC_package/
├── README.md                      # This file
├── AGENTS.md                      # Agent instructions
├── GEMINI.md                      # Gemini-specific config
├── env.example                    # Environment variables template
├── execution/
│   ├── clean_reddit_data.py      # Clean/filter Reddit posts
│   ├── cluster_stories.py        # Group similar stories
│   ├── evaluate_clusters.py      # Assess cluster quality
│   ├── evaluate_posts.py         # Score post relevance
│   ├── summarize_clusters.py     # Generate cluster summaries
│   └── summarize_posts.py        # Summarize individual posts
├── directives/
│   └── reddit_daily_summary.md   # Process documentation
└── .tmp/                          # Output directory
```

---

## Setup

### 1. Environment Variables

Copy and configure environment file:

```bash
cp env.example .env
```

Edit `.env` with your API keys:

```bash
# Reddit API
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=your_app_name

# AI API (choose one)
OPENAI_API_KEY=your_openai_key
# OR
ANTHROPIC_API_KEY=your_anthropic_key

# Google APIs (optional)
GOOGLE_SHEETS_CREDENTIALS=path/to/credentials.json
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Common dependencies:
- `praw` - Reddit API
- `feedparser` - RSS feeds
- `openai` or `anthropic` - AI processing
- `scikit-learn` - Clustering
- `pandas` - Data manipulation

---

## Usage

### Workflow Overview

```
1. Clean → 2. Evaluate → 3. Cluster → 4. Summarize
```

**Note:** For data fetching (Reddit/RSS), use appropriate tools first, then process with these scripts.

### 1. Clean Reddit Data

```bash
python3 execution/clean_reddit_data.py
```

Filters and cleans Reddit posts for relevance.

### 2. Evaluate Posts

```bash
python3 execution/evaluate_posts.py
```

Scores posts for HVAC relevance and quality.

### 3. Cluster Stories

```bash
python3 execution/cluster_stories.py
```

Groups similar discussions together using ML clustering.

### 4. Summarize Content

```bash
# Summarize individual posts
python3 execution/summarize_posts.py

# Summarize clusters
python3 execution/summarize_clusters.py
```

Generates AI-powered summaries of content.

### 5. Evaluate Results

```bash
python3 execution/evaluate_clusters.py
```

Assesses cluster quality and coherence.

---

## Script Details

### clean_reddit_data.py
**Purpose:** Filter and clean Reddit posts
**Input:** Raw Reddit data
**Output:** Cleaned, filtered posts
**Filters:** Removes spam, off-topic, low-quality

### evaluate_posts.py
**Purpose:** Score posts for relevance
**Input:** Cleaned posts
**Output:** Posts with relevance scores
**Uses:** AI to evaluate HVAC relevance

### cluster_stories.py
**Purpose:** Group similar discussions
**Input:** Evaluated posts
**Output:** Clustered groups
**Algorithm:** K-means or hierarchical clustering

### summarize_posts.py
**Purpose:** Summarize individual posts
**Input:** Posts
**Output:** Concise summaries
**Uses:** AI summarization

### summarize_clusters.py
**Purpose:** Summarize entire clusters
**Input:** Clustered posts
**Output:** Cluster-level summaries
**Uses:** AI to synthesize themes

### evaluate_clusters.py
**Purpose:** Assess cluster quality
**Input:** Clusters
**Output:** Quality metrics
**Metrics:** Coherence, separation, silhouette score

---

## Configuration

### Subreddits

Edit scripts to target specific subreddits:
```python
subreddits = ['HVAC', 'hvacadvice', 'HomeImprovement']
```

### Time Ranges

Adjust fetch timeframes:
```python
time_filter = 'day'  # hour, day, week, month, year, all
```

### Clustering Parameters

Tune clustering:
```python
n_clusters = 5  # Number of clusters
min_posts = 3   # Minimum posts per cluster
```

---

## Examples

### Daily HVAC Summary Workflow

```bash
#!/bin/bash
# Complete daily analysis

# 1. Clean and evaluate (assuming data already fetched)
python3 execution/clean_reddit_data.py
python3 execution/evaluate_posts.py

# 2. Cluster similar stories
python3 execution/cluster_stories.py

# 3. Generate summaries
python3 execution/summarize_clusters.py

# 4. Quality check
python3 execution/evaluate_clusters.py
```

### Custom Analysis

```bash
# Focus on specific subreddit
python3 execution/clean_reddit_data.py --subreddit hvacadvice

# Adjust clustering
python3 execution/cluster_stories.py --clusters 10

# Evaluate specific cluster
python3 execution/evaluate_clusters.py --cluster_id 3
```

---

## Architecture: 3-Layer Design

This follows the 3-layer architecture pattern:

**Layer 1: Directives** - SOPs in `directives/`
- Natural language instructions
- Define goals, inputs, tools, outputs

**Layer 2: Orchestration** - AI/human decision-making
- Read directives
- Call execution scripts
- Handle errors

**Layer 3: Execution** - Python scripts in `execution/`
- Deterministic processing
- API calls
- Data manipulation

### Why This Works

- **Reliability:** Deterministic scripts don't make random mistakes
- **Maintainability:** Each layer can be updated independently
- **Testability:** Scripts are easily testable
- **Scalability:** Add new scripts without changing directives

---

## Output Files

All outputs go to `.tmp/` directory:

```
.tmp/
├── reddit_posts_raw.json        # Raw Reddit data (from external source)
├── reddit_posts_cleaned.json    # Filtered posts
├── posts_evaluated.json         # With scores
├── clusters.json                # Clustered groups
├── post_summaries.json          # Individual summaries
├── cluster_summaries.json       # Cluster summaries
└── cluster_evaluation.json      # Quality metrics
```

---

## API Usage & Costs

### Reddit API
- **Free tier:** 60 requests/minute
- **Cost:** Free
- **Limits:** Rate-limited

### OpenAI API
- **GPT-3.5:** ~$0.002 per request
- **GPT-4:** ~$0.03 per request
- **Cost varies:** Based on token usage

### Anthropic API
- **Claude Sonnet:** ~$0.003 per request
- **Claude Opus:** ~$0.015 per request
- **Cost varies:** Based on token usage

**Tip:** Use caching and batch processing to minimize costs.

---

## Best Practices

1. **Rate Limiting:** Respect API limits (add delays)
2. **Caching:** Save intermediate results
3. **Error Handling:** Scripts should fail gracefully
4. **Logging:** Track API calls and costs
5. **Testing:** Test with small datasets first
6. **Monitoring:** Check output quality regularly

---

## Troubleshooting

### Reddit API Errors

**"Invalid credentials"**
```bash
# Check .env file
cat .env | grep REDDIT
# Verify credentials at reddit.com/prefs/apps
```

### AI API Errors

**"Rate limit exceeded"**
```python
# Add delays between requests
import time
time.sleep(1)  # 1 second delay
```

**"Insufficient quota"**
- Check your API usage/billing
- Switch to cheaper model
- Reduce request frequency

### Clustering Issues

**"Empty clusters"**
- Reduce number of clusters
- Check minimum posts setting
- Verify data quality

---

## Extending the System

### Add New Data Source

1. Create new script: `execution/fetch_newsource.py`
2. Follow existing patterns
3. Output to `.tmp/`
4. Update workflow

### Add New Analysis

1. Create script: `execution/analyze_something.py`
2. Read from `.tmp/`
3. Process data
4. Save results

### Add New Directive

1. Create: `directives/new_process.md`
2. Document: goals, inputs, tools, outputs
3. Reference in workflow

---

## Testing

### Test Individual Scripts

```bash
# Test with limited data
python3 execution/fetch_rss.py --limit 10
python3 execution/clean_reddit_data.py --test

# Check outputs
ls -lh .tmp/
```

### Validate Results

```bash
# Check cluster quality
python3 execution/evaluate_clusters.py

# Review summaries
cat .tmp/cluster_summaries.json | python3 -m json.tool
```

---

## Performance

- **Fetch:** ~1-2 seconds per feed
- **Clean:** ~100 posts/second
- **Evaluate:** ~2-5 seconds per post (AI call)
- **Cluster:** <1 second for 1000 posts
- **Summarize:** ~3-10 seconds per summary (AI call)

**Bottlenecks:** AI API calls (use caching!)

---

## Directory Structure

```bash
# Keep organized
.tmp/              # Temporary/intermediate files
data/              # Persistent data (optional)
logs/              # Log files (optional)
config/            # Configuration files (optional)
```

---

## Security

### API Keys
- ⚠️ Never commit `.env` to git
- ⚠️ Use `.gitignore` to exclude secrets
- ⚠️ Rotate keys periodically

### Data Privacy
- Reddit data is public
- Follow Reddit's terms of service
- Respect user privacy
- Don't redistribute personal info

---

## Self-Annealing

When errors occur:
1. **Fix the script** that failed
2. **Test the fix**
3. **Update directive** with learnings
4. **System improves**

Example:
```
❌ Hit API rate limit
→ Add exponential backoff
→ Test with stress test
→ Update directive: "Use backoff for >10 requests"
✅ System handles load
```

---

## Related Projects

- **Multi-Agent Log Resolution** - Separate package for macOS logs
- Both use the same 3-layer architecture
- Can be used independently

---

## Support

- Check `directives/reddit_daily_summary.md` for process docs
- Review `AGENTS.md` for agent instructions
- See script comments for implementation details

---

## Future Enhancements

- [ ] Add sentiment analysis
- [ ] Trend detection over time
- [ ] Geographic clustering
- [ ] Real-time monitoring
- [ ] Web dashboard
- [ ] Email reports
- [ ] Slack integration

---

## License

MIT License - Free to use, modify, distribute.

---

## Quick Start Checklist

- [ ] Copy `env.example` to `.env`
- [ ] Add API keys to `.env`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Obtain Reddit/RSS data (use RSS_fetch_package or other tools)
- [ ] Run workflow: clean → evaluate → cluster → summarize
- [ ] Check outputs in `.tmp/`

---

**Ready to analyze HVAC discussions?**

```bash
# Setup
cp env.example .env
# (edit .env with your keys)
pip install -r requirements.txt

# Run (assuming you have data in .tmp/)
python3 execution/clean_reddit_data.py
python3 execution/cluster_stories.py
python3 execution/summarize_clusters.py
```

**Version:** 1.0.0
**Updated:** 2026-01-08
**Portable:** Yes - move folder anywhere
