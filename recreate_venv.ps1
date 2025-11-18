# 重新创建虚拟环境脚本
# 使用方法：.\recreate_venv.ps1

Write-Host "正在删除旧的虚拟环境..." -ForegroundColor Yellow
if (Test-Path .\venv) {
    Remove-Item -Recurse -Force .\venv
    Write-Host "旧虚拟环境已删除" -ForegroundColor Green
}

Write-Host "`n正在创建新的虚拟环境..." -ForegroundColor Yellow
python -m venv venv

Write-Host "`n正在激活虚拟环境..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

Write-Host "`n正在升级 pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host "`n正在安装依赖..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`n虚拟环境重新创建完成！" -ForegroundColor Green
Write-Host "现在可以运行: python -m app.main" -ForegroundColor Yellow

