import json
import os
import argparse
import google.generativeai as genai
from dotenv import load_dotenv

# Load env
load_dotenv()

def evaluate_posts(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found.")
        return

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    with open(input_file, 'r') as f:
        posts = json.load(f)

    signal_posts = []
    print(f"Evaluating {len(posts)} posts...")

    for post in posts:
        # Create a concise representation for the LLM
        post_content = f"Title: {post['title']}\nLink: {post['link']}\nContent Snippet: {post['text'][:500]}..."
        
        prompt = f"""
        Analyze the following Reddit post and determine if it is "Signal" or "Noise".
        
        Criteria for SIGNAL:
        1. Relevant to AI and automation for making money or growing an audience.
        2. Contains concrete details, insights, or actionable advice.
        3. Suggests a real problem, idea, or opportunity.
        
        Post:
        {post_content}
        
        Respond with ONLY a JSON object: {{"is_signal": true/false, "reason": "short explanation"}}
        """
        
        try:
            response = model.generate_content(prompt)
            # simplistic json extraction (handling potential markdown fences)
            text_resp = response.text.strip()
            if text_resp.startswith("```json"):
                text_resp = text_resp[7:-3]
            elif text_resp.startswith("```"):
                text_resp = text_resp[3:-3]
            
            result = json.loads(text_resp)
            
            if result.get('is_signal'):
                post['evaluation'] = result.get('reason')
                signal_posts.append(post)
                print(f"  [SIGNAL] {post['title']}")
            else:
                # print(f"  [NOISE] {post['title']}")
                pass
                
        except Exception as e:
            print(f"  Error evaluating post {post.get('title', 'Unknown')}: {e}")

    print(f"Found {len(signal_posts)} signal posts out of {len(posts)} total.")
    
    with open(output_file, 'w') as f:
        json.dump(signal_posts, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Evaluate Reddit posts for signal/noise")
    parser.add_argument("--input", default=".tmp/clean_posts.json", help="Input cleaned JSON file")
    parser.add_argument("--output", default=".tmp/signal_posts.json", help="Output signal JSON file")
    
    args = parser.parse_args()
    evaluate_posts(args.input, args.output)

if __name__ == "__main__":
    main()
