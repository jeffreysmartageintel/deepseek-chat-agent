# Google Artifact Registry 配置说明

## 📋 概述

工作流已更新为支持 Google Artifact Registry，移除了 Artifactory 相关的配置。

## 🔧 主要变更

### 移除的 Secrets（不再需要）

- ❌ `ARTIFACTORY_REPO` - 已移除
- ❌ `ARTIFACTORY_USER` - 已移除
- ❌ `ARTIFACTORY_PASSWORD` - 已移除

### 保留的 Secret（可选）

- ✅ `ARTIFACTORY_URL` - 用于 Google Artifact Registry URL
  - 示例值：`asia-east1-docker.pkg.dev/firbase-app1-17308/smartage`
  - 格式：`REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME`

## 🔐 认证方式

Google Artifact Registry 使用 **Google Cloud 服务账号认证**，不需要用户名和密码：

1. 使用 `GCP_SA_KEY` 进行认证
2. 通过 `gcloud auth configure-docker` 配置 Docker
3. 自动使用服务账号权限推送镜像

## 📝 配置步骤

### 1. 在 GitHub Secrets 中配置

**Secret 名称：** `ARTIFACTORY_URL`

**Secret 值：** 
```
asia-east1-docker.pkg.dev/firbase-app1-17308/smartage
```

**注意：**
- 不包含 `https://`
- 不包含镜像名称
- 格式：`REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME`

### 2. 确保服务账号权限

服务账号（`GCP_SA_KEY`）需要以下权限：

- ✅ Cloud Run Admin
- ✅ Service Account User
- ✅ Storage Admin（用于 GCR）
- ✅ **Artifact Registry Writer**（用于 Artifact Registry）

### 3. 验证配置

工作流会自动：
1. 从 Secret 读取 `ARTIFACTORY_URL`
2. 配置 Docker 认证
3. 构建镜像并打标签
4. 推送到 Artifact Registry（如果配置了）

## 🎯 镜像路径

配置后，镜像会被推送到：

```
asia-east1-docker.pkg.dev/firbase-app1-17308/smartage/deepseek-chat-agent:TAG
asia-east1-docker.pkg.dev/firbase-app1-17308/smartage/deepseek-chat-agent:latest
```

其中 `TAG` 是 Git commit SHA。

## ✅ 验证

部署成功后，可以在 Google Cloud Console 中查看：

1. 前往 [Artifact Registry](https://console.cloud.google.com/artifacts)
2. 选择你的仓库：`smartage`
3. 应该能看到 `deepseek-chat-agent` 镜像

## 📚 相关文档

- [Google Artifact Registry 文档](https://cloud.google.com/artifact-registry/docs)
- [GitHub Secrets 配置指南](GITHUB_SECRETS_SETUP.md)

