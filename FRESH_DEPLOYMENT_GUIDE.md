# 全新部署指南（Artifact Registry 已清空）

## 当前状态

✅ **Artifact Registry 镜像已清空**  
✅ **代码已修复**（移除健康检查服务器，直接启动 Gradio）  
✅ **GitHub Actions 工作流已配置**

## 部署方式

### 方式 1: 使用 GitHub Actions（推荐）

#### 步骤 1: 确认代码已提交

```powershell
# 检查当前状态
git status

# 如果有未提交的更改，提交它们
git add .
git commit -m "Remove health check server, launch Gradio directly"
git push
```

#### 步骤 2: 触发 GitHub Actions

**方法 A: 手动触发（推荐）**

1. 打开 GitHub 仓库页面
2. 点击 **"Actions"** 标签
3. 选择 **"DeepSeek Chat Agent - Build & Deploy to Google Cloud Run"** 工作流
4. 点击 **"Run workflow"** 按钮
5. 选择分支（通常是 `main`）
6. 勾选 **"强制构建（跳过 push 检查）"**（如果需要）
7. 点击 **"Run workflow"** 按钮

**方法 B: 等待自动触发**

- 每天 UTC 11:30（北京时间 19:30）自动检查并构建

#### 步骤 3: 批准部署

1. 等待构建完成（约 5-10 分钟）
2. 在 GitHub Actions 页面找到 **"部署到 Google Cloud Run（需要批准）"** job
3. 点击 **"Review deployments"** 按钮
4. 点击 **"Approve and deploy"** 按钮批准部署

#### 步骤 4: 验证部署

部署完成后，访问服务 URL：
```
https://deepseek-chat-agent-205204734416.us-central1.run.app
```

应该看到：
- ✅ Gradio 聊天界面（HTML 页面）
- ✅ 可以输入问题并开始对话
- ❌ 不再是 JSON 响应

---

### 方式 2: 手动部署（快速验证）

如果需要快速验证，可以手动构建和部署：

#### 步骤 1: 配置环境变量

```powershell
# 设置变量
$AR = "us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel"
$SN = "deepseek-chat-agent"
$TAG = "v1.0.3"  # 使用新版本号
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

#### 步骤 3: 构建 Docker 镜像

```powershell
# 构建镜像（使用 --no-cache 确保使用最新代码）
docker build --no-cache -t deepseek-chat-agent:local .
```

#### 步骤 4: 标记镜像

```powershell
# 标记镜像（带版本号）
docker tag deepseek-chat-agent:local "$AR/$SN:$TAG"

# 标记镜像（latest）
docker tag deepseek-chat-agent:local "$AR/$SN:latest"
```

#### 步骤 5: 推送镜像到 Artifact Registry

```powershell
# 推送带版本号的镜像
docker push "$AR/$SN:$TAG"

# 推送 latest 标签
docker push "$AR/$SN:latest"
```

#### 步骤 6: 部署到 Cloud Run

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

#### 步骤 7: 验证部署

```powershell
# 获取服务 URL
gcloud run services describe $SN `
    --platform managed `
    --region $REGION `
    --project $PROJECT `
    --format="value(status.url)"

# 访问服务 URL（在浏览器中打开）
# 应该看到 Gradio 聊天界面
```

---

## 部署检查清单

### 代码检查

- [ ] `app/start_server.py` 中没有健康检查服务器代码
- [ ] `app/start_server.py` 直接启动 Gradio
- [ ] `Dockerfile` 使用 `CMD ["python", "-m", "app.start_server"]`
- [ ] 代码已提交到 GitHub

### 环境检查

- [ ] GitHub Secrets 已配置：
  - [ ] `GCP_SA_KEY`（Google Cloud 服务账号密钥）
  - [ ] `DEEPSEEK_API_KEY`（DeepSeek API 密钥）
  - [ ] `ARTIFACTORY_URL`（Artifact Registry URL）
  - [ ] `LARK_WEBHOOK_URL`（可选，用于通知）
- [ ] GitHub Environment `cloud-run-production` 已配置
- [ ] Required reviewers 已设置（如果需要审批）

### 部署检查

- [ ] Docker 镜像构建成功
- [ ] 镜像已推送到 Artifact Registry
- [ ] Cloud Run 服务部署成功
- [ ] 服务 URL 可访问
- [ ] 访问服务 URL 看到 Gradio 界面（不是 JSON）

---

## 常见问题

### Q1: 构建失败，提示 "无法找到镜像"

**A:** 这是正常的，因为 Artifact Registry 已清空。GitHub Actions 会重新构建并推送新镜像。

### Q2: 部署后仍然返回 JSON

**A:** 可能的原因：
1. 部署的镜像仍然是旧版本（检查镜像标签）
2. Gradio 启动失败（查看 Cloud Run 日志）
3. 代码未正确提交（确认 `app/start_server.py` 已更新）

**解决方法**：
1. 确认代码已提交
2. 使用 `--no-cache` 重新构建
3. 查看 Cloud Run 日志确认 Gradio 是否启动

### Q3: 如何查看 Cloud Run 日志？

```powershell
# 查看最近的日志
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=deepseek-chat-agent" `
    --limit 50 `
    --project firbase-app1-17308 `
    --format json

# 或查看实时日志
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=deepseek-chat-agent" `
    --project firbase-app1-17308
```

**关键日志信息**：
- `✓ Gradio module imported successfully`
- `✓ Gradio demo created successfully`
- `Running on local URL: http://127.0.0.1:8080`

### Q4: 部署需要多长时间？

**A:** 
- 构建镜像：约 5-10 分钟
- 推送镜像：约 1-2 分钟
- 部署到 Cloud Run：约 2-5 分钟
- **总计**：约 10-20 分钟

---

## 预期结果

部署成功后：

1. **访问服务 URL**：
   ```
   https://deepseek-chat-agent-205204734416.us-central1.run.app
   ```

2. **应该看到**：
   - Gradio 聊天界面（HTML 页面）
   - 聊天历史区域
   - 输入框
   - 发送按钮
   - 清除按钮
   - 温度滑块

3. **可以**：
   - 输入问题
   - 点击发送
   - 收到 AI 回复
   - 查看聊天历史

---

## 下一步

部署成功后，可以：
1. 测试聊天功能
2. 调整温度参数
3. 查看 Cloud Run 监控指标
4. 根据需要调整资源配置

如果遇到问题，请查看：
- `DEPLOYMENT_VERIFICATION.md` - 部署验证指南
- `CLOUD_RUN_TROUBLESHOOTING.md` - 故障排除指南
- Cloud Run 日志 - 获取详细错误信息

