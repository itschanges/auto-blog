import os
import requests

# 1. 使用 GitHub Models 生成文章
def generate_article():
    api_key = os.environ["GH_MODELS_API_KEY"]

    url = "https://models.inference.ai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-10-01-preview"


    prompt = """
你是一名中文战地作者，请生成一篇关于"最新美国-以色列-伊朗战事发展"的最新报道原创文章。
要求：
- 字数 1500~2500
- HTML 格式输出（包含 <h2>, <p>, <ul>, <li>）
- 风格通俗易懂，适合普通用户
"""


    payload = {
        "model": "gpt-4o-mini",  # GitHub Models 免费模型
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()

    html = resp.json()["choices"][0]["message"]["content"]

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

