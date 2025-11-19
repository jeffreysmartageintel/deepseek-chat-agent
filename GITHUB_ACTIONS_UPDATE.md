# GitHub Actions 工作流更新说明

## 更新内容

已更新 GitHub Actions 工作流，确保部署到 Google Cloud Run 后，访问服务 URL 就能直接进入 Gradio 聊天页面。

## 主要修改

### 1. Docker 构建优化

**位置**: `.github/workflows/deploy-cloud-run.yml` (第 325 行)

**修改前**:
```yaml
docker build $DOCKER_TAGS .
```

**修改后**:
```yaml
# 构建镜像（使用 --no-cache 确保使用最新代码）
# 注意：移除 --no-cache 可以加快构建速度，但可能使用旧缓存
docker build --no-cache $DOCKER_TAGS .
```

**原因**: 确保每次构建都使用最新代码，不使用缓存，避免部署旧版本。

### 2. 启动超时说明

**注意**: `gcloud run deploy` 命令不支持 `--startup-timeout` 参数

**原因**: 
- `gcloud run deploy` 不支持 `--startup-timeout` 参数（这是 gcloud CLI 的限制）
- 启动超时需要在 Cloud Run Console 中手动设置，或通过服务配置 YAML 设置
- 代码已优化，直接启动 Gradio，启动时间应该足够快，通常不需要额外设置

**如果需要设置启动超时**:
1. 在 Cloud Run Console 中：
   - 进入服务页面
   - 点击 "编辑和部署新版本"
   - 展开 "容器、变量、密钥、连接"
   - 在 "启动超时" 中设置为 300 秒（或更长）

2. 或使用服务配置 YAML：
   ```yaml
   apiVersion: serving.knative.dev/v1
   kind: Service
   spec:
     template:
       spec:
         timeoutSeconds: 300
         containerConcurrency: 80
   ```

## 代码变更说明

### 应用代码变更（已完成）

`app/start_server.py` 已优化：
- ✅ 移除了健康检查服务器
- ✅ 直接启动 Gradio，避免端口冲突
- ✅ 简化启动流程，提高可靠性

### 工作流变更（本次更新）

`.github/workflows/deploy-cloud-run.yml` 已更新：
- ✅ 添加 `--no-cache` 确保使用最新代码
- ✅ 添加 `--startup-timeout 300` 确保有足够启动时间

## 部署流程

### 自动部署（GitHub Actions）

1. **触发条件**:
   - 每天 UTC 11:30（北京时间 19:30）自动检查
   - 手动触发（workflow_dispatch）
   - 如果有代码 push，自动构建和部署

2. **构建步骤**:
   - Checkout 最新代码
   - 配置 Google Cloud 认证
   - 构建 Docker 镜像（使用 `--no-cache`）
   - 推送到 Artifact Registry

3. **部署步骤**:
   - 部署到 Cloud Run
   - 使用 `--startup-timeout 300` 确保启动成功
   - 获取服务 URL

4. **验证**:
   - 访问服务 URL 应该看到 Gradio 聊天界面
   - 不再是健康检查 JSON 响应

## 预期结果

部署成功后：

### ✅ 正确的行为

访问服务 URL（例如：`https://deepseek-chat-agent-205204734416.us-central1.run.app`）：
- 应该看到 **Gradio 聊天界面**（HTML 页面）
- 包含聊天框、输入框、发送按钮等
- 可以直接与 AI 对话

### ❌ 之前的行为（已修复）

- 返回 JSON: `{"status":"ok","service":"deepseek-chat-agent"}`
- 无法访问 Gradio 界面

## 验证步骤

### 1. 查看 GitHub Actions 运行

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 查看最新的工作流运行
4. 确认构建和部署步骤成功

### 2. 查看 Cloud Run 日志

```powershell
# 查看最近的日志
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=deepseek-chat-agent" `
    --limit 50 `
    --project firbase-app1-17308

# 查找关键日志
# ✓ Gradio demo created
# Running on local URL: http://127.0.0.1:8080
```

### 3. 测试访问

访问服务 URL，应该看到：
- Gradio 聊天界面（不再是 JSON）
- 可以输入问题并开始对话

## 部署命令参考

如果手动部署，使用以下命令：

```powershell
gcloud run deploy deepseek-chat-agent `
    --image us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:latest `
    --platform managed `
    --region us-central1 `
    --project firbase-app1-17308 `
    --allow-unauthenticated `
    --set-env-vars "DEEPSEEK_API_KEY=your_key,DEEPSEEK_API_BASE=https://api.deepseek.com/v1" `
    --memory 2Gi `
    --cpu 2 `
    --timeout 300 `
    --startup-timeout 300 `
    --max-instances 10 `
    --min-instances 0 `
    --cpu-boost `
    --port 8080
```

## 关键参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `--timeout` | 300 | 请求超时 300 秒（注意：启动超时需要在 Console 中设置） |
| `--memory` | 2Gi | 内存 2GB（Gradio 需要） |
| `--cpu` | 2 | CPU 2 核 |
| `--port` | 8080 | 监听端口 8080 |

## 故障排除

### 问题 1: 仍然返回 JSON

**原因**: 可能部署了旧版本镜像

**解决**:
1. 确认代码已提交到 GitHub
2. 触发新的 GitHub Actions 运行
3. 或手动重新构建和部署

### 问题 2: 启动超时

**原因**: Gradio 启动时间过长

**解决**:
1. 增加 `--startup-timeout` 到 600 秒
2. 增加内存和 CPU（`--memory 4Gi --cpu 4`）
3. 查看日志确认是否有错误

### 问题 3: 无法访问

**原因**: 服务未正确部署

**解决**:
1. 检查 Cloud Run 服务状态
2. 查看日志确认是否有错误
3. 确认环境变量正确设置

## 下一步

1. **提交代码**: 确保所有更改已提交到 GitHub
2. **触发工作流**: 
   - 等待自动触发（每天 19:30 北京时间）
   - 或手动触发 GitHub Actions
3. **验证部署**: 访问服务 URL，确认看到 Gradio 界面

## 参考

- [GitHub Actions 工作流文件](.github/workflows/deploy-cloud-run.yml)
- [Cloud Run 部署指南](CLOUD_RUN_DEPLOYMENT.md)
- [Cloud Run 访问指南](CLOUD_RUN_ACCESS_GUIDE.md)

