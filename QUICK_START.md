# 快速启动指南

本文档提供最简洁的本地启动步骤，帮助你在本地快速运行 DeepSeek Chat Agent。

## 前置要求

- **Python 3.11+**（推荐）
- **DeepSeek API Key**（从 [DeepSeek 官网](https://www.deepseek.com) 获取）

## 快速启动步骤（Windows PowerShell）

### 1. 进入项目目录

```powershell
cd D:\smartage-code\deepseek-chat-agent
```

### 2. 创建并激活虚拟环境

```powershell
# 创建虚拟环境（如果还没有）
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1
```

激活成功后，命令行提示符前会显示 `(venv)`。

### 3. 安装依赖

```powershell
# 升级 pip
python -m pip install --upgrade pip

# 安装所有依赖
pip install -r requirements.txt
```

**如果安装遇到网络问题，可以尝试：**
```powershell
# 升级 pip 后重试
python -m pip install --upgrade pip
pip install -r requirements.txt

# 或者使用官方源（默认）
pip install -r requirements.txt
```

### 4. 创建 .env 文件

在项目根目录创建 `.env` 文件：

```powershell
# 创建 .env 文件
New-Item -Path .env -ItemType File -Force

# 编辑 .env 文件（使用记事本）
notepad .env
```

在 `.env` 文件中添加以下内容：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
PORT=8080
```

**重要**: 将 `your_deepseek_api_key_here` 替换为你的实际 API Key。

### 5. 启动应用

#### 方式 A: 启动 Gradio UI（推荐，交互式界面）

```powershell
python -m app.start_server
```

#### 方式 B: 直接启动 Gradio

```powershell
python -m app.gradio_app
```

#### 方式 C: 启动 FastAPI 服务（API 模式）

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### 6. 访问应用

- **Gradio UI**: 打开浏览器访问 `http://localhost:8080`
- **FastAPI API**: 打开浏览器访问 `http://localhost:8080/docs`（查看 API 文档）

### 7. 停止服务

在运行服务的终端中按 `Ctrl + C` 停止服务。

## 常见问题

### 问题 1: 模块导入错误

**错误**: `ImportError: cannot import name 'HfFolder'`

**解决**: 确保安装了正确版本的依赖：
```powershell
pip install -r requirements.txt --force-reinstall
```

### 问题 2: API Key 未设置

**错误**: `DEEPSEEK_API_KEY environment variable is not set`

**解决**: 
1. 检查 `.env` 文件是否在项目根目录
2. 检查 `.env` 文件中的 API Key 是否正确
3. 确保 `.env` 文件格式正确（没有多余的空格或引号）

### 问题 3: 端口被占用

**错误**: `Address already in use`

**解决**: 
```powershell
# 查找占用 8080 端口的进程
netstat -ano | findstr :8080

# 或者使用其他端口
$env:PORT=8081; python -m app.start_server
```

### 问题 4: 依赖安装失败

**解决**: 
```powershell
# 使用官方 PyPI 源（默认）
pip install -r requirements.txt

# 或者逐个安装主要依赖
pip install gradio
pip install langchain-deepseek
pip install langchain-community
pip install fastapi uvicorn
```

## 验证安装

运行以下命令验证关键依赖是否安装成功：

```powershell
python -c "import gradio; print('Gradio:', gradio.__version__)"
python -c "import langchain_deepseek; print('LangChain DeepSeek: OK')"
python -c "from dotenv import load_dotenv; print('python-dotenv: OK')"
```

## 下一步

- 查看 [LOCAL_RUN_GUIDE.md](LOCAL_RUN_GUIDE.md) 了解详细说明
- 查看 [README.md](README.md) 了解项目功能
- 开始使用你的 AI 聊天助手！

