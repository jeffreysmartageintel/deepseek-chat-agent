# PowerShell 脚本：测试 DeepSeek Chat Agent API
# 使用方法：.\test_api_powershell.ps1

$baseUrl = "http://localhost:8080"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "测试 DeepSeek Chat Agent API" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 测试 1: 健康检查
Write-Host "1. 测试健康检查端点..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/health" -Method GET -UseBasicParsing
    Write-Host "✓ 状态码: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "响应内容:" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
    Write-Host ""
} catch {
    Write-Host "❌ 错误: $_" -ForegroundColor Red
    Write-Host "请确保服务正在运行！" -ForegroundColor Red
    Write-Host "启动命令: python -m app.start_server" -ForegroundColor Yellow
    Write-Host "或: uvicorn app.main:app --reload --host 0.0.0.0 --port 8080" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# 测试 2: 简化聊天接口
Write-Host "2. 测试简化聊天接口..." -ForegroundColor Yellow
try {
    $params = @{
        user_input = "你好，请介绍一下你自己"
    }
    $queryString = ($params.GetEnumerator() | ForEach-Object { "$($_.Key)=$([System.Web.HttpUtility]::UrlEncode($_.Value))" }) -join "&"
    $url = "$baseUrl/api/chat/simple?$queryString"
    
    $response = Invoke-WebRequest -Uri $url -Method POST -UseBasicParsing -ContentType "application/json"
    Write-Host "✓ 状态码: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "响应内容:" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
    Write-Host ""
} catch {
    Write-Host "❌ 错误: $_" -ForegroundColor Red
    Write-Host ""
}

# 测试 3: 完整聊天接口
Write-Host "3. 测试完整聊天接口..." -ForegroundColor Yellow
try {
    $body = @{
        messages = @(
            @{
                role = "user"
                content = "什么是人工智能？"
            }
        )
        temperature = 0.7
        max_tokens = 5000
    } | ConvertTo-Json -Depth 10
    
    $response = Invoke-WebRequest -Uri "$baseUrl/api/chat" `
        -Method POST `
        -Body $body `
        -ContentType "application/json" `
        -UseBasicParsing
    
    Write-Host "✓ 状态码: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "响应内容:" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
    Write-Host ""
} catch {
    Write-Host "❌ 错误: $_" -ForegroundColor Red
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "测试完成！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

