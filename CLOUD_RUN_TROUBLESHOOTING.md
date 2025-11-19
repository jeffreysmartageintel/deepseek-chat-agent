# Cloud Run 部署故障排除指南

## 问题：容器启动超时

**错误信息：**
```
The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable within the allocated timeout.
```

## 解决方案

### 方案 1: 在 Cloud Run Console 中设置启动超时（推荐）

**注意**: `gcloud run deploy` 命令不支持 `--startup-timeout` 参数，需要在 Console 中设置。

**在 Cloud Run Console 中设置：**

1. 进入 Cloud Run 服务页面
2. 点击 "编辑和部署新版本"
3. 展开 "容器、变量、密钥、连接"
4. 在 "启动超时" 中设置为 **300 秒**（或更长）
5. 在 "请求超时" 中设置为 **300 秒**
6. 点击 "部署"

**使用 gcloud 命令部署（不包含启动超时）：**

```powershell
gcloud run deploy deepseek-chat-agent `
    --image us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:v1.0.0 `
    --platform managed `
    --region us-central1 `
    --project firbase-app1-17308 `
    --allow-unauthenticated `
    --set-env-vars DEEPSEEK_API_KEY=your_key,DEEPSEEK_API_BASE=https://api.deepseek.com/v1 `
    --memory 2Gi `
    --cpu 2 `
    --timeout 300 `
    --port 8080
```

**关键参数：**
- `--timeout 300`: 设置请求超时为 300 秒
- 启动超时需要在 Console 中手动设置

### 方案 2: 在 Cloud Run Console 中设置

1. 进入 Cloud Run 服务页面
2. 点击 "编辑和部署新版本"
3. 展开 "容器、变量、密钥、连接"
4. 在 "启动超时" 中设置为 **300 秒**（或更长）
5. 在 "请求超时" 中设置为 **300 秒**
6. 点击 "部署"

### 方案 3: 优化启动流程（已实现）

代码已优化，包含：
1. **健康检查服务器**：立即启动，让 Cloud Run 知道容器已就绪
2. **后台加载**：Gradio 在后台加载，不阻塞健康检查
3. **快速响应**：健康检查端点立即响应，满足 Cloud Run 的启动检测

### 方案 4: 增加资源分配

如果启动仍然慢，可以增加资源：

```powershell
gcloud run deploy deepseek-chat-agent `
    --memory 4Gi `
    --cpu 4 `
    --startup-timeout 600 `
    --timeout 600
```

## 验证部署

### 1. 检查日志

在 Cloud Run Console 中：
1. 进入服务页面
2. 点击 "日志" 标签
3. 查看启动日志，确认：
   - ✓ Health check server started
   - ✓ Gradio demo created
   - ✓ Gradio server started

### 2. 测试健康检查

```powershell
# 获取服务 URL
$SERVICE_URL = (gcloud run services describe deepseek-chat-agent `
    --region us-central1 `
    --format 'value(status.url)')

# 测试健康检查
curl "$SERVICE_URL/health"
```

### 3. 检查端口监听

在容器日志中应该看到：
```
✓ Health check server started on port 8080
```

## 常见问题

### Q1: 为什么需要健康检查服务器？

**A:** Cloud Run 需要在容器启动后立即检测到端口监听。Gradio 启动需要时间（加载依赖、初始化等），健康检查服务器可以立即响应，满足 Cloud Run 的启动检测要求。

### Q2: 启动超时应该设置多长？

**A:** 
- **最小**: 60 秒（简单应用）
- **推荐**: 300 秒（5 分钟，适合 Gradio 应用）
- **最大**: 900 秒（15 分钟，Cloud Run 限制）

### Q3: 如何知道启动是否成功？

**A:** 检查日志中的关键信息：
- `✓ Health check server started` - 健康检查服务器启动
- `✓ Gradio demo created` - Gradio 界面创建成功
- `Running on local URL: http://127.0.0.1:8080` - Gradio 服务器启动成功

### Q4: 仍然超时怎么办？

**A:** 尝试以下步骤：
1. 增加 `--startup-timeout` 到 600 秒
2. 增加内存和 CPU（`--memory 4Gi --cpu 4`）
3. 检查日志中的错误信息
4. 确认所有依赖都已正确安装
5. 检查网络连接（如果需要下载模型或依赖）

## 部署命令模板

### 完整部署命令

```powershell
# 设置变量
$AR = "us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel"
$SN = "deepseek-chat-agent"
$TAG = "v1.0.0"
$PROJECT = "firbase-app1-17308"
$REGION = "us-central1"
$API_KEY = "your_api_key_here"

# 部署
gcloud run deploy $SN `
    --image "$AR/$SN:$TAG" `
    --platform managed `
    --region $REGION `
    --project $PROJECT `
    --allow-unauthenticated `
    --set-env-vars "DEEPSEEK_API_KEY=$API_KEY,DEEPSEEK_API_BASE=https://api.deepseek.com/v1" `
    --memory 2Gi `
    --cpu 2 `
    --timeout 300 `
    --startup-timeout 300 `
    --max-instances 10 `
    --min-instances 0 `
    --cpu-boost `
    --port 8080
```

## 参考

- [Cloud Run 启动超时文档](https://cloud.google.com/run/docs/configuring/startup-timeout)
- [Cloud Run 故障排除](https://cloud.google.com/run/docs/troubleshooting)
- [容器启动最佳实践](https://cloud.google.com/run/docs/tips/general)

