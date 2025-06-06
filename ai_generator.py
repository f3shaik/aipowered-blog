import os
from openai import OpenAI

# - A module (`ai_generator.py`) that calls OpenAI with a structured prompt to generate a blog post draft 
# (HTML or Markdown), replacing `{{AFF_LINK_n}}` placeholders with dummy URLs.

def generate_post(keyword: str, metrics: dict, api_key: str) -> str:
    API_KEY= os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY not present in environment, use valid key and try again")
    # basic prompt engineering for blog post
    sys_prompt = (
        "Act as a helpful blog-writing assistant.\n"
        "You generate a complete blog post in Markdown format, structured with:\n"
        "- A title that includes the keyword prominently.\n"
        "- An introduction paragraph (2–3 sentences) mentioning why the keyword matters.\n"
        "- 3–4 H2 sections (each with a heading that includes the keyword or a relevant subtopic).\n"
        "- In each section, write 3–4 sentences providing actionable information or tips.\n"
        "- A conclusion summarizing the main points and including a call to action, no matter how insignificant.\n"
        "- Insert three affiliate link placeholders named {{AFF_LINK_1}}, {{AFF_LINK_2}}, and {{AFF_LINK_3}} at logical points.\n"
        "- At the very top of the post (just below the title), include a bullet list showing the SEO metrics:\n"
        "  • Search Volume: {search_volume}\n"
        "  • Keyword Difficulty: {keyword_difficulty}\n"
        "  • Avg. CPC: ${cpc}\n"
        "Please make the output is pure Markdown (no HTML)."
    ).format(
        search_volume=metrics["search_volume"],
        keyword_difficulty=metrics["keyword_difficulty"],
        cpc=metrics["cpc"]
    )
    
    client = OpenAI(api_key=api_key)    # Updated method to use ChatCompletion
    user_prompt = f"Generate a blog post optimized for the keyword: {keyword}."
    post = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "system", "content": user_prompt}
        ],
        temperature = 0.7,
        max_tokens=850
    )
    return post.choices[0].message.content.strip()