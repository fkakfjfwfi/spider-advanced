# 🕷 爬虫进阶

一个纯静态、零依赖、可离线使用的爬虫体系课网站。

- **知识体系**对齐崔庆才《Python3网络爬虫开发实战（第二版）》（15 章核心全映射）与主流 JS 逆向实战体系；
- **多源精读**：聚合韦世东《Python3反爬虫原理与绕过实战》、Ryan Mitchell《Python网络爬虫权威指南》、《精通Scrapy网络爬虫》、K哥《JS逆向百例》、夜幕团队 NightTeam 等全网高质量来源；
- **面向有基础的学习者**：每章标出与考研 408（计算机网络/操作系统/数据库/密码学）已有知识的连接点；
- **可视化教学**：6 集动画课堂（可拖进度、倍速、字幕）+ 7 个互动实验室（请求解剖台、选择器游乐场、参数实验室、403 实验室、加密算法训练场、Scrapy 架构图、并发模拟器）；
- **练习驱动**：每章配套练习 + 24 道分级题库 + 授权平台闯关任务卡；
- **进度打卡**：60 个知识点，localStorage 自动保存。

## 📂 目录结构

```
├── index.html            # 课程总览（知识体系 / 学习路径 / 动画课堂索引）
├── ch01~ch10.html        # 十章课程（每章末标注对应教材章节）
├── library.html          # 多源图书馆（全网优质资源地图）
├── practice.html         # 练习场（题库 + 闯关任务卡）
├── assets/               # style.css / app.js(进度) / lesson-player.js(动画引擎)
└── docs/                 # 爬虫高手养成计划.md
```

## 🚀 本地使用

- 双击 `启动网站.bat`（Windows，需 Python），或直接双击 `index.html`；
- 或任意静态服务器：`python -m http.server 8018` 后访问 `http://127.0.0.1:8018/`。

## 🌐 发布到 GitHub Pages（首次，约 3 分钟）

1. 在 GitHub 新建一个 **Public** 仓库（如 `spider-advanced`，不要勾选自动生成 README）；
2. 在本文件夹打开终端（或 Git Bash）执行：

```bash
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git branch -M main
git push -u origin main
```

3. 仓库页 → Settings → Pages → Source 选 **Deploy from a branch** → Branch 选 **main / (root)** → Save；
4. 1~2 分钟后访问 `https://<你的用户名>.github.io/<仓库名>/`。

> 站内所有链接均为相对路径，放在仓库根目录即可在 `/<仓库名>/` 子路径下正常工作，无需任何配置。

## 🔄 日常更新

修改任意文件后：双击 `推送到GitHub.bat`（或手动 `git add -A && git commit -m "说明" && git push`），Pages 会自动重新发布。

## 🔒 安全加固

GitHub Pages **不允许自定义 HTTP 响应头**（无法下发 `Content-Security-Policy`、`X-Frame-Options`、`X-Content-Type-Options` 等），因此本站的安全策略全部写在页面 `<head>` 里：

- **CSP**（`<meta http-equiv="Content-Security-Policy">`，每个页面首行）：`default-src 'self'`，只允许加载本站资源；`object-src`、`base-uri`、`form-action`、`frame-src` 全部 `none`。效果：即使页面某处被注入内容，也无法加载外部脚本、往外部地址发数据、被 `<base>` 劫持相对路径或提交表单。
- **Referrer-Policy**：`strict-origin-when-cross-origin`，跨站跳转不泄露完整路径与参数。
- **防点击劫持**：`X-Frame-Options` 无法下发，改用脚本事前判断——被第三方页面 iframe 嵌套时自动跳回顶层或清空页面。
- **外链**：所有 `target="_blank"` 的链接统一 `rel="noopener noreferrer"`，防止被外链页面通过 `window.opener` 反向控制本页。

> ⚠️ 维护注意：改动页面时不要删除 `<head>` 里那段 `SECURITY-HARDENING` 注释包裹的代码。如果新增了**外部**脚本、样式、图片或 `fetch` 请求，必须同步修改 CSP 的对应指令，否则浏览器会拦截。

**仓库侧才是最大风险点**（代码层防护挡不住别人拿到你的 GitHub 账号）：

1. GitHub 账号务必开启 **2FA**；
2. 仓库 Settings → Branches 加一条保护规则（禁止直接 push 到 `main`，或至少要求 PR）；
3. 这个仓库里**永远不要**提交任何 token / Cookie / 账号密码（公开仓库 = 全网可见）；
4. 若以后迁到 Cloudflare Pages / Netlify / Vercel，可补一份真实响应头（`_headers` 文件），把 CSP 从前端 `<meta>` 升级为服务端下发，并加上 `X-Content-Type-Options: nosniff`。

## ⚖️ 合规声明

本站内容仅用于技术学习。爬虫请遵守目标网站 robots.txt 与服务条款、控制访问频率；JS 逆向相关内容仅适用于猿人学、Scrape Center 等**授权练习平台**与学习研究用途；请勿用于破坏技术措施、采集个人隐私或任何违法违规场景。
