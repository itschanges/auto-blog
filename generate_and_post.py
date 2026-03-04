import os
import requests
import google.generativeai as genai

# ====== 1. AI 生成文章 ======
def generate_article():
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = """
你是一名中文科技博客作者，请生成一篇关于"OpenWrt 家庭网络优化"的原创文章。
要求：
- 字数 1500~2500
- HTML 格式输出（包含 <h2>, <p>, <ul>, <li>）
- 风格通俗易懂，适合普通用户
"""

    response = model.generate_content(prompt)
    html = response.text

    # 第一行作为标题
    lines = html.splitlines()
    title = lines[0].replace("#", "").strip()
    content = "\n".join(lines[1:]).strip()

    return title, content

# ====== 2. 发布到 WordPress ======
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