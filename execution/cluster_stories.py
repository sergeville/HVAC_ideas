import json
import os
import argparse
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def cluster_stories(input_file, output_file, distance_threshold=0.5):
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found.")
        return

    with open(input_file, 'r') as f:
        posts = json.load(f)

    if not posts:
        print("No posts to cluster.")
        return

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        return

    genai.configure(api_key=api_key)

    print(f"Generating embeddings for {len(posts)} posts...")
    
    # Prepare text for embedding: "Title: [title] Summary: [snippet]"
    texts_to_embed = [
        f"Title: {post['title']} Content: {post['text'][:200]}" 
        for post in posts
    ]
    
    try:
        # Batch embedding if supported, or loop. "models/text-embedding-004" is the latest stable often used
        # Note: 'models/embedding-001' is older. Check strict model name. 
        # Using 'models/text-embedding-004' is generally safe for newer Gemini SDKs.
        model = 'models/text-embedding-004'
        embeddings = []
        
        # Batch requests to avoid rate limits or payload limits
        batch_size = 50
        for i in range(0, len(texts_to_embed), batch_size):
            batch = texts_to_embed[i:i+batch_size]
            result = genai.embed_content(
                model=model,
                content=batch,
                task_type="clustering"
            )
            embeddings.extend(result['embedding'])
            
        embeddings = np.array(embeddings)
        print(f"Embeddings shape: {embeddings.shape}")
        
        # Clustering
        # Agglomerative Clustering with cosine distance is good for text
        # But sklearn default is euclidean. Normalizing vectors makes euclidean ~= cosine ranking.
        # Normalize embeddings to unit length
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized_embeddings = embeddings / norms
        
        # Distance threshold needs tuning. 0.5 is a starting point for cosine-like distance (if using proper metric)
        # Using default euclidean on normalized vectors: distance = sqrt(2*(1-cos_sim))
        # if cos_sim = 0.8 (high sim), dist = sqrt(2*0.2) = sqrt(0.4) ~= 0.63
        # if cos_sim = 0.9, dist = sqrt(0.2) ~= 0.44
        # Let's start with threshold = 0.6 (implies cos_sim ~ 0.82)
        
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=0.6, 
            metric='euclidean', 
            linkage='average'
        )
        labels = clustering.fit_predict(normalized_embeddings)
        
        # Group posts by cluster
        clusters = {}
        for post_idx, cluster_id in enumerate(labels):
            cluster_id = str(cluster_id)
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(posts[post_idx])
            
        # Format output: List of "Stories" (clusters)
        clustered_output = []
        for cid, cluster_posts in clusters.items():
            clustered_output.append({
                "cluster_id": cid,
                "posts": cluster_posts,
                "size": len(cluster_posts)
            })
            
        # Sort by size (largest stories first)
        clustered_output.sort(key=lambda x: x['size'], reverse=True)
        
        print(f"Created {len(clustered_output)} clusters/stories from {len(posts)} posts.")
        print(f"Top 3 cluster sizes: {[c['size'] for c in clustered_output[:3]]}")
        
        with open(output_file, 'w') as f:
            json.dump(clustered_output, f, indent=2)
            
    except Exception as e:
        print(f"Error during embedding/clustering: {e}")

def main():
    parser = argparse.ArgumentParser(description="Cluster Reddit posts by topic")
    parser.add_argument("--input", default=".tmp/clean_posts.json", help="Input cleaned JSON file")
    parser.add_argument("--output", default=".tmp/clustered_posts.json", help="Output clustered JSON file")
    
    args = parser.parse_args()
    cluster_stories(args.input, args.output)

if __name__ == "__main__":
    main()
