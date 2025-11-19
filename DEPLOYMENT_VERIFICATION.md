# 部署验证指南

## 问题诊断

如果访问 Cloud Run 服务 URL 仍然返回 JSON：
```json
{"status":"ok","service":"deepseek-chat-agent"}
```

这说明部署的镜像仍然是**旧版本**（包含健康检查服务器）。

## 解决方案

### 步骤 1: 确认代码已更新

检查 `app/start_server.py` 文件，确认：
- ✅ 没有 `HealthCheckHandler` 类
- ✅ 没有 `start_health_check_server` 函数
- ✅ 直接启动 Gradio，没有健康检查服务器

### 步骤 2: 提交代码到 GitHub

```powershell
# 检查更改
git status

# 添加所有更改
git add .

# 提交更改
git commit -m "Remove health check server, launch Gradio directly"

# 推送到 GitHub
git push
```

### 步骤 3: 触发 GitHub Actions

**方法 A: 等待自动触发**
- 每天 UTC 11:30（北京时间 19:30）自动检查

**方法 B: 手动触发**
1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择 "DeepSeek Chat Agent - Build & Deploy to Google Cloud Run"
4. 点击 "Run workflow"
5. 勾选 "强制构建（跳过 push 检查）"
6. 点击 "Run workflow"

### 步骤 4: 验证部署

部署完成后：

1. **查看 GitHub Actions 日志**：
   - 确认构建成功
   - 确认部署成功
   - 查看服务 URL

2. **访问服务 URL**：
   ```
   https://deepseek-chat-agent-205204734416.us-central1.run.app
   ```
   
   应该看到：
   - ✅ Gradio 聊天界面（HTML 页面）
   - ❌ 不再是 JSON 响应

3. **如果仍然返回 JSON**：
   - 检查 Cloud Run 日志，确认 Gradio 是否启动
   - 确认部署的镜像标签是否正确
   - 可能需要手动重新部署

## 手动重新部署（如果 GitHub Actions 失败）

如果 GitHub Actions 部署失败，可以手动部署：

```powershell
# 1. 构建新镜像
docker build --no-cache -t deepseek-chat-agent:local .

# 2. 标记镜像
docker tag deepseek-chat-agent:local us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:v1.0.3

# 3. 推送镜像
docker push us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:v1.0.3

# 4. 部署到 Cloud Run
gcloud run deploy deepseek-chat-agent `
    --image us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:v1.0.3 `
    --platform managed `
    --region us-central1 `
    --project firbase-app1-17308 `
    --allow-unauthenticated `
    --set-env-vars "DEEPSEEK_API_KEY=your_key,DEEPSEEK_API_BASE=https://api.deepseek.com/v1" `
    --memory 2Gi `
    --cpu 2 `
    --timeout 300 `
    --max-instances 10 `
    --min-instances 0 `
    --cpu-boost `
    --port 8080
```

## 检查 Cloud Run 日志

```powershell
# 查看最近的日志
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=deepseek-chat-agent" `
    --limit 100 `
    --project firbase-app1-17308 `
    --format json | ConvertFrom-Json | Select-Object -First 20

# 或查看实时日志
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=deepseek-chat-agent" `
    --project firbase-app1-17308
```

**关键日志信息**：
- `✓ Gradio module imported successfully`
- `✓ Gradio demo created successfully`
- `Running on local URL: http://127.0.0.1:8080`

## 常见问题

### Q1: 为什么仍然返回 JSON？

**A:** 部署的镜像仍然是旧版本。需要：
1. 确认代码已提交到 GitHub
2. 触发新的 GitHub Actions 运行
3. 或手动重新构建和部署

### Q2: 如何确认部署的是新版本？

**A:** 
1. 查看 Cloud Run 日志，确认没有 "Health check server" 相关日志
2. 查看镜像标签，确认是最新的 commit SHA
3. 访问服务 URL，应该看到 Gradio 界面

### Q3: Gradio 启动需要多长时间？

**A:** 
- 通常 10-30 秒
- 如果启动时间过长，可能需要增加内存和 CPU
- 查看日志确认是否有错误

## 验证清单

- [ ] 代码已提交到 GitHub
- [ ] GitHub Actions 构建成功
- [ ] GitHub Actions 部署成功
- [ ] 访问服务 URL 看到 Gradio 界面（不是 JSON）
- [ ] 可以正常输入问题并收到回复

## 下一步

部署成功后，访问服务 URL 应该：
1. 看到 Gradio 聊天界面
2. 可以输入问题
3. 收到 AI 回复

如果仍然有问题，请查看 Cloud Run 日志获取详细错误信息。

