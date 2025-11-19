# Windows PowerShell API 测试指南

## 问题说明

在 Windows PowerShell 中，`curl` 是 `Invoke-WebRequest` 的别名，语法与 Linux 的 curl 不同，可能导致连接错误。

## 解决方案

### 方案 1: 使用 Invoke-WebRequest（推荐）⭐

这是 PowerShell 的原生命令，语法正确：

```powershell
# 1. 健康检查
Invoke-WebRequest -Uri "http://localhost:8080/health" -Method GET -UseBasicParsing

# 2. 查看响应内容（JSON 格式化）
$response = Invoke-WebRequest -Uri "http://localhost:8080/health" -Method GET -UseBasicParsing
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### 方案 2: 使用测试脚本（最简单）⭐

运行项目根目录下的测试脚本：

```powershell
.\test_api_powershell.ps1
```

这个脚本会自动测试所有 API 端点。

### 方案 3: 使用 curl.exe（如果已安装 Git for Windows）

如果你安装了 Git for Windows，可以使用 `curl.exe`（注意是 `.exe` 后缀）：

```powershell
# 健康检查
curl.exe http://localhost:8080/health

# POST 请求
curl.exe -X POST "http://localhost:8080/api/chat" `
    -H "Content-Type: application/json" `
    -d '{\"messages\": [{\"role\": \"user\", \"content\": \"你好\"}]}'
```

### 方案 4: 使用浏览器（最简单直观）

1. **健康检查**:
   ```
   http://localhost:8080/health
   ```

2. **API 文档（Swagger UI）**:
   ```
   http://localhost:8080/docs
   ```
   在 Swagger UI 中可以：
   - 查看所有 API 端点
   - 直接测试 API
   - 查看请求/响应格式

3. **Gradio UI**:
   ```
   http://localhost:8080
   ```
   交互式聊天界面

## 常见错误及解决方法

### 错误 1: "无法连接到远程服务器"

**原因**:
- 服务没有启动
- 端口被占用
- 防火墙阻止

**解决方法**:

1. **检查服务是否运行**:
   ```powershell
   # 检查 8080 端口是否被占用
   netstat -ano | findstr :8080
   ```

2. **启动服务**:
   ```powershell
   # 启动 Gradio UI
   python -m app.start_server
   
   # 或启动 FastAPI 服务
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
   ```

3. **检查防火墙**:
   - 确保 Windows 防火墙允许 Python 访问网络
   - 或临时关闭防火墙测试

### 错误 2: PowerShell 执行策略限制

如果无法运行 `.ps1` 脚本，需要修改执行策略：

```powershell
# 查看当前执行策略
Get-ExecutionPolicy

# 临时允许运行脚本（当前会话）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 或永久允许（需要管理员权限）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 错误 3: curl 命令语法错误

**原因**: PowerShell 中的 `curl` 是 `Invoke-WebRequest` 的别名，语法不同。

**解决方法**: 使用 `Invoke-WebRequest` 或 `curl.exe`（如果已安装 Git）。

## 完整测试示例

### 测试健康检查

```powershell
$response = Invoke-WebRequest -Uri "http://localhost:8080/health" -Method GET -UseBasicParsing
Write-Host "状态码: $($response.StatusCode)"
$response.Content | ConvertFrom-Json | ConvertTo-Json
```

### 测试简化聊天接口

```powershell
$url = "http://localhost:8080/api/chat/simple?user_input=你好"
$response = Invoke-WebRequest -Uri $url -Method POST -ContentType "application/json" -UseBasicParsing
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### 测试完整聊天接口

```powershell
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

$response = Invoke-WebRequest -Uri "http://localhost:8080/api/chat" `
    -Method POST `
    -Body $body `
    -ContentType "application/json" `
    -UseBasicParsing

$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

## 推荐工作流程

1. **启动服务**:
   ```powershell
   python -m app.start_server
   ```

2. **打开浏览器访问**:
   - Gradio UI: `http://localhost:8080`
   - API 文档: `http://localhost:8080/docs`

3. **或运行测试脚本**:
   ```powershell
   .\test_api_powershell.ps1
   ```

## 需要帮助？

如果仍然遇到问题：
1. 检查服务日志，查看是否有错误信息
2. 确认 `.env` 文件配置正确
3. 确认所有依赖已正确安装
4. 查看 [LOCAL_RUN_GUIDE.md](LOCAL_RUN_GUIDE.md) 获取详细说明

