# 本地构建和推送 Docker 镜像到 Google Artifact Registry

本文档说明如何在本地构建 Docker 镜像并推送到 Google Artifact Registry。

## 前置要求

1. **安装 Docker Desktop**（Windows/Mac）或 Docker Engine（Linux）
2. **安装 Google Cloud SDK (gcloud)**
3. **配置 Google Cloud 认证**

## 配置信息

- **Artifact Registry URL**: `us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel`
- **服务名称**: `deepseek-chat-agent`
- **项目 ID**: `firbase-app1-17308`
- **区域**: `us-central1`

## 步骤 1: 配置 Google Cloud 认证

### 方法 A: 使用服务账号密钥文件（推荐）

```powershell
# 1. 设置环境变量（如果使用服务账号 JSON 文件）
$env:GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"

# 2. 配置 Docker 认证
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
```

### 方法 B: 使用用户账号认证

```powershell
# 1. 登录 Google Cloud
gcloud auth login

# 2. 设置项目
gcloud config set project firbase-app1-17308

# 3. 配置 Docker 认证
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
```

## 步骤 2: 构建 Docker 镜像

### 基本构建命令

```powershell
# 在项目根目录执行
docker build -t deepseek-chat-agent:local .
```

### 带版本标签的构建

```powershell
# 使用版本号作为标签
docker build -t deepseek-chat-agent:v1.0.0 .

# 或使用时间戳
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
docker build -t deepseek-chat-agent:$timestamp .
```

## 步骤 3: 标记镜像（Tag）

在推送到 Artifact Registry 之前，需要将镜像标记为 Artifact Registry 的完整路径：

```powershell
# 设置变量
$ARTIFACT_REGISTRY_URL = "us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel"
$SERVICE_NAME = "deepseek-chat-agent"
$IMAGE_TAG = "v1.0.0"  # 或使用 "latest", "local", 时间戳等

# 标记镜像（完整路径）
docker tag deepseek-chat-agent:local "$ARTIFACT_REGISTRY_URL/$SERVICE_NAME:$IMAGE_TAG"

# 同时标记为 latest
docker tag deepseek-chat-agent:local "$ARTIFACT_REGISTRY_URL/$SERVICE_NAME:latest"
```

### 一行命令（PowerShell）

```powershell
$ARTIFACT_REGISTRY_URL = "us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel"
$SERVICE_NAME = "deepseek-chat-agent"
$IMAGE_TAG = "v1.0.0"

docker tag deepseek-chat-agent:local "$ARTIFACT_REGISTRY_URL/$SERVICE_NAME:$IMAGE_TAG"
docker tag deepseek-chat-agent:local "$ARTIFACT_REGISTRY_URL/$SERVICE_NAME:latest"
```

## 步骤 4: 推送镜像到 Artifact Registry

```powershell
# 推送指定标签
docker push "$ARTIFACT_REGISTRY_URL/$SERVICE_NAME:$IMAGE_TAG"

# 推送 latest 标签
docker push "$ARTIFACT_REGISTRY_URL/$SERVICE_NAME:latest"
```

## 完整脚本（PowerShell）

将以下内容保存为 `build-and-push.ps1`：

```powershell
# 配置变量
$ARTIFACT_REGISTRY_URL = "us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel"
$SERVICE_NAME = "deepseek-chat-agent"
$IMAGE_TAG = "v1.0.0"  # 可以改为 latest, local, 或时间戳

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "构建和推送 Docker 镜像" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 步骤 1: 构建镜像
Write-Host "步骤 1: 构建 Docker 镜像..." -ForegroundColor Yellow
docker build -t "$SERVICE_NAME:local" .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 构建失败" -ForegroundColor Red
    exit 1
}
Write-Host "✅ 构建成功" -ForegroundColor Green
Write-Host ""

# 步骤 2: 标记镜像
Write-Host "步骤 2: 标记镜像..." -ForegroundColor Yellow
$FULL_IMAGE_NAME = "$ARTIFACT_REGISTRY_URL/$SERVICE_NAME:$IMAGE_TAG"
docker tag "$SERVICE_NAME:local" $FULL_IMAGE_NAME
docker tag "$SERVICE_NAME:local" "$ARTIFACT_REGISTRY_URL/$SERVICE_NAME:latest"
Write-Host "✅ 标记成功: $FULL_IMAGE_NAME" -ForegroundColor Green
Write-Host ""

# 步骤 3: 推送镜像
Write-Host "步骤 3: 推送镜像到 Artifact Registry..." -ForegroundColor Yellow
docker push $FULL_IMAGE_NAME
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 推送失败" -ForegroundColor Red
    exit 1
}
Write-Host "✅ 推送成功" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "完成！" -ForegroundColor Cyan
Write-Host "镜像地址: $FULL_IMAGE_NAME" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
```

### 使用方法

```powershell
# 运行脚本
.\build-and-push.ps1

# 或指定标签
$env:IMAGE_TAG="v1.0.0"; .\build-and-push.ps1
```

## 快速命令（一行）

### 构建、标记和推送（PowerShell）

```powershell
$AR="us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel"; $SN="deepseek-chat-agent"; $TAG="v1.0.0"; docker build -t "$SN:local" .; docker tag "$SN:local" "$AR/$SN:$TAG"; docker tag "$SN:local" "$AR/$SN:latest"; docker push "$AR/$SN:$TAG"; docker push "$AR/$SN:latest"
```

### 分步执行

```powershell
# 1. 构建
docker build -t deepseek-chat-agent:local .

# 2. 标记
docker tag deepseek-chat-agent:local us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:v1.0.0
docker tag deepseek-chat-agent:local us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:latest

# 3. 推送
docker push us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:v1.0.0
docker push us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:latest
```

## 验证推送

### 查看 Artifact Registry 中的镜像

```powershell
# 列出所有镜像
gcloud artifacts docker images list us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent

# 查看特定标签
gcloud artifacts docker images list us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent --include-tags
```

### 在浏览器中查看

访问 Google Cloud Console：
```
https://console.cloud.google.com/artifacts/docker/firbase-app1-17308/us-central1/smartageintel?project=firbase-app1-17308
```

## 常见问题

### 问题 1: 认证失败

**错误**: `unauthorized: You don't have the required permissions`

**解决**:
```powershell
# 重新配置认证
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet

# 或使用服务账号
$env:GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
gcloud auth activate-service-account --key-file=$env:GOOGLE_APPLICATION_CREDENTIALS
```

### 问题 2: 权限不足

**错误**: `denied: Permission denied`

**解决**: 确保服务账号或用户账号具有 `Artifact Registry Writer` 权限。

### 问题 3: 仓库不存在

**错误**: `repository not found`

**解决**: 创建 Artifact Registry 仓库：
```powershell
gcloud artifacts repositories create smartageintel `
    --repository-format=docker `
    --location=us-central1 `
    --description="SmartAge Intel Docker repository"
```

## 部署到 Cloud Run

推送成功后，可以使用以下命令部署到 Cloud Run：

```powershell
$IMAGE_URL = "us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:v1.0.0"

gcloud run deploy deepseek-chat-agent `
    --image $IMAGE_URL `
    --platform managed `
    --region us-central1 `
    --project firbase-app1-17308 `
    --allow-unauthenticated `
    --set-env-vars DEEPSEEK_API_KEY=$env:DEEPSEEK_API_KEY `
    --memory 2Gi `
    --cpu 2 `
    --port 8080
```

## 参考

- [Google Artifact Registry 文档](https://cloud.google.com/artifact-registry/docs)
- [Docker 构建最佳实践](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

