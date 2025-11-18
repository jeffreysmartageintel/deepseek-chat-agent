# 本地运行指南

本文档提供详细的本地运行步骤，帮助你在本地开发环境中运行 DeepSeek Chat Agent。

## 前置要求

### 1. Python 环境

- **Python 版本**: Python 3.9 或更高版本（推荐 Python 3.11）
- **包管理器**: pip

### 2. DeepSeek API Key

你需要一个有效的 DeepSeek API Key。如果没有，请访问 [DeepSeek 官网](https://www.deepseek.com) 获取。

## 详细运行步骤

### 步骤 1: 克隆或进入项目目录

```bash
# 如果是从远程仓库克隆
git clone <your-repo-url>
cd deepseek-chat-agent

# 如果已经在项目目录中，直接进入
cd deepseek-chat-agent
```

### 步骤 2: 创建 Python 虚拟环境（推荐）

**Windows (PowerShell):**
```powershell
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

激活成功后，命令行提示符前会显示 `(venv)`。

### 步骤 3: 安装依赖

```bash
# 升级 pip（可选但推荐）
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

如果安装过程中遇到问题，可以尝试：

```bash
# 使用国内镜像源（如果网络较慢）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 步骤 4: 配置环境变量

创建 `.env` 文件（在项目根目录）：

**Windows (PowerShell):**
```powershell
# 创建 .env 文件
New-Item -Path .env -ItemType File

# 编辑 .env 文件（使用记事本或其他编辑器）
notepad .env
```

**macOS/Linux:**
```bash
# 创建并编辑 .env 文件
nano .env
# 或
vim .env
```

在 `.env` 文件中添加以下内容：

```env
# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com

# 服务器配置
PORT=8080
```

**重要**: 将 `your_deepseek_api_key_here` 替换为你的实际 DeepSeek API Key。

### 步骤 5: 修改代码以支持 .env 文件（如果需要）

如果代码中没有自动加载 `.env` 文件，我们需要添加这个功能。检查 `app/main.py` 是否已经导入了 `python-dotenv`。

### 步骤 6: 运行应用

#### 方法 1: 直接运行 Python 文件

```bash
# 确保在项目根目录
python -m app.main
```

或者：

```bash
python app/main.py
```

#### 方法 2: 使用 uvicorn 命令（推荐）

```bash
# 从项目根目录运行
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

参数说明：
- `--reload`: 开发模式，代码修改后自动重启
- `--host 0.0.0.0`: 允许外部访问（默认只允许 localhost）
- `--port 8080`: 指定端口号

#### 方法 3: 使用环境变量指定端口

```bash
# Windows (PowerShell)
$env:PORT=8080; uvicorn app.main:app --reload

# Windows (CMD)
set PORT=8080 && uvicorn app.main:app --reload

# macOS/Linux
PORT=8080 uvicorn app.main:app --reload
```

### 步骤 7: 验证服务运行

服务启动成功后，你会看到类似以下的输出：

```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

### 步骤 8: 测试 API

#### 方法 1: 使用浏览器访问

1. **健康检查**:
   ```
   http://localhost:8080/
   ```
   或
   ```
   http://localhost:8080/health
   ```

2. **API 文档（Swagger UI）**:
   ```
   http://localhost:8080/docs
   ```

3. **API 文档（ReDoc）**:
   ```
   http://localhost:8080/redoc
   ```

#### 方法 2: 使用 curl 命令

**Windows (PowerShell):**
```powershell
# 健康检查
curl http://localhost:8080/health

# 测试简化聊天接口
curl -X POST "http://localhost:8080/api/chat/simple?user_input=你好，请介绍一下你自己" -H "Content-Type: application/json"

# 测试完整聊天接口
curl -X POST "http://localhost:8080/api/chat" `
  -H "Content-Type: application/json" `
  -d '{"messages": [{"role": "user", "content": "什么是人工智能？"}]}'
```

**macOS/Linux:**
```bash
# 健康检查
curl http://localhost:8080/health

# 测试简化聊天接口
curl -X POST "http://localhost:8080/api/chat/simple?user_input=你好，请介绍一下你自己" \
  -H "Content-Type: application/json"

# 测试完整聊天接口
curl -X POST "http://localhost:8080/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "什么是人工智能？"}]}'
```

#### 方法 3: 使用 Python requests

创建测试文件 `test_api.py`:

```python
import requests
import json

# 测试健康检查
response = requests.get("http://localhost:8080/health")
print("Health Check:", response.json())

# 测试简化聊天接口
response = requests.post(
    "http://localhost:8080/api/chat/simple",
    params={"user_input": "你好，请介绍一下你自己"}
)
print("\nSimple Chat Response:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# 测试完整聊天接口
response = requests.post(
    "http://localhost:8080/api/chat",
    json={
        "messages": [
            {"role": "user", "content": "什么是人工智能？"}
        ],
        "temperature": 0.7,
        "max_tokens": 5000
    }
)
print("\nFull Chat Response:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

运行测试：
```bash
python test_api.py
```

## 常见问题排查

### 问题 1: 找不到模块

**错误信息**: `ModuleNotFoundError: No module named 'xxx'`

**解决方案**:
```bash
# 确保虚拟环境已激活
# 重新安装依赖
pip install -r requirements.txt
```

### 问题 2: API Key 未设置

**错误信息**: `ValueError: DEEPSEEK_API_KEY environment variable is not set`

**解决方案**:
1. 检查 `.env` 文件是否存在
2. 检查 `.env` 文件中的 API Key 是否正确
3. 确保代码中加载了 `.env` 文件（需要 `python-dotenv`）

### 问题 3: 端口被占用

**错误信息**: `Address already in use`

**解决方案**:
```bash
# Windows: 查找占用端口的进程
netstat -ano | findstr :8080

# macOS/Linux: 查找占用端口的进程
lsof -i :8080

# 或者使用其他端口
uvicorn app.main:app --reload --port 8081
```

### 问题 4: LangChain 导入错误

**错误信息**: `ImportError: cannot import name 'ChatDeepSeek'`

**解决方案**:
LangChain 的 API 可能在不同版本中有所变化。如果遇到导入错误，可以：

1. 检查 LangChain 版本：
```bash
pip show langchain langchain-community
```

2. 如果版本不兼容，尝试更新：
```bash
pip install --upgrade langchain langchain-community
```

3. 或者使用兼容的版本（查看代码中的实际导入）

### 问题 5: 网络连接问题

**错误信息**: 无法连接到 DeepSeek API

**解决方案**:
1. 检查网络连接
2. 检查 API Key 是否有效
3. 检查 API Base URL 是否正确
4. 如果在中国大陆，可能需要配置代理

## 开发模式建议

### 1. 使用热重载

启动时添加 `--reload` 参数，代码修改后自动重启：

```bash
uvicorn app.main:app --reload
```

### 2. 查看详细日志

代码中已经配置了日志，可以在控制台查看详细的运行信息。

### 3. 使用 API 文档

访问 `http://localhost:8080/docs` 可以：
- 查看所有 API 端点
- 测试 API 接口
- 查看请求/响应格式

## 停止服务

在运行服务的终端中按 `Ctrl + C` 停止服务。

## 下一步

- 查看 [README.md](README.md) 了解项目完整功能
- 查看 [.github/DEPLOYMENT_SETUP.md](.github/DEPLOYMENT_SETUP.md) 了解部署配置
- 开始开发你的功能！

## 需要帮助？

如果遇到问题，请：
1. 检查本文档的"常见问题排查"部分
2. 查看 GitHub Issues
3. 查看项目文档

