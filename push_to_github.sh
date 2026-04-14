#!/bin/bash
# 推送 stock-analyzer-pro 到 GitHub

cd /Users/sunjian/.openclaw/workspace/skills/stock-analyzer-pro

# 1. 先在浏览器创建仓库：https://github.com/new
#    仓库名：stock-analyzer-pro
#    选择 Public 或 Private
#    不要勾选 README（已有）

# 2. 然后运行以下命令：

# 设置 Git 用户信息
git config user.name "dhwangluo-eng"
git config user.email "your-email@example.com"

# 添加远程仓库
git remote add origin https://github.com/dhwangluo-eng/stock-analyzer-pro.git

# 推送到 GitHub
git branch -M main
git push -u origin main

echo "✅ 推送完成！"
echo "📎 仓库地址：https://github.com/dhwangluo-eng/stock-analyzer-pro"
