# Cloud Run 访问指南

## 问题分析

### 当前状态

根据你提供的信息：
- ✅ 容器已启动
- ✅ 健康检查端点 `/` 正常返回：`{"status":"ok","service":"deepseek-chat-agent"}`
- ❌ 无法访问 Gradio 聊天界面

### 可能的原因

1. **健康检查服务器仍在运行**：健康检查服务器可能没有正确停止，Gradio 没有接管端口
2. **Gradio 启动失败**：Gradio 可能在启动过程中出错
3. **端口冲突**：健康检查服务器和 Gradio 可能发生端口冲突

## 解决方案

### 方案 1: 检查 Cloud Run 日志（推荐）

1. **进入 Cloud Run Console**：
   - 访问：https://console.cloud.google.com/run
   - 选择服务：`deepseek-chat-agent`
   - 点击 "日志" 标签

2. **查看关键日志**：
   查找以下信息：
   ```
   ✓ Gradio demo created
   Launching Gradio server on 0.0.0.0:8080
   Running on local URL: http://127.0.0.1:8080
   ```

3. **如果看到错误**：
   - 复制错误信息
   - 根据错误信息进行修复

### 方案 2: 使用 gcloud 命令查看日志

```powershell
# 查看最近的日志
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=deepseek-chat-agent" `
    --limit 50 `
    --format json `
    --project firbase-app1-17308

# 或查看实时日志
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=deepseek-chat-agent" `
    --project firbase-app1-17308
```

### 方案 3: 重新部署（已优化代码）

代码已优化，移除了健康检查服务器，直接启动 Gradio。重新构建和部署：

```powershell
# 1. 构建新镜像
docker build -t deepseek-chat-agent:local .

# 2. 标记镜像
docker tag deepseek-chat-agent:local us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:v1.0.2

# 3. 推送镜像
docker push us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:v1.0.2

# 4. 部署到 Cloud Run
gcloud run deploy deepseek-chat-agent `
    --image us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:v1.0.2 `
    --platform managed `
    --region us-central1 `
    --project firbase-app1-17308 `
    --allow-unauthenticated `
    --set-env-vars "DEEPSEEK_API_KEY=your_key,DEEPSEEK_API_BASE=https://api.deepseek.com/v1" `
    --memory 2Gi `
    --cpu 2 `
    --timeout 300 `
    --startup-timeout 300 `
    --port 8080
```

## 正确的访问方式

### ❌ 错误的访问方式

```
https://deepseek-chat-agent-205204734416.us-central1.run.app/8080  # 错误：不需要端口号
```

### ✅ 正确的访问方式

```
https://deepseek-chat-agent-205204734416.us-central1.run.app/     # 根路径
```

**注意**：Cloud Run 的 URL 不需要端口号，因为 Cloud Run 自动处理端口映射。

## 验证步骤

### 1. 检查服务状态

```powershell
gcloud run services describe deepseek-chat-agent `
    --region us-central1 `
    --project firbase-app1-17308 `
    --format="value(status.url)"
```

### 2. 测试访问

```powershell
# 获取服务 URL
$SERVICE_URL = (gcloud run services describe deepseek-chat-agent `
    --region us-central1 `
    --format 'value(status.url)')

# 测试访问
curl $SERVICE_URL
```

### 3. 查看响应

- **如果返回 HTML**：说明 Gradio 已启动 ✅
- **如果返回 JSON**：说明健康检查服务器仍在运行 ❌

## 常见问题

### Q1: 为什么访问 `/` 返回 JSON 而不是 Gradio 界面？

**A:** 健康检查服务器仍在运行，Gradio 没有成功启动或接管端口。

**解决**：
1. 查看日志确认 Gradio 是否启动
2. 重新部署优化后的代码（已移除健康检查服务器）

### Q2: 如何确认 Gradio 是否启动？

**A:** 查看 Cloud Run 日志，查找：
- `✓ Gradio demo created`
- `Running on local URL: http://127.0.0.1:8080`

### Q3: 访问时显示 "加载中" 怎么办？

**A:** 
1. 等待几秒钟（Gradio 可能需要时间加载）
2. 检查浏览器控制台（F12）的错误信息
3. 查看 Cloud Run 日志

### Q4: 如何强制重新部署？

**A:** 

```powershell
# 使用新的镜像标签强制部署
gcloud run deploy deepseek-chat-agent `
    --image us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:v1.0.2 `
    --platform managed `
    --region us-central1 `
    --project firbase-app1-17308 `
    --allow-unauthenticated `
    --set-env-vars "DEEPSEEK_API_KEY=your_key" `
    --memory 2Gi `
    --cpu 2 `
    --timeout 300 `
    --startup-timeout 300 `
    --port 8080 `
    --no-traffic  # 部署但不接收流量（用于测试）
```

## 下一步

1. **查看日志**：确认 Gradio 是否启动
2. **重新部署**：使用优化后的代码（已移除健康检查服务器）
3. **测试访问**：访问服务 URL，应该看到 Gradio 界面

## 参考

- [Cloud Run 日志查看](https://console.cloud.google.com/run)
- [Cloud Run 故障排除](https://cloud.google.com/run/docs/troubleshooting)

