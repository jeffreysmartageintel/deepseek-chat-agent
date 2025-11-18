# 安装 DeepSeek Chat Agent 依赖
# 确保虚拟环境已激活

Write-Host "正在安装依赖包..." -ForegroundColor Green

# 安装基础依赖
pip install -r requirements.txt

# 确保安装了 openai 和 langchain-openai
Write-Host "`n正在安装 openai 和 langchain-openai..." -ForegroundColor Green
pip install openai langchain-openai

Write-Host "`n依赖安装完成！" -ForegroundColor Green
Write-Host "现在可以运行: python -m app.main" -ForegroundColor Yellow

