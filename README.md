# DeepSeek Chat Agent

基于LangChain和DeepSeek API的聊天服务，使用FastAPI构建，可部署到Google Cloud Run。

## 功能特性

- ✅ 使用LangChain集成DeepSeek v3 API
- ✅ FastAPI Web服务器提供RESTful API
- ✅ Token控制（最大5000 tokens）
- ✅ Docker容器化部署
- ✅ GitHub Actions自动部署到Google Cloud Run
- ✅ 支持流式和非流式响应

## 项目结构

```
.
├── app/
│   └── main.py          # FastAPI应用主文件
├── .github/
│   └── workflows/
│       └── deploy-cloud-run.yml  # GitHub Actions部署配置
├── Dockerfile           # Docker镜像构建文件
├── requirements.txt     # Python依赖
├── .env.example        # 环境变量示例
└── README.md           # 项目说明文档
```

## 快速开始

### 本地开发

**📖 详细的本地运行步骤请参考 [LOCAL_RUN_GUIDE.md](LOCAL_RUN_GUIDE.md)**

**快速开始:**

1. **克隆项目**
```bash
git clone <your-repo-url>
cd deepseek-chat-agent
```

2. **创建虚拟环境（推荐）**
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**

创建 `.env` 文件：
```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com
PORT=8080
```

5. **运行服务**
```bash
# 方法1: 使用 uvicorn（推荐，支持热重载）
uvicorn app.main:app --reload --port 8080

# 方法2: 直接运行 Python
python -m app.main
```

6. **访问API文档**
打开浏览器访问: http://localhost:8080/docs

7. **测试API（可选）**
```bash
python test_api.py
```

### Docker本地运行

```bash
# 构建镜像
docker build -t deepseek-chat-agent .

# 运行容器
docker run -p 8080:8080 -e DEEPSEEK_API_KEY=your_key_here deepseek-chat-agent
```

## API接口

### 1. 健康检查
```bash
GET /health
```

### 2. 简化聊天接口
```bash
POST /api/chat/simple
Content-Type: application/json

{
  "user_input": "你好，请介绍一下你自己"
}
```

### 3. 完整聊天接口
```bash
POST /api/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "什么是人工智能？"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 5000
}
```

### 响应示例
```json
{
  "message": "人工智能（AI）是...",
  "usage": {
    "estimated_tokens": 150,
    "max_tokens": 5000
  }
}
```

## 部署到Google Cloud Run

### 前置要求

1. Google Cloud项目
2. 启用以下API：
   - Cloud Run API
   - Container Registry API
   - Cloud Build API

3. 创建服务账号并授予权限：
   - Cloud Run Admin
   - Service Account User
   - Storage Admin

### GitHub Secrets配置

在GitHub仓库设置以下Secrets：

**必需Secrets:**
- `GCP_PROJECT_ID`: Google Cloud项目ID
- `GCP_SA_KEY`: 服务账号的JSON密钥
- `DEEPSEEK_API_KEY`: DeepSeek API密钥
- `LARK_WEBHOOK_URL`: Lark Webhook URL（用于发送通知）

**可选Secrets（Artifactory）:**
- `ARTIFACTORY_URL`: Artifactory URL
- `ARTIFACTORY_REPO`: Artifactory Docker仓库名称（默认: docker-local）
- `ARTIFACTORY_USER`: Artifactory 用户名
- `ARTIFACTORY_PASSWORD`: Artifactory 密码或API Key

### GitHub Environment配置

为了启用部署审批功能，需要配置GitHub Environment：

1. 前往仓库设置：`Settings` > `Environments`
2. 创建新环境：`cloud-run-production`
3. 配置 `Required reviewers`：添加需要审批部署的用户或团队
4. 保存配置

详细配置说明请参考 [.github/DEPLOYMENT_SETUP.md](.github/DEPLOYMENT_SETUP.md)

### 工作流功能

#### 1. 定时构建和部署

- **触发时间**: 每天北京时间 19:30
- **检查逻辑**: 
  - 检查当天 00:00-19:30 之间是否有代码提交
  - 如果有提交，自动构建并等待审批
  - 如果没有提交，发送通知并跳过构建

#### 2. 失败通知

- 每个job失败时自动发送Lark通知
- 包含详细的错误信息和日志链接

#### 3. Docker镜像管理

- 构建Docker镜像
- 推送到Google Container Registry (GCR)
- 可选：推送到Artifactory（如果配置了相关Secrets）

#### 4. 部署审批

- 使用GitHub Environment进行部署审批
- 只有配置的审批者才能批准部署
- 部署前发送等待审批通知

#### 5. 通知系统

- **无代码提交**: 当天没有代码提交时发送
- **构建成功**: 构建完成，等待审批
- **构建失败**: 构建过程中出错
- **等待审批**: 提醒审批者批准部署
- **部署成功**: 部署完成
- **部署失败**: 部署过程中出错

### 自动部署

推送代码到`main`分支，GitHub Actions会自动：
1. 检查代码提交（定时任务时）
2. 构建Docker镜像
3. 推送到Google Container Registry
4. 可选：推送到Artifactory
5. 等待审批
6. 部署到Cloud Run

### 手动部署

```bash
# 设置项目
gcloud config set project YOUR_PROJECT_ID

# 构建并推送镜像
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/deepseek-chat-agent

# 部署到Cloud Run
gcloud run deploy deepseek-chat-agent \
  --image gcr.io/YOUR_PROJECT_ID/deepseek-chat-agent \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --set-env-vars DEEPSEEK_API_KEY=your_key_here \
  --memory 512Mi \
  --cpu 1
```

### 手动触发工作流

1. 前往 `Actions` > `DeepSeek Chat Agent - Build & Deploy to Google Cloud Run`
2. 点击 `Run workflow`
3. 选择选项：
   - `force_build`: 强制构建（跳过 push 检查）
   - `approve_deployment`: 批准部署（跳过构建，直接部署）

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥（必需） | - |
| `DEEPSEEK_API_BASE` | DeepSeek API基础URL | https://api.deepseek.com |
| `PORT` | 服务端口 | 8080 |

## 相关开源项目

以下是一些类似的开源项目，可以作为参考：

1. **LangChain官方示例**
   - https://github.com/langchain-ai/langchain
   - LangChain框架的官方仓库，包含大量集成示例

2. **FastAPI + LangChain项目**
   - https://github.com/hwchase17/langchain-fastapi-template
   - FastAPI和LangChain的模板项目

3. **ChatGPT API服务**
   - https://github.com/acheong08/ChatGPT
   - 类似的聊天API服务实现

4. **Google Cloud Run示例**
   - https://github.com/GoogleCloudPlatform/python-docs-samples
   - Google Cloud官方Python示例，包含Cloud Run部署

5. **DeepSeek相关项目**
   - https://github.com/deepseek-ai
   - DeepSeek官方GitHub组织

## 注意事项

1. **API密钥安全**: 确保不要将API密钥提交到代码仓库
2. **Token限制**: 当前设置为最大5000 tokens，可根据需要调整
3. **成本控制**: 注意API调用成本，建议设置Cloud Run的实例数量限制
4. **CORS配置**: 生产环境应该限制允许的域名

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

