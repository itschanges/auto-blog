import os
import requests
import re

def clean_html_output(text):
    # 删除所有 Markdown 标题（# 开头）
    text = re.sub(r"^#+.*$", "", text, flags=re.MULTILINE)

    # 删除 Edge metadata 或系统提示（包含 “metadata” 或 “browser tabs”）
    text = re.sub(r".*browser tabs metadata.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r".*Edge browser.*", "", text, flags=re.IGNORECASE)

    # 删除代码块 ```...```
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    # 删除多余空行
    text = re.sub(r"\n{2,}", "\n", text)

    return text.strip()


def extract_title_and_content(html):
    # 优先使用 <h1>
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.IGNORECASE)
    if m:
        title = m.group(1).strip()
        content = html
        return title, content

    # 其次使用 <h2>
    m = re.search(r"<h2[^>]*>(.*?)</h2>", html, flags=re.IGNORECASE)
    if m:
        title = m.group(1).strip()
        content = html
        return title, content

    # 如果没有 HTML 标题，则用第一行文本
    lines = html.splitlines()
    title = lines[0].strip()
    content = "\n".join(lines[1:]).strip()
    return title, content


def generate_article():
    api_key = os.environ["GH_MODELS_API_KEY"]

    url = "https://models.inference.ai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-10-01-preview"

    prompt = """
你是一名中文战地作者，请g根据最新的主流权威新闻生成一篇关于"最新美国-以色列-伊朗战事发展"+"日期和时间" 的最新报道原创文章。

必须严格遵守以下要求：
1. **只输出 HTML，不要输出 Markdown**
2. **不要输出任何系统信息、元数据、注释、解释、说明**
3. **不要输出 #、##、### 这样的 Markdown 标题**
4. **文章必须以 <h1> 或 <h2> 开头作为标题**
5. **正文必须包含 <p>、<ul>、<li> 等 HTML 标签**
6. **不要输出代码块，不要输出 ```**
7. **不要输出与浏览器、系统、AI 模型相关的任何内容**

示例结构（仅供参考，不要照抄内容）：
<h1>标题</h1>
<p>段落内容……</p>
<h2>小节标题</h2>
<ul>
  <li>要点 1</li>
  <li>要点 2</li>
</ul>
"""

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()

    raw = resp.json()["choices"][0]["message"]["content"]

    # 清洗非 HTML 内容
    html = clean_html_output(raw)

    # 提取标题与正文
    title, content = extract_title_and_content(html)

    return title, content


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
