import json
import os
import argparse
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def summarize_posts(input_file, output_dir):
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found.")
        return

    with open(input_file, 'r') as f:
        signal_posts = json.load(f)

    if not signal_posts:
        print("No signal posts to summarize.")
        return

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prepare data for summary
    posts_text = ""
    for i, post in enumerate(signal_posts, 1):
        posts_text += f"{i}. Title: {post['title']}\n   Link: {post['link']}\n   Key Point: {post.get('evaluation', '')}\n\n"

    prompt = f"""
    You are an expert AI & Automation trend analyst.
    Below is a list of high-signal Reddit posts identified today.
    
    Your task:
    1. Synthesize these into a meaningful daily summary. 
    2. Group them by common themes (e.g., "New Tools", "Strategy", "Problems to Solve").
    3. highlighting the core ideas and opportunities.
    4. Keep it concise and readable.
    
    Input Posts:
    {posts_text}
    
    Output Format:
    # Daily AI & Automation Digest - {datetime.now().strftime('%Y-%m-%d')}
    
    ## Executive Summary
    [1-2 sentences on today's vibe]
    
    ## Key Themes
    
    ### [Theme Name]
    - **[Title of Post]**: [Brief summary of insight]
    
    ## Opportunities
    - [Bullet points on potential money-making or audience-growth angles found]
    """
    
    print("Generating summary...")
    try:
        response = model.generate_content(prompt)
        summary_text = response.text
        
        # Ensure output dir exists
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"daily_summary_{datetime.now().strftime('%Y-%m-%d')}.txt"
        output_path = os.path.join(output_dir, filename)
        
        with open(output_path, 'w') as f:
            f.write(summary_text)
            
        print(f"Summary written to {output_path}")
        
    except Exception as e:
        print(f"Error generating summary: {e}")

def main():
    parser = argparse.ArgumentParser(description="Summarize signal posts")
    parser.add_argument("--input", default=".tmp/signal_posts.json", help="Input signal JSON file")
    parser.add_argument("--output_dir", default="outputs", help="Directory for output text files")
    
    args = parser.parse_args()
    summarize_posts(args.input, args.output_dir)

if __name__ == "__main__":
    main()
