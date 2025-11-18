# Gradio UI 使用指南

## 📋 方案概述

提供了两种方案来实现 Gradio Web UI：

### 方案 1：集成方案（推荐）⭐
**文件**: `app/gradio_app.py`

**特点：**
- ✅ 直接使用 main.py 中的 LLM 对象，无需 HTTP 调用
- ✅ 性能更好，延迟更低
- ✅ 只需要运行一个服务
- ✅ 代码更简洁

**适用场景：**
- 单机部署
- 追求最佳性能
- 简单易用

---

### 方案 2：分离方案（API调用）
**文件**: `app/gradio_app_api.py`

**特点：**
- ✅ 通过 HTTP 调用 main.py 的 API
- ✅ 前后端分离，架构更清晰
- ✅ 可以独立扩展和部署
- ✅ 支持多个客户端同时使用

**适用场景：**
- 需要前后端分离
- 多客户端访问
- 分布式部署

---

## 🚀 快速开始

### 方案 1：集成方案（推荐）

#### 步骤 1：安装依赖

```powershell
pip install gradio requests
```

或重新安装所有依赖：

```powershell
pip install -r requirements.txt
```

#### 步骤 2：运行 Gradio 应用

```powershell
python -m app.gradio_app
```

#### 步骤 3：访问 Web UI

打开浏览器访问：
```
http://localhost:7860
```

**完成！** 现在你可以：
- 在输入框中输入问题
- 点击"发送"或按 Enter 键
- 在聊天界面中看到问题和回复
- 调整温度参数控制回复风格
- 点击"清空"重置对话历史

---

### 方案 2：分离方案（API调用）

#### 步骤 1：启动 API 服务

**终端 1：**
```powershell
python -m app.main
```

服务将在 `http://localhost:8080` 启动

#### 步骤 2：启动 Gradio UI

**终端 2：**
```powershell
python -m app.gradio_app_api
```

#### 步骤 3：访问 Web UI

打开浏览器访问：
```
http://localhost:7860
```

**注意：** 确保 API 服务（main.py）正在运行，否则会显示连接错误。

---

## 🎨 功能特性

### 界面功能

1. **聊天界面**
   - 实时显示对话历史
   - 用户问题和 AI 回复清晰区分
   - 支持多轮对话

2. **配置选项**
   - **Temperature 滑块**：控制回复的随机性
     - 0.0-0.5：更确定、更保守的回复
     - 0.5-1.0：平衡的回复（推荐）
     - 1.0-2.0：更随机、更有创意的回复

3. **操作按钮**
   - **发送**：提交问题
   - **清空**：重置对话历史
   - **刷新状态**（仅方案2）：检查 API 连接状态

### 技术特性

- ✅ 使用 LangChain 管理对话历史
- ✅ 支持系统提示配置
- ✅ 错误处理和日志记录
- ✅ 响应式 UI 设计
- ✅ 支持中文和英文

---

## 📊 架构对比

### 方案 1：集成方案

```
┌─────────────────┐
│  Gradio UI      │
│  (gradio_app.py)│
└────────┬────────┘
         │
         │ 直接调用
         ▼
┌─────────────────┐
│  ChatDeepSeek   │
│  (LLM对象)      │
└────────┬────────┘
         │
         │ HTTP API
         ▼
┌─────────────────┐
│  DeepSeek API   │
│  (远程服务)      │
└─────────────────┘
```

### 方案 2：分离方案

```
┌─────────────────┐         ┌─────────────────┐
│  Gradio UI      │         │  FastAPI        │
│  (gradio_app_   │  HTTP   │  (main.py)      │
│   api.py)       │◄───────►│                 │
└─────────────────┘         └────────┬────────┘
                                      │
                                      │ 直接调用
                                      ▼
                              ┌─────────────────┐
                              │  ChatDeepSeek   │
                              │  (LLM对象)      │
                              └────────┬────────┘
                                       │
                                       │ HTTP API
                                       ▼
                              ┌─────────────────┐
                              │  DeepSeek API   │
                              │  (远程服务)      │
                              └─────────────────┘
```

---

## 🔧 配置说明

### 环境变量

两个方案都需要 `.env` 文件：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com
```

### 端口配置

- **Gradio UI**: 默认端口 `7860`
- **FastAPI**: 默认端口 `8080`（仅方案2需要）

可以在代码中修改端口：

```python
# gradio_app.py 或 gradio_app_api.py
demo.launch(
    server_port=7860,  # 修改为你想要的端口
    ...
)
```

---

## 💡 使用示例

### 示例 1：Python 编程问题

**用户输入：**
```
如何在Python中读取CSV文件？
```

**AI回复：**
```
在Python中读取CSV文件有几种常用方法：

1. 使用pandas（推荐）：
   import pandas as pd
   df = pd.read_csv('file.csv')
   print(df)

2. 使用csv模块：
   import csv
   with open('file.csv', 'r') as file:
       reader = csv.reader(file)
       for row in reader:
           print(row)
...
```

### 示例 2：代码调试

**用户输入：**
```
我的代码报错了：NameError: name 'x' is not defined
```

**AI回复：**
```
这个错误表示变量 `x` 在使用前没有被定义。可能的原因和解决方案：

1. 变量未初始化
2. 作用域问题
3. 拼写错误

请提供你的代码，我可以帮你具体分析。
```

---

## 🐛 故障排除

### 问题 1：无法连接到 DeepSeek API

**解决方案：**
- 检查 `.env` 文件中的 `DEEPSEEK_API_KEY` 是否正确
- 检查网络连接
- 确认 API Key 是否有效

### 问题 2：方案2显示"API服务未连接"

**解决方案：**
- 确保 `main.py` 服务正在运行
- 检查 API 服务地址是否正确（默认 `http://localhost:8080`）
- 点击"刷新状态"按钮检查连接

### 问题 3：Gradio 界面无法访问

**解决方案：**
- 检查端口 7860 是否被占用
- 尝试修改端口号
- 检查防火墙设置

### 问题 4：回复生成很慢

**解决方案：**
- 检查网络连接
- 降低 `max_tokens` 值
- 使用方案1（集成方案）性能更好

---

## 📝 代码说明

### 关键组件

1. **ChatBot 类**
   - 管理对话历史
   - 生成 AI 回复
   - 处理用户输入

2. **create_demo() 函数**
   - 创建 Gradio 界面
   - 配置 UI 组件
   - 绑定事件处理

3. **LLM 初始化**
   - 使用 `langchain_deepseek.ChatDeepSeek`
   - 配置 API Key 和参数
   - 与 main.py 保持一致

---

## 🎯 推荐方案

**对于大多数用户，推荐使用方案1（集成方案）：**

✅ 更简单：只需要运行一个命令  
✅ 更快速：无需 HTTP 调用开销  
✅ 更稳定：减少网络错误  
✅ 更易维护：代码更简洁

**只有在以下情况才考虑方案2：**
- 需要前后端分离架构
- 需要多个客户端同时访问
- 需要独立扩展和部署

---

## 📚 相关文档

- [API 使用指南](API_USAGE_GUIDE.md)
- [本地运行指南](LOCAL_RUN_GUIDE.md)
- [README](README.md)

---

## 🎉 开始使用

选择你喜欢的方案，按照上面的步骤操作，即可开始使用 Gradio Web UI！

如有问题，请查看故障排除部分或提交 Issue。

