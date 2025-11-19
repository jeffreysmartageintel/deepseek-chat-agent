# 快速部署指南

## 当前状态

✅ **代码已提交**  
✅ **Artifact Registry 已清空**  
✅ **代码已修复**（移除健康检查服务器，直接启动 Gradio）

## 部署方式

### 方式 1: 使用 GitHub Actions（推荐，自动化）

#### 步骤 1: 确认代码已推送到 GitHub

```powershell
# 检查是否已推送
git status

# 如果显示 "Your branch is ahead of 'origin/main'"，需要推送
git push
```

#### 步骤 2: 触发 GitHub Actions

**方法 A: 手动触发（推荐）**

1. 打开 GitHub 仓库：`https://github.com/jeffreysmartageintel/deepseek-chat-agent`
2. 点击 **"Actions"** 标签
3. 在左侧选择 **"DeepSeek Chat Agent - Build & Deploy to Google Cloud Run"**
4. 点击右上角 **"Run workflow"** 按钮
5. 选择分支（通常是 `main`）
6. 点击 **"Run workflow"** 按钮

**方法 B: 等待自动触发**

- 每天 UTC 11:30（北京时间 19:30）自动检查并构建

#### 步骤 3: 等待构建完成

- 构建时间：约 5-10 分钟
- 可以在 GitHub Actions 页面查看实时日志

#### 步骤 4: 批准部署

1. 构建完成后，找到 **"部署到 Google Cloud Run（需要批准）"** job
2. 点击 **"Review deployments"** 按钮
3. 点击 **"Approve and deploy"** 按钮批准部署

#### 步骤 5: 验证部署

部署完成后（约 2-5 分钟），访问服务 URL：
```
https://deepseek-chat-agent-205204734416.us-central1.run.app
```

**应该看到**：
- ✅ Gradio 聊天界面（HTML 页面）
- ✅ 可以输入问题并开始对话
- ❌ 不再是 JSON 响应

---

### 方式 2: 手动部署（快速验证）

如果需要立即部署，可以手动执行：

#### 步骤 1: 配置环境变量

```powershell
# 设置变量
$AR = "us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel"
$SN = "deepseek-chat-agent"
$TAG = "v1.0.3"
$PROJECT = "firbase-app1-17308"
$REGION = "us-central1"
```

#### 步骤 2: 认证 Google Cloud

```powershell
# 使用服务账号密钥文件认证
gcloud auth activate-service-account --key-file=./firbase-app1-17308-55a0269a02c7.json

# 配置 Docker 认证（Artifact Registry）
gcloud auth configure-docker us-central1-docker.pkg.dev
```

#### 步骤 3: 构建并推送镜像

```powershell
# 构建镜像（使用 --no-cache 确保使用最新代码）
docker build --no-cache -t deepseek-chat-agent:local .

# 标记镜像
docker tag deepseek-chat-agent:local "$AR/$SN:$TAG"
docker tag deepseek-chat-agent:local "$AR/$SN:latest"

# 推送镜像
docker push "$AR/$SN:$TAG"
docker push "$AR/$SN:latest"
```

#### 步骤 4: 部署到 Cloud Run

```powershell
# 部署到 Cloud Run
gcloud run deploy $SN `
    --image "$AR/$SN:$TAG" `
    --platform managed `
    --region $REGION `
    --project $PROJECT `
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

**注意**：将 `your_key` 替换为实际的 `DEEPSEEK_API_KEY`。

#### 步骤 5: 验证部署

```powershell
# 获取服务 URL
gcloud run services describe $SN `
    --platform managed `
    --region $REGION `
    --project $PROJECT `
    --format="value(status.url)"
```

访问返回的 URL，应该看到 Gradio 聊天界面。

---

## 部署时间估算

- **GitHub Actions 方式**：约 15-20 分钟
  - 构建镜像：5-10 分钟
  - 推送镜像：1-2 分钟
  - 部署到 Cloud Run：2-5 分钟
  - 等待批准：取决于审批人响应时间

- **手动部署方式**：约 10-15 分钟
  - 构建镜像：5-10 分钟
  - 推送镜像：1-2 分钟
  - 部署到 Cloud Run：2-5 分钟

---

## 验证清单

部署完成后，确认：

- [ ] 访问服务 URL 看到 Gradio 聊天界面（不是 JSON）
- [ ] 可以输入问题
- [ ] 可以收到 AI 回复
- [ ] 聊天历史正常显示
- [ ] 温度滑块可以调整

---

## 如果遇到问题

### 问题 1: 仍然返回 JSON

**原因**：部署的镜像仍然是旧版本

**解决**：
1. 确认代码已提交并推送
2. 使用 `--no-cache` 重新构建
3. 查看 Cloud Run 日志确认 Gradio 是否启动

### 问题 2: 部署失败

**解决**：
1. 查看 GitHub Actions 日志（如果使用 GitHub Actions）
2. 查看 Cloud Run 日志
3. 确认环境变量已正确设置

### 问题 3: 如何查看日志？

```powershell
# 查看 Cloud Run 日志
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=deepseek-chat-agent" `
    --limit 50 `
    --project firbase-app1-17308 `
    --format json
```

---

## 下一步

部署成功后：
1. 测试聊天功能
2. 根据需要调整资源配置
3. 查看 Cloud Run 监控指标

如果需要帮助，请查看：
- `FRESH_DEPLOYMENT_GUIDE.md` - 详细部署指南
- `DEPLOYMENT_VERIFICATION.md` - 部署验证指南
- `CLOUD_RUN_TROUBLESHOOTING.md` - 故障排除指南

