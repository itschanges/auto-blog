import os
import requests
from google import genai

# 1. 使用 Google Gemini 2.0 Flash 生成文章
def generate_article():
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


    prompt = """
你是一名中文战地作者，请生成一篇关于"最新美国-以色列-伊朗战事发展"的最新报道原创文章。
要求：
- 字数 1500~2500
- HTML 格式输出（包含 <h2>, <p>, <ul>, <li>）
- 风格通俗易懂，适合普通用户
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )

    html = response.text

    # 第一行作为标题
    lines = html.splitlines()
    title = lines[0].replace("#", "").strip()
    content = "\n".join(lines[1:]).strip()

    return title, content


# 2. 发布到 WordPress
def post_to_wordpress(title, content):
    wp_url = os.environ["WP_URL"].rstrip("/") + "/wp-json/wp/v2/posts"
    wp_user = os.environ["WP_USER"]
    wp_app_password = os.environ["WP_APP_PASSWORD"]

    data = {
        "title": title,
        "content": content,
        "status": "publish"
    }

    resp = requests.post(
        wp_url,
        json=data,
        auth=(wp_user, wp_app_password)
    )
    resp.raise_for_status()
    print("WordPress 发布成功:", resp.json().get("link"))


if __name__ == "__main__":
    title, content = generate_article()
    print("生成文章标题:", title)
    post_to_wordpress(title, content)
