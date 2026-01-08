import json
import os
import argparse
import time
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def summarize_clusters(input_file, output_dir):
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found.")
        return

    with open(input_file, 'r') as f:
        signal_clusters = json.load(f)

    if not signal_clusters:
        print("No signal clusters to summarize.")
        return

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    
    # Prepare data for final newsletter generation
    stories_content = ""
    for i, cluster in enumerate(signal_clusters, 1):
        eval_data = cluster.get('evaluation', {})
        headline = eval_data.get('story_headline', 'Untitled Story')
        angle = eval_data.get('story_angle', '')
        
        # Collect top links from the cluster
        # Maybe picking the top 3 specific posts to cite
        top_posts = cluster['posts'][:3]
        links = ", ".join([p.get('link') for p in top_posts])
        
        stories_content += f"""
        Story {i}: {headline}
        Angle: {angle}
        Related Links: {links}
        -----------------------
        """

    prompt = f"""
    You are the Editor-in-Chief of a premium "AI & Automation" Daily Newsletter.
    
    Below are the top "Stories" identified today (already pre-filtered for quality).
    
    Your Task:
    1. Write the final newsletter in markdown format.
    2. Start with a catchy "Daily Vibe" or Executive Summary (1-2 sentences).
    3. For EACH Story, write a short, punchy paragraph. Focus on the VALUE (What happened, Why it matters, How to profit/grow).
    4. Group stories logically if possible (e.g. "Tool Launches", "Strategy", "Discussion").
    5. Keep the tone professional but exciting ("Alpha" focused).
    
    Input Stories:
    {stories_content}
    
    Output Format:
    # 🤖 AI & Auto Daily - {datetime.now().strftime('%Y-%m-%d')}
    
    ## ⚡ The Vibe
    [Summary]
    
    ## 🚀 Top Stories
    ...
    
    ## 🛠️ Tools & Tactics
    ...
    """
    
    print("Generating Newsletter...")
    print("Generating Newsletter...")
    
    max_retries = 5
    base_delay = 5
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            newsletter_text = response.text
            
            os.makedirs(output_dir, exist_ok=True)
            filename = f"newsletter_{datetime.now().strftime('%Y-%m-%d')}.txt"
            output_path = os.path.join(output_dir, filename)
            
            with open(output_path, 'w') as f:
                f.write(newsletter_text)
                
            print(f"Newsletter written to {output_path}")
            break
            
        except Exception as e:
            if "429" in str(e):
                delay = base_delay * (2 ** attempt)
                print(f"Rate limit hit. Retrying in {delay}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(delay)
            else:
                print(f"Error generating newsletter: {e}")
                break

def main():
    parser = argparse.ArgumentParser(description="Generate Newsletter from Clusters")
    parser.add_argument("--input", default=".tmp/signal_clusters.json", help="Input Signal Clusters JSON")
    parser.add_argument("--output_dir", default="outputs", help="Directory for output files")
    
    args = parser.parse_args()
    summarize_clusters(args.input, args.output_dir)

if __name__ == "__main__":
    main()
