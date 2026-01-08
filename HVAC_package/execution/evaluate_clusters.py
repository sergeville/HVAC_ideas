import json
import os
import argparse
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def evaluate_clusters(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found.")
        return

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.0-flash')

    with open(input_file, 'r') as f:
        clusters = json.load(f)

    print(f"Evaluating {len(clusters)} clusters...")
    
    signal_clusters = []
    
    for i, cluster in enumerate(clusters):
        posts = cluster['posts']
        print(f"  Processing cluster {i+1}/{len(clusters)} (size: {len(posts)})...")
        
        # Prepare content digest for the cluster
        posts_digest = ""
        for j, p in enumerate(posts[:5]):
            posts_digest += f"Post {j+1}: {p['title']} (Snippet: {p['text'][:150]})\n"
            
        if len(posts) > 5:
            posts_digest += f"... and {len(posts)-5} more posts like this.\n"

        prompt = f"""
        You are an Editor evaluating potential stories for an AI & Automation Newsletter.
        
        Here is a cluster of related Reddit posts:
        {posts_digest}
        
        Task:
        1. Identify the core "Story" or topic here.
        2. Determine if this story is "Signal" (Relevant to AI/Automation money/growth, Concrete, Actionable) or "Noise" (Generic questions, Memes, Spam, Low-effort).
        3. If Signal, provide a catchy Headline and a 1-sentence "Angle" (why it matters).
        
        Resond with JSON ONLY:
        {{
            "is_signal": true/false,
            "story_headline": "...",
            "story_angle": "...",
            "reason": "..."
        }}
        """
        
        # Retry logic with exponential backoff
        max_retries = 5
        base_delay = 5
        
        for attempt in range(max_retries):
            try:
                # Add a small buffer before request to help free tier limits
                time.sleep(2) 
                
                response = model.generate_content(prompt)
                text_resp = response.text.strip()
                
                if text_resp.startswith("```json"):
                    text_resp = text_resp[7:-3]
                elif text_resp.startswith("```"):
                    text_resp = text_resp[3:-3]
                    
                eval_result = json.loads(text_resp)
                
                if eval_result.get('is_signal'):
                    cluster['evaluation'] = eval_result
                    signal_clusters.append(cluster)
                    print(f"    [SIGNAL] {eval_result['story_headline']}")
                else:
                    # print(f"    [NOISE] {eval_result.get('reason')}")
                    pass
                
                # Success, break retry loop
                break
                
            except Exception as e:
                if "429" in str(e):
                    delay = base_delay * (2 ** attempt)
                    print(f"    Rate limit hit. Retrying in {delay}s... (Attempt {attempt+1}/{max_retries})")
                    time.sleep(delay)
                else:
                    print(f"    Error evaluating cluster: {e}")
                    break
            
    print(f"Found {len(signal_clusters)} signal stories out of {len(clusters)} raw clusters.")
    
    with open(output_file, 'w') as f:
        json.dump(signal_clusters, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Evaluate Clusters for Signal")
    parser.add_argument("--input", default=".tmp/clustered_posts.json", help="Input Clustered JSON")
    parser.add_argument("--output", default=".tmp/signal_clusters.json", help="Output Signal Clusters JSON")
    
    args = parser.parse_args()
    evaluate_clusters(args.input, args.output)

if __name__ == "__main__":
    main()
