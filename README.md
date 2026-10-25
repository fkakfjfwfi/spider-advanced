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

## ⚖️ 合规声明

本站内容仅用于技术学习。爬虫请遵守目标网站 robots.txt 与服务条款、控制访问频率；JS 逆向相关内容仅适用于猿人学、Scrape Center 等**授权练习平台**与学习研究用途；请勿用于破坏技术措施、采集个人隐私或任何违法违规场景。
