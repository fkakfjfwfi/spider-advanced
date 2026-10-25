@echo off
chcp 65001 >nul
title 爬虫进阶
echo 正在启动 爬虫进阶 ...
start "爬虫进阶服务(勿关)" /min python -m http.server 8018 --bind 127.0.0.1 --directory "%~dp0"
ping -n 2 127.0.0.1 >nul
start "" http://127.0.0.1:8018/index.html
echo.
echo 浏览器已打开 http://127.0.0.1:8018/index.html
echo 若未自动打开，请手动访问该地址；关闭最小化的"爬虫进阶服务"窗口即停止服务。
echo 在线版（GitHub Pages）与本地版进度互通说明见 README.md。
pause
