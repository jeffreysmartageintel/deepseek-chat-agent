# Google Cloud Run 部署指南（Gradio 应用）

## 📋 部署说明

本项目已配置为将 Gradio Web UI 应用部署到 Google Cloud Run。

## 🔧 主要修改

### 1. Dockerfile 修改

**主要变更：**
- 启动命令从 `uvicorn app.main:app` 改为 `python -m app.gradio_app`
- 添加了 `PORT` 环境变量（默认 8080）
- 保持端口 8080（Cloud Run 要求）

### 2. gradio_app.py 修改

**主要变更：**
- 支持从环境变量 `PORT` 读取端口（Cloud Run 会自动设置）
- 默认端口改为 8080（符合 Cloud Run 要求）
- 禁用了 `show_api`（在 Cloud Run 上不需要）

### 3. GitHub Actions 工作流修改

**主要变更：**
- 更新了部署配置，增加内存和 CPU 资源（Gradio 需要更多资源）
- 添加了 `DEEPSEEK_API_BASE` 环境变量
- 更新了通知消息，指向 Gradio UI 而不是 API 文档

## 📊 资源配置

### 当前配置

- **内存**: 1Gi（从 512Mi 增加）
- **CPU**: 2（从 1 增加）
- **超时**: 300 秒
- **最大实例**: 10
- **最小实例**: 0（按需启动）

### 为什么需要更多资源？

Gradio 应用相比 FastAPI 需要更多资源：
- Gradio 需要运行 WebSocket 服务器
- 需要处理实时 UI 更新
- 需要更多内存来缓存对话历史

## 🚀 部署流程

### 自动部署

1. **定时触发**：每天北京时间 19:30 自动检查是否有代码 push
2. **手动触发**：可以在 GitHub Actions 中手动触发
3. **构建镜像**：自动构建 Docker 镜像
4. **等待批准**：需要审批者批准部署（如果配置了 Environment）
5. **部署到 Cloud Run**：批准后自动部署

### 手动部署

如果需要手动部署：

```bash
# 1. 构建镜像
docker build -t gcr.io/YOUR_PROJECT_ID/deepseek-chat-agent:latest .

# 2. 推送到 GCR
docker push gcr.io/YOUR_PROJECT_ID/deepseek-chat-agent:latest

# 3. 部署到 Cloud Run
gcloud run deploy deepseek-chat-agent \
  --image gcr.io/YOUR_PROJECT_ID/deepseek-chat-agent:latest \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --set-env-vars DEEPSEEK_API_KEY=your_key_here,DEEPSEEK_API_BASE=https://api.deepseek.com/v1 \
  --memory 1Gi \
  --cpu 2 \
  --timeout 300
```

## 🔐 环境变量配置

### 必需的 Secrets

在 GitHub Secrets 中配置：

- `GCP_PROJECT_ID`: Google Cloud 项目 ID
- `GCP_SA_KEY`: Google Cloud 服务账号密钥（JSON）
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥
- `LARK_WEBHOOK_URL`: Lark Webhook URL（用于通知）

### 环境变量

部署时会自动设置：

- `DEEPSEEK_API_KEY`: 从 Secrets 读取
- `DEEPSEEK_API_BASE`: `https://api.deepseek.com/v1`
- `PORT`: Cloud Run 自动设置（通常是 8080）

## 🌐 访问应用

部署成功后，可以通过以下方式访问：

1. **服务 URL**: Cloud Run 会自动分配一个公共 URL
   - 格式：`https://deepseek-chat-agent-xxxxx-xx.a.run.app`
   - 在部署通知中会显示完整 URL

2. **直接访问**: 打开浏览器访问服务 URL 即可使用 Gradio UI

## 📝 注意事项

### 1. 端口配置

- Cloud Run 要求应用监听 `$PORT` 环境变量指定的端口
- 代码已自动从环境变量读取端口
- 默认端口为 8080

### 2. 资源限制

- 如果遇到内存不足，可以增加 `--memory` 参数
- 如果响应慢，可以增加 `--cpu` 参数
- 注意成本：更多资源 = 更高成本

### 3. 超时设置

- 当前超时设置为 300 秒（5 分钟）
- 如果对话很长，可能需要增加超时时间
- 可以在部署命令中修改 `--timeout` 参数

### 4. 冷启动

- 最小实例设置为 0，意味着没有请求时会关闭实例
- 首次请求会有冷启动延迟（通常几秒）
- 如果需要更快响应，可以设置 `--min-instances 1`

## 🔍 故障排除

### 问题 1：应用无法启动

**检查：**
- 查看 Cloud Run 日志
- 确认环境变量正确设置
- 检查 API Key 是否有效

### 问题 2：内存不足

**解决：**
- 增加 `--memory` 参数（例如：`--memory 2Gi`）

### 问题 3：响应超时

**解决：**
- 增加 `--timeout` 参数（例如：`--timeout 600`）
- 检查网络连接

### 问题 4：端口错误

**检查：**
- 确认代码从 `PORT` 环境变量读取端口
- 确认 Dockerfile 暴露了正确的端口

## 📚 相关文档

- [Google Cloud Run 文档](https://cloud.google.com/run/docs)
- [Gradio 部署文档](https://gradio.app/guides/sharing-your-app)
- [Docker 文档](https://docs.docker.com/)

## ✅ 验证部署

部署成功后，可以通过以下方式验证：

1. **访问服务 URL**: 应该能看到 Gradio UI 界面
2. **测试对话**: 输入一个问题，应该能获得回复
3. **查看日志**: 在 Cloud Run 控制台查看应用日志

---

**部署完成后，你的 Gradio Web UI 就可以通过 Cloud Run 的公共 URL 访问了！** 🎉

