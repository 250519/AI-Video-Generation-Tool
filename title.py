# import json
# import urllib.request
# import pandas as pd
# import os
# import google.generativeai as genai
# import requests
# from dotenv import load_dotenv

# # === Load Environment Variables ===
# load_dotenv()

# # === Gemini API Setup ===
# api_key_gemini = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=api_key_gemini)
# llm = genai.GenerativeModel(
#     model_name="gemini-2.0-flash",
#     generation_config={"temperature": 0.9}
# )

# # === Fetch Top Headline (from GNews) ===
# apikey_gnews = os.getenv("GNEWS_API_KEY")
# if not apikey_gnews:
#     raise ValueError("GNEWS_API_KEY not found in environment variables.")
# category = "general"
# url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max=1&apikey={apikey_gnews}"

# headers_gnews = {
#     "User-Agent": "Mozilla/5.0"
# }
# req = urllib.request.Request(url, headers=headers_gnews)

# try:
#     with urllib.request.urlopen(req) as response:
#         data = json.loads(response.read().decode("utf-8"))
#         articles = data.get("articles", [])

#         if articles:
#             article = articles[0]  # Top-most article
#             title = article.get("title", "No Title")
#             description = article.get("description", "No Description")
            
#             print(f"Fetched Top News Title: {title}")
#             print(f"Fetched Description: {description}")

#             # === Prepare Prompt for Gemini ===
#             prompt = f"""
# You are an expert short-form video scriptwriter specializing in viral and engaging content for social media platforms like Instagram Reels, YouTube Shorts, and TikTok.

# Task:
# - Generate a crisp, energetic, and highly engaging script based on the provided news topic.
# - The script should be suitable for a 30-60 second video format.
# - Maintain a conversational and exciting tone while still being informative and trustworthy.
# - Start with a hook that instantly grabs attention in the first 5 seconds.
# - Use simple, relatable language that an average social media user can understand.
# - End with a punchline, question, or call-to-action to boost audience interaction.

# Input:
# Title: {title}

# Description: {description}

# Additional Guidelines:
# - Keep sentences short and impactful.
# - Prefer active voice over passive voice.
# - Include a slight emotional appeal if appropriate (e.g., wonder, excitement, urgency).
# - Use rhetorical questions if it fits naturally.
# - No hashtags, emojis, or platform mentions in the script.

# Deliver only the script. Avoid any preamble or explanations.
# """


#             # === Generate Script using Gemini ===
#             response = llm.generate_content(prompt)
#             generated_script = response.text.strip()

#             print("\n=== Generated Video Script ===\n")
#             print(generated_script)

#             # === Optional: Truncate Script if Too Long (max 1000 characters for 30-60s) ===
#             if len(generated_script) > 950:
#                 generated_script = generated_script[:950] + "..."

#             # === Send Script to Video Generation API ===

#             video_api_key = os.getenv("VIDEO_API_KEY")  # Make sure to set VIDEO_API_KEY in .env

#             video_api_url = "https://viralapi.vadoo.tv/api/generate_video"

#             headers_video = {
#                 "X-API-KEY": video_api_key,
#                 "Content-Type": "application/json"
#             }

#             body = {
#                 "topic": "Custom",
#                 "prompt": generated_script
#             }

#             video_response = requests.post(video_api_url, headers=headers_video, json=body)

#             if video_response.status_code == 200:
#                 video_data = video_response.json()
#                 vid = video_data.get("vid")
#                 print(f"\n✅ Video generation request successful! Video ID: {vid}")
#             else:
#                 print(f"\n❌ Failed to request video generation. Status Code: {video_response.status_code}")
#                 print(video_response.text)

#         else:
#             print("No articles found!")

# except Exception as e:
#     print(f"An error occurred: {e}")


import requests
import json

# Your AIMLAPI Key (replace here)
aimlapi_key = "c950cd7e742749a2a423e49b198b7e4f"

# Your text prompt (this should be your Gemini-generated script or any text)
prompt_text = """
Imagine exploring the ancient temples of Bali at sunrise, feeling the sacred energy in the air, followed by a refreshing dip in a hidden waterfall deep in the jungle...
"""  # Replace this with your dynamic script

# API Request
response = requests.post(
    "https://api.aimlapi.com/v2/generate/video/google/generation",
    headers={
        "Authorization": f"Bearer {aimlapi_key}",
        "Content-Type": "application/json"
    },
    data=json.dumps({
        "model": "veo2",         # Model used (as per API docs)
        "prompt": prompt_text,   # Your text prompt
        "aspect_ratio": "16:9",  # Can use "9:16" for vertical
        "duration": 5            # Duration in seconds (you can adjust)
    })
)

# Handle the API Response
if response.status_code == 200:
    print("✅ Video generation request successful!")
    data = response.json()
    print(json.dumps(data, indent=4))
else:
    print(f"❌ Failed with Status Code: {response.status_code}")
    print(response.text)


