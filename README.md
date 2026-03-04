# 🧱 Vercel + GitHub Actions + Google AI Studio + WordPress 自动发文系统

这个系统每天自动运行一次：

1. GitHub Actions 定时触发  
2. Python 脚本调用 **Google AI Studio（Gemini）** 生成文章  
3. 自动发布到 **WordPress**  
4. 全程无人值守

---

## 📦 系统准备

### 1. 创建 Google AI Studio API Key
进入：https://aistudio.google.com/apikey

创建一个 Key（不要公开）。

### 2. WordPress 启用应用密码
WordPress 后台 → 用户 → Profile → Application Passwords  
创建一个新的应用密码，记录下来。

### 3. GitHub 仓库结构

```
auto-blog/
├─ generate_and_post.py
├─ requirements.txt
└─ .github/
   └─ workflows/
      └─ auto-post.yml
```

---

## 🔐 GitHub Secrets 配置

进入 GitHub 仓库 → Settings → Secrets → Actions → New Secret  
添加以下内容：

| Secret 名称 | 内容 |
|------------|------|
| `GOOGLE_API_KEY` | Google AI Studio API Key |
| `WP_URL` | 例如 `https://ict.135799.xyz` |
| `WP_USER` | WordPress 用户名，例如 `admin` |
| `WP_APP_PASSWORD` | WordPress 应用密码 |

---

## 🚀 运行方式

### 自动运行
- 每天 09:00 中国时间（UTC+8）自动执行

### 手动运行
进入 GitHub 仓库 → Actions → Auto Post Blog → Run workflow

---

## 📝 文件说明

- **generate_and_post.py**: 主脚本，负责生成文章并发布到 WordPress
- **requirements.txt**: Python 依赖包列表
- **.github/workflows/auto-post.yml**: GitHub Actions 工作流配置

---

## ✅ 配置检查清单

- [ ] Google AI Studio API Key 已创建
- [ ] WordPress 应用密码已创建
- [ ] GitHub Secrets 已配置
- [ ] 工作流文件已上传
- [ ] Python 脚本已上传

完成以上步骤后，系统即可自动运行！