# Gradio UI 启动脚本
# 使用方法：.\start_gradio_ui.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DeepSeek Chat Agent - Gradio UI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "请选择启动方案：" -ForegroundColor Yellow
Write-Host "1. 集成方案（推荐）- 直接使用LLM，性能最佳" -ForegroundColor Green
Write-Host "2. 分离方案 - 通过API调用，需要先启动main.py" -ForegroundColor Yellow
Write-Host ""

$choice = Read-Host "请输入选项 (1 或 2)"

if ($choice -eq "1") {
    Write-Host "`n正在启动集成方案..." -ForegroundColor Green
    Write-Host "访问地址: http://localhost:7860" -ForegroundColor Cyan
    Write-Host ""
    python -m app.gradio_app
}
elseif ($choice -eq "2") {
    Write-Host "`n注意：分离方案需要先启动 API 服务！" -ForegroundColor Yellow
    Write-Host "请确保在另一个终端运行: python -m app.main" -ForegroundColor Yellow
    Write-Host ""
    $confirm = Read-Host "API服务已启动？(y/n)"
    
    if ($confirm -eq "y" -or $confirm -eq "Y") {
        Write-Host "`n正在启动分离方案..." -ForegroundColor Green
        Write-Host "访问地址: http://localhost:7860" -ForegroundColor Cyan
        Write-Host ""
        python -m app.gradio_app_api
    }
    else {
        Write-Host "`n请先启动 API 服务：" -ForegroundColor Red
        Write-Host "python -m app.main" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "然后在另一个终端运行此脚本并选择选项2" -ForegroundColor Yellow
    }
}
else {
    Write-Host "`n无效选项，请重新运行脚本" -ForegroundColor Red
}

