# 环境变量配置说明

## GitHub Actions 工作流配置

### ✅ 已配置的环境变量

在 `.github/workflows/deploy-cloud-run.yml` 文件的第 **604 行**，GitHub Actions 确实设置了 `DEEPSEEK_API_KEY`：

```yaml
--set-env-vars DEEPSEEK_API_KEY=${{ secrets.DEEPSEEK_API_KEY }},DEEPSEEK_API_BASE=${{ env.DEEPSEEK_API_BASE }} \
```

**完整部署命令**（第 598-611 行）：
```yaml
DEPLOY_CMD="gcloud run deploy ${{ env.SERVICE_NAME }} \
  --image \"$IMAGE_URL\" \
  --platform managed \
  --region ${{ env.REGION }} \
  --project ${{ env.PROJECT_ID }} \
  --allow-unauthenticated \
  --set-env-vars DEEPSEEK_API_KEY=${{ secrets.DEEPSEEK_API_KEY }},DEEPSEEK_API_BASE=${{ env.DEEPSEEK_API_BASE }} \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --min-instances 0 \
  --cpu-boost \
  --port 8080"
```

### 环境变量说明

1. **`DEEPSEEK_API_KEY`**
   - 来源：`${{ secrets.DEEPSEEK_API_KEY }}`
   - 说明：需要在 GitHub Secrets 中配置
   - 用途：DeepSeek API 认证密钥

2. **`DEEPSEEK_API_BASE`**
   - 来源：`${{ env.DEEPSEEK_API_BASE }}`
   - 默认值：`https://api.deepseek.com/v1`（如果未设置）
   - 说明：可以在 GitHub Secrets 中配置，或使用默认值
   - 用途：DeepSeek API 基础 URL

---

## 手动部署时的环境变量配置

### 在 Google Cloud Console 中配置

当你在 Google Cloud Console 中手动部署时：

1. **进入 Cloud Run 服务页面**
2. **点击"编辑和部署新版本"**
3. **展开"容器、变量、密钥、连接"**
4. **在"变量和参数"部分添加**：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `DEEPSEEK_API_KEY` | `your_api_key_here` | DeepSeek API 密钥 |
| `DEEPSEEK_API_BASE` | `https://api.deepseek.com/v1` | DeepSeek API 基础 URL（可选） |

### 使用 gcloud CLI 配置

```powershell
# 部署时设置环境变量
gcloud run deploy deepseek-chat-agent `
    --image us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:latest `
    --platform managed `
    --region us-central1 `
    --project firbase-app1-17308 `
    --allow-unauthenticated `
    --set-env-vars "DEEPSEEK_API_KEY=your_api_key_here,DEEPSEEK_API_BASE=https://api.deepseek.com/v1" `
    --memory 2Gi `
    --cpu 2 `
    --timeout 300 `
    --max-instances 10 `
    --min-instances 0 `
    --cpu-boost `
    --port 8080
```

---

## 验证环境变量是否设置

### 方法 1: 在 Cloud Run Console 中查看

1. 进入 Cloud Run 服务页面
2. 点击服务名称
3. 在"修订版本"标签中，点击最新的修订版本
4. 查看"环境变量"部分，确认 `DEEPSEEK_API_KEY` 已设置

### 方法 2: 使用 gcloud CLI 查看

```powershell
# 查看服务配置
gcloud run services describe deepseek-chat-agent `
    --region us-central1 `
    --project firbase-app1-17308 `
    --format="value(spec.template.spec.containers[0].env)"
```

### 方法 3: 查看容器日志

```powershell
# 查看最近的日志
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=deepseek-chat-agent" `
    --limit 50 `
    --project firbase-app1-17308 `
    --format="table(timestamp,textPayload)" `
    | Select-String -Pattern "DEEPSEEK_API_KEY|API Key"
```

**新版本应该看到**：
- `✓ DEEPSEEK_API_KEY is set`
- `✓ DEEPSEEK_API_BASE: https://api.deepseek.com/v1`

**如果看到错误**：
- `DEEPSEEK_API_KEY environment variable is not set` - 说明环境变量未设置

---

## 关于 URL 和端口的说明

### ✅ 正确的访问方式

**Cloud Run 服务 URL**（不需要端口号）：
```
https://deepseek-chat-agent-205204734416.us-central1.run.app
```

**说明**：
- Cloud Run 自动处理端口映射
- 不需要在 URL 中指定 `:8080`
- 直接访问根路径 `/` 即可看到 Gradio UI

### ❌ 错误的访问方式

```
https://deepseek-chat-agent-205204734416.us-central1.run.app:8080
```

**说明**：
- Cloud Run 使用 HTTPS（443 端口）
- 容器内部监听 8080 端口
- Cloud Run 自动将外部 HTTPS 请求转发到容器内部的 8080 端口

---

## 问题排查

### 问题 1: 仍然返回 JSON 而不是 Gradio UI

**可能原因**：
1. 部署的镜像仍然是旧版本（包含健康检查服务器）
2. Gradio 启动失败
3. 环境变量未正确设置

**解决方法**：
1. 确认使用最新镜像（包含修复后的 `start_server.py`）
2. 查看 Cloud Run 日志，确认 Gradio 是否启动
3. 确认环境变量已设置

### 问题 2: 环境变量未设置

**症状**：
- 日志显示：`DEEPSEEK_API_KEY environment variable is not set`
- 容器启动失败

**解决方法**：
1. 在 Cloud Run Console 中检查环境变量
2. 重新部署并设置环境变量
3. 使用 `--set-env-vars` 参数设置

### 问题 3: Gradio 启动失败

**症状**：
- 日志显示 Gradio 相关错误
- 访问 URL 返回错误页面

**解决方法**：
1. 查看完整日志，定位错误原因
2. 检查依赖是否正确安装
3. 确认内存和 CPU 资源足够（建议 2Gi 内存，2 CPU）

---

## 完整部署检查清单

### 代码检查
- [ ] `app/start_server.py` 已修复（移除健康检查服务器）
- [ ] `Dockerfile` 使用 `CMD ["python", "-m", "app.start_server"]`
- [ ] 代码已提交并推送到 GitHub

### 镜像检查
- [ ] 使用 `--no-cache` 构建镜像，确保使用最新代码
- [ ] 镜像已推送到 Artifact Registry
- [ ] 镜像标签正确

### 环境变量检查
- [ ] `DEEPSEEK_API_KEY` 已设置（在 Cloud Run Console 或通过 CLI）
- [ ] `DEEPSEEK_API_BASE` 已设置（可选，默认使用官方 API）
- [ ] 环境变量值正确（无多余空格或引号）

### 部署检查
- [ ] 使用正确的镜像 URL
- [ ] 端口设置为 8080
- [ ] 内存和 CPU 资源足够（2Gi 内存，2 CPU）
- [ ] 服务已部署成功

### 验证检查
- [ ] 访问服务 URL（不需要 `:8080`）
- [ ] 看到 Gradio 聊天界面（不是 JSON）
- [ ] 可以输入问题并收到回复

---

## 总结

### GitHub Actions 配置

✅ **已正确配置**：
- `DEEPSEEK_API_KEY` 从 `secrets.DEEPSEEK_API_KEY` 读取
- `DEEPSEEK_API_BASE` 从环境变量读取（默认 `https://api.deepseek.com/v1`）

### 手动部署配置

✅ **需要手动设置**：
- 在 Cloud Run Console 的"变量和参数"中添加 `DEEPSEEK_API_KEY`
- 可选：添加 `DEEPSEEK_API_BASE`（如果不使用默认值）

### URL 访问

✅ **正确方式**：
- 直接访问 Cloud Run 服务 URL（不需要 `:8080`）
- 访问根路径 `/` 即可看到 Gradio UI

---

## 下一步

1. **确认环境变量已设置**：
   - 在 Cloud Run Console 中检查
   - 或使用 gcloud CLI 查看

2. **查看日志确认 Gradio 启动**：
   ```powershell
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=deepseek-chat-agent" `
       --limit 50 `
       --project firbase-app1-17308
   ```

3. **如果仍然返回 JSON**：
   - 确认部署的镜像是最新版本
   - 重新构建并部署（使用 `--no-cache`）

