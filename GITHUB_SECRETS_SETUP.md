# GitHub Secrets 配置指南

## 📋 概述

本文档说明在 GitHub Actions 中需要配置的所有 Secrets。

## 🔐 必需的 Secrets

以下 Secrets 是**必须配置**的，否则工作流无法正常运行：

### 1. `GCP_PROJECT_ID` ⭐ 必需

**说明：** Google Cloud 项目 ID

**类型：** 字符串

**示例值：**
```
my-gcp-project-123456
```

**获取方式：**
1. 登录 [Google Cloud Console](https://console.cloud.google.com/)
2. 选择你的项目
3. 在项目信息中可以看到 Project ID

**配置位置：**
```
Settings → Secrets and variables → Actions → New repository secret
```

---

### 2. `GCP_SA_KEY` ⭐ 必需

**说明：** Google Cloud 服务账号的 JSON 密钥文件内容

**类型：** 多行文本（JSON）

**示例值：**
```json
{
  "type": "service_account",
  "project_id": "my-gcp-project-123456",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "github-actions@my-gcp-project-123456.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

**获取方式：**

1. **创建服务账号：**
   ```bash
   # 在 Google Cloud Console 中
   # IAM & Admin → Service Accounts → Create Service Account
   ```

2. **授予权限：**
   - Cloud Run Admin
   - Service Account User
   - Storage Admin（用于推送镜像到 GCR）

3. **创建密钥：**
   ```bash
   # 在服务账号详情页
   # Keys → Add Key → Create new key → JSON
   ```

4. **复制整个 JSON 文件内容**到 GitHub Secrets

**⚠️ 重要提示：**
- 这是敏感信息，不要提交到代码仓库
- 确保服务账号有足够的权限
- 定期轮换密钥以提高安全性

---

### 3. `DEEPSEEK_API_KEY` ⭐ 必需

**说明：** DeepSeek API 密钥

**类型：** 字符串

**示例值：**
```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**获取方式：**
1. 访问 [DeepSeek 官网](https://www.deepseek.com/)
2. 登录账户
3. 前往 API 密钥管理页面
4. 创建新的 API 密钥
5. 复制密钥（只显示一次，请妥善保存）

**用途：**
- 部署到 Cloud Run 时作为环境变量
- 用于调用 DeepSeek API

---

### 4. `LARK_WEBHOOK_URL` ⭐ 必需

**说明：** Lark（飞书）Webhook URL，用于发送部署通知

**类型：** URL 字符串

**示例值：**
```
https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxx
```

**获取方式：**

1. **在 Lark 中创建群聊机器人：**
   - 打开 Lark 群聊
   - 群设置 → 群机器人 → 添加机器人 → 自定义机器人

2. **配置机器人：**
   - 机器人名称：DeepSeek Chat Agent
   - 描述：GitHub Actions 部署通知
   - 安全设置：选择"自定义关键词"或"签名校验"

3. **获取 Webhook URL：**
   - 复制生成的 Webhook 地址

**用途：**
- 发送构建成功/失败通知
- 发送部署成功/失败通知
- 发送等待审批通知

**⚠️ 如果没有 Lark，可以：**
- 暂时留空（工作流会失败，但不影响核心功能）
- 或者使用其他通知服务（需要修改工作流）

---

## 🔧 可选的 Secrets（Artifactory）

以下 Secrets 是**可选的**，只有在需要将镜像推送到 Artifactory 时才需要配置：

### 5. `ARTIFACTORY_URL` ⚪ 可选

**说明：** Artifactory 服务器 URL

**类型：** URL 字符串

**示例值：**
```
https://your-company.jfrog.io
```

**默认行为：**
- 如果未配置，工作流会跳过推送到 Artifactory 的步骤
- 不会影响构建和部署到 Cloud Run

---

### 6. `ARTIFACTORY_REPO` ⚪ 可选

**说明：** Artifactory Docker 仓库名称

**类型：** 字符串

**示例值：**
```
docker-local
```

**默认值：**
- 如果未配置，默认使用 `docker-local`

---

### 7. `ARTIFACTORY_USER` ⚪ 可选

**说明：** Artifactory 用户名

**类型：** 字符串

**示例值：**
```
my-artifactory-user
```

**注意：**
- 如果配置了 `ARTIFACTORY_URL`，建议同时配置用户名和密码

---

### 8. `ARTIFACTORY_PASSWORD` ⚪ 可选

**说明：** Artifactory 密码或 API Key

**类型：** 字符串（敏感信息）

**示例值：**
```
your-artifactory-password-or-api-key
```

**注意：**
- 可以是密码或 API Key
- 建议使用 API Key 而不是密码

---

## 📝 配置步骤

### 方法 1：通过 GitHub Web 界面

1. **进入仓库设置：**
   ```
   仓库 → Settings → Secrets and variables → Actions
   ```

2. **添加 Secret：**
   - 点击 "New repository secret"
   - 输入 Name（Secret 名称）
   - 输入 Value（Secret 值）
   - 点击 "Add secret"

3. **重复步骤 2**，添加所有必需的 Secrets

### 方法 2：通过 GitHub CLI

```bash
# 安装 GitHub CLI (gh)
# https://cli.github.com/

# 设置 Secrets
gh secret set GCP_PROJECT_ID --body "my-gcp-project-123456"
gh secret set GCP_SA_KEY < service-account-key.json
gh secret set DEEPSEEK_API_KEY --body "sk-xxxxxxxxxxxxxxxx"
gh secret set LARK_WEBHOOK_URL --body "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"
```

---

## ✅ 配置检查清单

在运行工作流之前，请确认已配置：

- [ ] `GCP_PROJECT_ID` - Google Cloud 项目 ID
- [ ] `GCP_SA_KEY` - Google Cloud 服务账号密钥（JSON）
- [ ] `DEEPSEEK_API_KEY` - DeepSeek API 密钥
- [ ] `LARK_WEBHOOK_URL` - Lark Webhook URL（可选，但建议配置）

**可选配置（如果需要 Artifactory）：**
- [ ] `ARTIFACTORY_URL` - Artifactory URL
- [ ] `ARTIFACTORY_REPO` - Artifactory 仓库名称
- [ ] `ARTIFACTORY_USER` - Artifactory 用户名
- [ ] `ARTIFACTORY_PASSWORD` - Artifactory 密码

---

## 🔒 安全最佳实践

### 1. 最小权限原则

- 服务账号只授予必要的权限
- 定期审查和更新权限

### 2. 密钥轮换

- 定期轮换 API 密钥和服务账号密钥
- 建议每 90 天轮换一次

### 3. 访问控制

- 限制可以访问 Secrets 的人员
- 使用 GitHub 的 Environment 保护规则

### 4. 监控和审计

- 定期检查 GitHub Actions 日志
- 监控异常活动

---

## 🐛 常见问题

### Q: 工作流失败，提示 "Secret not found"

**A:** 检查是否已配置所有必需的 Secrets，特别是：
- `GCP_PROJECT_ID`
- `GCP_SA_KEY`
- `DEEPSEEK_API_KEY`

### Q: 部署失败，提示 "Permission denied"

**A:** 检查服务账号权限：
- Cloud Run Admin
- Service Account User
- Storage Admin

### Q: 无法推送到 Artifactory

**A:** 检查 Artifactory 相关 Secrets：
- `ARTIFACTORY_URL`
- `ARTIFACTORY_USER`
- `ARTIFACTORY_PASSWORD`

如果不需要 Artifactory，可以不配置这些 Secrets。

### Q: Lark 通知没有收到

**A:** 检查：
- `LARK_WEBHOOK_URL` 是否正确
- Webhook 是否已启用
- 网络连接是否正常

---

## 📚 相关文档

- [GitHub Secrets 文档](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Google Cloud 服务账号文档](https://cloud.google.com/iam/docs/service-accounts)
- [DeepSeek API 文档](https://platform.deepseek.com/api-docs/)
- [Lark 机器人文档](https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN)

---

## 🎯 快速配置模板

### 最小配置（必需）

```yaml
Secrets:
  GCP_PROJECT_ID: "your-project-id"
  GCP_SA_KEY: "{...JSON内容...}"
  DEEPSEEK_API_KEY: "sk-xxxxxxxx"
  LARK_WEBHOOK_URL: "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"
```

### 完整配置（包含 Artifactory）

```yaml
Secrets:
  GCP_PROJECT_ID: "your-project-id"
  GCP_SA_KEY: "{...JSON内容...}"
  DEEPSEEK_API_KEY: "sk-xxxxxxxx"
  LARK_WEBHOOK_URL: "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"
  ARTIFACTORY_URL: "https://your-company.jfrog.io"
  ARTIFACTORY_REPO: "docker-local"
  ARTIFACTORY_USER: "your-username"
  ARTIFACTORY_PASSWORD: "your-password"
```

---

**配置完成后，工作流就可以正常运行了！** 🚀

