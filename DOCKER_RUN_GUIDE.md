# Docker 运行指南

## 问题分析

### 错误命令

```powershell
docker run -p 8080:8080 -e DEEPSEEK_API_KEY=xxx deepseek-chat-agent:local us-central1-docker.pkg.dev/...
```

**错误原因：**
- `docker run` 的语法是：`docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`
- `deepseek-chat-agent:local` 是镜像名
- `us-central1-docker.pkg.dev/...` 被当作命令参数，Docker 试图执行它作为命令
- 导致错误：`exec: "us-central1-docker.pkg.dev/...": no such file or directory`

## 正确的使用方法

### 方法 1: 使用本地构建的镜像（推荐用于本地测试）

```powershell
# 1. 构建本地镜像
docker build -t deepseek-chat-agent:local .

# 2. 运行本地镜像
docker run -p 8080:8080 -e DEEPSEEK_API_KEY=sk-7b8adc0f4c0a4acea30b6e8b39e4f870 deepseek-chat-agent:local
```

### 方法 2: 从 Artifact Registry 拉取并运行

```powershell
# 1. 配置认证（首次使用）
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet

# 2. 从 Artifact Registry 拉取镜像
docker pull us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:latest

# 3. 运行镜像（使用完整路径）
docker run -p 8080:8080 `
    -e DEEPSEEK_API_KEY=sk-7b8adc0f4c0a4acea30b6e8b39e4f870 `
    us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:latest
```

### 方法 3: 拉取后使用简短名称运行

```powershell
# 1. 拉取镜像
docker pull us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:latest

# 2. 标记为简短名称（可选，方便使用）
docker tag us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:latest deepseek-chat-agent:latest

# 3. 使用简短名称运行
docker run -p 8080:8080 -e DEEPSEEK_API_KEY=sk-7b8adc0f4c0a4acea30b6e8b39e4f870 deepseek-chat-agent:latest
```

## 完整工作流程

### 场景 A: 本地开发测试

```powershell
# 1. 构建本地镜像
docker build -t deepseek-chat-agent:local .

# 2. 运行测试
docker run -p 8080:8080 `
    -e DEEPSEEK_API_KEY=sk-7b8adc0f4c0a4acea30b6e8b39e4f870 `
    -e DEEPSEEK_API_BASE=https://api.deepseek.com/v1 `
    deepseek-chat-agent:local

# 3. 访问应用
# 浏览器打开: http://localhost:8080
```

### 场景 B: 使用 Artifact Registry 镜像

```powershell
# 1. 配置认证
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet

# 2. 拉取最新镜像
docker pull us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:latest

# 3. 运行镜像
docker run -p 8080:8080 `
    -e DEEPSEEK_API_KEY=sk-7b8adc0f4c0a4acea30b6e8b39e4f870 `
    -e DEEPSEEK_API_BASE=https://api.deepseek.com/v1 `
    us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:latest
```

## 常用 Docker 命令

### 查看本地镜像

```powershell
docker images
```

### 查看运行中的容器

```powershell
docker ps
```

### 停止容器

```powershell
# 查找容器 ID
docker ps

# 停止容器
docker stop <container_id>
```

### 查看容器日志

```powershell
# 运行中的容器
docker logs <container_id>

# 实时查看日志
docker logs -f <container_id>
```

### 进入容器调试

```powershell
docker exec -it <container_id> /bin/bash
```

## 环境变量配置

### 使用环境变量文件

创建 `.env.docker` 文件：

```env
DEEPSEEK_API_KEY=sk-7b8adc0f4c0a4acea30b6e8b39e4f870
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
PORT=8080
```

运行命令：

```powershell
docker run -p 8080:8080 --env-file .env.docker deepseek-chat-agent:local
```

### 直接在命令行设置

```powershell
docker run -p 8080:8080 `
    -e DEEPSEEK_API_KEY=sk-7b8adc0f4c0a4acea30b6e8b39e4f870 `
    -e DEEPSEEK_API_BASE=https://api.deepseek.com/v1 `
    -e PORT=8080 `
    deepseek-chat-agent:local
```

## 常见问题

### Q1: 如何知道使用哪个镜像？

**A:** 
- **本地开发测试**：使用 `deepseek-chat-agent:local`（本地构建）
- **测试 Artifact Registry 镜像**：使用完整路径 `us-central1-docker.pkg.dev/...`
- **生产环境**：在 Cloud Run 上使用 Artifact Registry 镜像

### Q2: 端口被占用怎么办？

**A:** 使用其他端口：

```powershell
docker run -p 8081:8080 -e DEEPSEEK_API_KEY=xxx deepseek-chat-agent:local
```

然后访问 `http://localhost:8081`

### Q3: 如何查看容器是否正常启动？

**A:** 

```powershell
# 查看容器状态
docker ps

# 查看日志
docker logs <container_id>

# 实时查看日志
docker logs -f <container_id>
```

### Q4: 如何清理旧的容器和镜像？

**A:**

```powershell
# 停止所有容器
docker stop $(docker ps -aq)

# 删除所有停止的容器
docker rm $(docker ps -aq)

# 删除未使用的镜像
docker image prune -a
```

## 快速参考

### 本地测试（最常用）

```powershell
# 构建
docker build -t deepseek-chat-agent:local .

# 运行
docker run -p 8080:8080 -e DEEPSEEK_API_KEY=your_key deepseek-chat-agent:local
```

### 使用 Artifact Registry 镜像

```powershell
# 拉取
docker pull us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:latest

# 运行
docker run -p 8080:8080 -e DEEPSEEK_API_KEY=your_key us-central1-docker.pkg.dev/firbase-app1-17308/smartageintel/deepseek-chat-agent:latest
```

## 总结

**关键点：**
1. `docker run` 命令中，镜像名后面不应该有其他路径
2. 如果要使用 Artifact Registry 镜像，先 `docker pull`，然后使用完整路径运行
3. 本地测试推荐使用本地构建的镜像（`deepseek-chat-agent:local`）

