@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === 爬虫进阶 · 推送到 GitHub ===
git remote -v | findstr origin >nul
if errorlevel 1 (
  echo [!] 还没有关联远程仓库。请先完成 README.md "发布到 GitHub Pages" 的第 1~2 步：
  echo     git remote add origin https://github.com/你的用户名/仓库名.git
  pause
  exit /b
)
git add -A
set /p MSG=更新说明（直接回车默认为"更新内容"）:
if "%MSG%"=="" set MSG=更新内容
git commit -m "%MSG%"
git push
if errorlevel 1 (
  echo.
  echo [x] 推送失败。检查网络 / 仓库地址 / 登录凭据后重试。
) else (
  echo.
  echo [OK] 已推送！1~2 分钟后 GitHub Pages 自动更新。
)
pause
