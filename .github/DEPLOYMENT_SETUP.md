# GitHub Actions 部署配置指南

本文档说明如何配置 GitHub Actions 工作流以部署到 Google Cloud Run。

## 前置要求

1. Google Cloud 项目已创建
2. 已启用以下 API：
   - Cloud Run API
   - Container Registry API
   - Artifact Registry API（如果使用）

## 1. GitHub Secrets 配置

在 GitHub 仓库设置中添加以下 Secrets：

### 必需 Secrets

- `GCP_PROJECT_ID`: Google Cloud 项目 ID
- `GCP_SA_KEY`: Google Cloud 服务账号的 JSON 密钥
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥
- `LARK_WEBHOOK_URL`: Lark Webhook URL（用于发送通知）

### 可选 Secrets（Artifactory）

如果使用 Artifactory 存储 Docker 镜像，需要配置：

- `ARTIFACTORY_URL`: Artifactory URL（例如: `https://your-company.jfrog.io`）
- `ARTIFACTORY_REPO`: Artifactory Docker 仓库名称（默认: `docker-local`）
- `ARTIFACTORY_USER`: Artifactory 用户名
- `ARTIFACTORY_PASSWORD`: Artifactory 密码或 API Key

## 2. GitHub Environment 配置

为了启用部署审批功能，需要配置 GitHub Environment：

### 步骤

1. 前往仓库设置：`Settings` > `Environments`
2. 点击 `New environment`
3. 输入环境名称：`cloud-run-production`
4. 配置 `Required reviewers`：
   - 添加需要审批部署的用户或团队
   - 至少需要 1 个审批者
5. 可选：配置 `Wait timer`（部署等待时间）
6. 保存环境配置

### 环境配置示例

```
Environment name: cloud-run-production
Required reviewers: 
  - @your-team
  - @devops-team
Wait timer: 0 minutes (可选)
```

## 3. Google Cloud 服务账号配置

### 创建服务账号

```bash
# 创建服务账号
gcloud iam service-accounts create github-actions-sa \
  --display-name="GitHub Actions Service Account" \
  --project=YOUR_PROJECT_ID

# 授予必要权限
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# 创建并下载密钥
gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com

# 将 key.json 的内容复制到 GitHub Secret: GCP_SA_KEY
```

## 4. 工作流触发方式

### 自动触发（定时任务）

- **时间**: 每天北京时间 19:30
- **条件**: 检查当天 00:00-19:30 之间是否有代码提交
- **行为**: 
  - 如果有提交，自动构建并等待审批
  - 如果没有提交，发送通知并跳过构建

### 手动触发

1. 前往 `Actions` > `DeepSeek Chat Agent - Build & Deploy to Google Cloud Run`
2. 点击 `Run workflow`
3. 选择选项：
   - `force_build`: 强制构建（跳过 push 检查）
   - `approve_deployment`: 批准部署（跳过构建，直接部署）

## 5. 工作流流程

```
1. check-push (检查代码提交)
   ↓
2. send-no-push-email (如果没有提交，发送通知)
   ↓
3. build (构建 Docker 镜像)
   ├─ 构建镜像
   ├─ 推送到 GCR
   ├─ 推送到 Artifactory (可选)
   └─ 发送构建成功通知
   ↓
4. notify-pending-approval (发送等待审批通知)
   ↓
5. deploy-to-cloud-run (需要审批)
   ├─ 等待审批
   ├─ 部署到 Cloud Run
   └─ 发送部署结果通知
```

## 6. 通知配置

### Lark Webhook 设置

1. 在 Lark 群组中添加机器人
2. 获取 Webhook URL
3. 将 URL 添加到 GitHub Secret: `LARK_WEBHOOK_URL`

### 通知类型

- **无代码提交**: 当天没有代码提交时发送
- **构建成功**: 构建完成，等待审批
- **构建失败**: 构建过程中出错
- **等待审批**: 提醒审批者批准部署
- **部署成功**: 部署完成
- **部署失败**: 部署过程中出错
- **Job 失败**: 任何 job 失败时发送

## 7. 故障排查

### 常见问题

1. **权限错误**
   - 检查服务账号是否有足够权限
   - 确保已启用必要的 API

2. **Artifactory 推送失败**
   - 检查 Artifactory URL 和凭证
   - 如果不需要 Artifactory，可以不配置相关 Secrets

3. **审批不生效**
   - 检查 Environment 配置
   - 确保审批者在 Required reviewers 列表中

4. **定时任务不触发**
   - 检查 cron 表达式是否正确
   - 注意 UTC 时间和北京时间的转换

## 8. 最佳实践

1. **安全性**
   - 定期轮换服务账号密钥
   - 使用最小权限原则
   - 不要在代码中硬编码密钥

2. **监控**
   - 设置工作流通知
   - 监控 Cloud Run 服务状态
   - 定期检查日志

3. **成本控制**
   - 设置 Cloud Run 实例数量限制
   - 使用适当的资源配额
   - 监控 API 调用成本

## 9. 相关链接

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Google Cloud Run 文档](https://cloud.google.com/run/docs)
- [Lark 机器人文档](https://open.larkoffice.com/document/ukzNzUjL5YzM14SO2YTN)

